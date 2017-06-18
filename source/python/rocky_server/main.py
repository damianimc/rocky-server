from bottle import route, run, template, post, request, get
import json
import os
import platform
from datetime import datetime


PROJECTS_DIR = r'D:/damiani/projects'
MONGO_URL = r'mongodb://rocky-app:TfHx3DDtCR8Rk4Py@ds123182.mlab.com:23182/simulations'


_started_simulations = {}


def post_simulation(project_name):
    from pymongo import MongoClient
    client = MongoClient(MONGO_URL)

    # print(client.server_info())
    rocky = client.simulations.rocky
    return rocky.insert_one({
        'name' : project_name,
        'created' : datetime.now(),
        'server' : platform.node()
    }).inserted_id


@route('/create/<project_name>')
def create_project(project_name):
    cwd = os.path.abspath(os.path.join(PROJECTS_DIR, project_name))
    if os.path.exists(cwd):
        return json.dumps({'error' : 'project already exist!'})

    os.mkdir(cwd)
    project_id = post_simulation(project_name)
    return json.dumps({
        'project' : project_name,
        'directory' : cwd
    })

@route('/list')
def create_project():
    project_list = []
    for dir_name in os.listdir(PROJECTS_DIR):
        project_list.append(dir_name)

    return json.dumps({
        'projects' : project_list
    })    


@get('/simulation_status')
def simulation_status():
    if len(_started_simulations) == 0:
        return json.dumps({'status' : 'no simulation'})

    statuses = []
    for name, (proc, simulation_filename) in _started_simulations.items():
        if proc.poll() is None:
            out_filename = simulation_filename + '.prg'
            with open(out_filename, 'rb') as ifs:
                try:
                    ifs.seek(-1024, 2)
                except Exception as e:
                    print('seek exception', e)
                    last_line = None
                else:
                    last_line = ifs.readlines()[-1].decode()
                    if last_line.startswith('json: '):
                        last_line = json.loads(last_line[len('json: '):])

            statuses.append({'name' : name, 'status' : 'running', 'lastline' : last_line})
        else:
            statuses.append({'name' : name, 'status' : 'finished'})

    return json.dumps({'simulations' : statuses})


@get('/simulation_stop')
def simulation_stop():
    if len(_started_simulations) == 0:
        return json.dumps({'status' : 'no simulation'})

    statuses = []
    for name, (proc, simulation_filename) in _started_simulations.items():
        if proc.poll() is None:
            proc.kill()
            return json.dumps({'status' : 'simulation stopped'})
        else:            
            return json.dumps({'status' : 'simulation already stopped'})

# "c:\Program Files\ESSS\Rocky DEV\bin\RockySolver.exe" --license=C:\Users\ASUS\Downloads\rlm_demo_license_R4.lic --rcy-file=rocky_simulation.rocky20 --ncpus=1
@post('/start_simulation')
def start_simulation():
    import subprocess

    if len(_started_simulations) > 0:
        return json.dumps({'status' : 'error'})

    print('start_simulation:', request)
    kwargs = request.json

    simulation_filename = kwargs['filename']
    if not os.path.exists(simulation_filename):
        return json.dumps({'error' : 'file not found'})
    
    solver = r"c:\Program Files\ESSS\Rocky DEV\bin\RockySolver.exe"
    solver = r"/home/microay/rocky4/Rocky"
    if not os.path.exists(solver):
        return json.dumps({'error' : 'solver executable file not found'})

    license = r"C:\Users\ASUS\Downloads\rlm_demo_license_R4.lic"
    license = r"/home/microway/.Rocky/license.lic"
    if not os.path.exists(license):
        return json.dumps({'error' : 'license file not found'})

    sim_process = subprocess.Popen([
        solver,
        r'--license=' + license,
        '--rcy-file', simulation_filename,
        '--ncpus=1',
        ],
        stdout=None,
        stderr=None,
        cwd=kwargs.get('cwd'),
    )
    print(sim_process.poll())
    _started_simulations['test'] = (sim_process, simulation_filename)

    return json.dumps({'status' : 'started'})


if __name__ == '__main__':
    run(host='localhost', port=8080)

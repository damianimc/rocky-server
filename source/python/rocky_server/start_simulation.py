import requests
import time
from ssh_tunnel import tunnel_microway

with tunnel_microway():
    
    r = requests.post(
        'http://localhost:8080/start_simulation',
        json={
            "filename": r'/home/microway/cases/damiani/rocky_simulation.rocky20',
            "cwd": r'/home/microway/cases/damiani'
        }
    )
    print(r.status_code)
    print(r.json())

    while True:
        r = requests.get('http://localhost:8080/simulation_status')
        if r.status_code != 200:
            break
        
        time.sleep(5.0)
        rj = r.json()
        print(rj)
        if (rj['simulations'][0]['status'] == 'finished'):
            break

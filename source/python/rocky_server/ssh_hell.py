import spur
import time


ms = spur.SshShell(
    hostname='50.245.10.181', port=30039, username='microway', password='RockyDEMdemo!',
    missing_host_key=spur.ssh.MissingHostKey.accept
)

with ms:
    # r = ms.run(['pwd'])
    # print(r.output)

    # r = ms.run(['ls'])
    # print(r.output.decode().split('\n'))

    # # r = ms.run(['cd', 'cases'])
    # # print(r.output.decode().split('\n'))

    # r = ms.run(['ls'], cwd='cases/simulation')
    # print('\n'.join(r.output.decode().split('\n')))

    r = ms.spawn(
        [
            '~/rocky4/RockySolver',
            '--license=/home/microway/.Rocky/license.lic',
            '--rcy-file=rocky_simulation.rocky20',
            '--ncpus=1'
        ],
            cwd='cases/simulation'
    )
    if r.is_running():
        print('still running')
        time.sleep(2)
    
    r = r.wait_for_result()
    print('\n'.join(r.output.decode().split('\n')))

print('done')
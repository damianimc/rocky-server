import paramiko
from scp import SCPClient
import time


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def scp_progress(filename, size, sent):
    print(filename, sent, 'of', size, '%.2f%%' % (100.0 * sent/float(size)))

ssh = createSSHClient('gateway.microway.com', 30039, 'microway', 'RockyDEMdemo!')
scp = SCPClient(ssh.get_transport(), progress=scp_progress)
print("starting")
st = time.time()
scp.put(
    [
        r'D:\damiani\rprojects\rocky_file_dir.rocky30\simulation\rocky_simulation.rocky20',
        r'D:\damiani\rprojects\rocky_file_dir.rocky30\simulation\rocky_simulation_H.txt',
        r'D:\damiani\rprojects\rocky_file_dir.rocky30\simulation\rocky_simulation00000.rhs',
    ],
    remote_path=b'/home/microway/cases/damiani'
)
print('done', time.time() - st)
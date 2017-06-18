from sshtunnel import SSHTunnelForwarder
from contextlib import contextmanager

@contextmanager
def tunnel_microway():
    server = SSHTunnelForwarder(
        ('gateway.microway.com', 30039),
        ssh_username="microway",
        ssh_password="RockyDEMdemo!",
        remote_bind_address=('127.0.0.1', 8080),
        local_bind_address=('127.0.0.1', 8080),
    )

    print('server started')
    server.start()
    yield
    print('server stoped')
    server.stop()
    
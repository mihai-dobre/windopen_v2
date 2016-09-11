import os
from main import RpycServer, init_rpyc_server

# started = os.environ.get('RPYC_STARTED', False)
# if not started:
#     os.environ.setdefault('RPYC_STARTED', 'true')
#     server = RpycServer()
MTU_SERVER = init_rpyc_server()


import os
from main import RpycServer

started = os.environ.get('RPYC_STARTED', False)
if not started:
    os.environ.setdefault('RPYC_STARTED', 'true')
    server = RpycServer()

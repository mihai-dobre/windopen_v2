import time
import threading
from rpyc.utils.server import ThreadPoolServer
from rpyc.core.protocol import DEFAULT_CONFIG
from .rpyc_service import MTUService
from django.conf import settings
from windopen_starter.log import logger_rpyc as log


def start_daemon_thread(method, args):
    thread = threading.Thread(target=method, args=args)
    thread.daemon = True
    thread.start()
    return thread


def keep_server_alive(server):
    while 1:
        if not server.active:
            log.warning("Server not active. Doing restart!")
            start_daemon_thread(server.start, ())
        else:
            time.sleep(2)


def init_rpyc_server():
    DEFAULT_CONFIG.update({"logger": log})
    server = ThreadPoolServer(
        MTUService,
        hostname=settings.HOSTNAME,
        port=settings.RPYC_PORT,
        protocol_config=DEFAULT_CONFIG,
        logger=log,
        reuse_addr=True
    )
    print("Server id: ", id(server))
    try:
        t = start_daemon_thread(keep_server_alive, (server,))
        log.info("RPyc Serving on {}:{}".format(settings.HOSTNAME, settings.RPYC_PORT))
    except Exception as err:
        t.join()
        log.exception("MTUservice initialization failed: %s", err)
    return server




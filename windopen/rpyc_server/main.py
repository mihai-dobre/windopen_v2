import time
import threading
import ssl

from rpyc.utils.authenticators import SSLAuthenticator
from rpyc.utils.server import ThreadPoolServer
from rpyc.core.protocol import DEFAULT_CONFIG
from .rpyc_service import MTUService
from django.conf import settings
from windopen_starter.log import logger_rpyc as log

DAEMON_THREAD = None


def start_daemon_thread(name, method, args):
    thread = threading.Thread(name=name, target=method, args=args, daemon=True)
    thread.start()
    return thread


def keep_server_alive(server):
    global DAEMON_THREAD
    while 1:
        if not server.active:
            log.warning("Server not active. Doing restart!")
            DAEMON_THREAD = start_daemon_thread('RPyCServer', server.start, ())
        log.info('RPYC Server is healthy')
        time.sleep(5)


def init_rpyc_server():
    DEFAULT_CONFIG.update({"logger": log})
    server = ThreadPoolServer(
        MTUService,
        hostname=settings.HOSTNAME,
        port=settings.RPYC_PORT,
        protocol_config=DEFAULT_CONFIG,
        logger=log,
        reuse_addr=True,
        listener_timeout=None,
        nbThreads=5,
        authenticator=SSLAuthenticator(
            keyfile='/var/certs/server.key',
            certfile='/var/certs/server.cert',
            ca_certs='/var/certs/ca.cert',
            # ssl_version=ssl.OPENSSL_VERSION_NUMBER,
        ),
    )
    print("Server id: ", id(server))
    try:
        t = start_daemon_thread('KeepAlive', keep_server_alive, (server,))
        log.info("RPyc Serving on {}:{}".format(settings.HOSTNAME, settings.RPYC_PORT))
    except Exception as err:
        t.join()
        log.exception("MTUservice initialization failed: %s", err)
    return server, DAEMON_THREAD, t


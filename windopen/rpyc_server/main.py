import time
import threading
import ssl

from rpyc.utils.authenticators import SSLAuthenticator
from rpyc.utils.server import ThreadPoolServer, ThreadedServer
from rpyc.core.protocol import DEFAULT_CONFIG
from .rpyc_service import MTUService
from django.conf import settings
from windopen_starter.log import logger_rpyc as log

DAEMON_THREAD = None


def start_daemon_thread(name, method, args, daemon=False):
    thread = threading.Thread(name=name, target=method, args=args, daemon=daemon)
    thread.start()
    return thread


def init_rpyc_server():
    global DAEMON_THREAD
    DEFAULT_CONFIG.update({"logger": log})
    server = ThreadedServer(
        MTUService,
        hostname=settings.HOSTNAME,
        port=settings.RPYC_PORT,
        protocol_config=DEFAULT_CONFIG,
        logger=log,
        reuse_addr=True,
        listener_timeout=None,
        # authenticator=SSLAuthenticator(
        #     keyfile='/var/certs/server.key',
        #     certfile='/var/certs/server.cert',
        #     ca_certs='/var/certs/ca.cert',
        #     # ssl_version=ssl.OPENSSL_VERSION_NUMBER,
        # ),
    )
    print("Server id: ", id(server))
    try:
        DAEMON_THREAD = start_daemon_thread('RPyCServer', server.start, (), True)
        log.info("RPyc Serving on {}:{}".format(settings.HOSTNAME, settings.RPYC_PORT))
    except Exception as err:
        DAEMON_THREAD.join()
        log.exception("MTUservice initialization failed: %s", err)
    return server, DAEMON_THREAD


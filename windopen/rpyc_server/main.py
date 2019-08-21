import os
import ssl
import time
import threading

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
    DEFAULT_CONFIG.update({"logger": log, "sync_request_timeout": 5})
    server = ThreadedServer(
        MTUService,
        hostname=settings.HOSTNAME,
        port=settings.RPYC_PORT,
        protocol_config=DEFAULT_CONFIG,
        logger=log,
        authenticator=SSLAuthenticator(
            keyfile=os.path.join(settings.SSL_PATH, 'keys', 'watering.dev.qadre.io.key.pem'),
            certfile=os.path.join(settings.SSL_PATH, 'certs', 'watering.dev.qadre.io.cert.pem'),
            ca_certs=os.path.join(settings.SSL_PATH, 'certs', 'ca-chain.cert.pem'),
            ssl_version=ssl.PROTOCOL_SSLv23
        ),
        reuse_addr=False,
        listener_timeout=0.1,
    )
    try:
        DAEMON_THREAD = start_daemon_thread('RPyCServer', server.start, (), True)
        log.info("RPyc Serving on {}:{}".format(settings.HOSTNAME, settings.RPYC_PORT))
    except Exception as err:
        DAEMON_THREAD.join()
        log.exception("MTUservice initialization failed: %s", err)
    return server, DAEMON_THREAD


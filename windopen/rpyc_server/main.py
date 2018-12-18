import _thread
from rpyc.utils.server import ThreadPoolServer
from .rpyc_service import MTUService
from django.conf import settings
from windopen_starter.log import logger_rpyc as log


# class Singleton(type):
#     instance = None
#
#     def __call__(cls, *args, **kwargs):
#         if cls.instance is None:
#             cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls.instance
#
#
# class RpycServer(object):
#     __metaclass__ = Singleton
#
#     def __init__(self):
#         print("a creat un server")
#         print(settings.HOSTNAME)
#         try:
#             _thread.start_new_thread(init_rpyc_server, ())
#         except Exception as err:
#             log.error("Failed to start rpyc server: %s", err)


def init_rpyc_server():
    rpyc_t_id = None
    MTU_SERVER = None
    while 1:
        if rpyc_t_id:
            break
        else:
            try:
                MTU_SERVER = ThreadPoolServer(MTUService,
                                              hostname=settings.HOSTNAME,
                                              reuse_addr=True,
                                              port=settings.RPYC_PORT,
                                              protocol_config=settings.R_CONFIG)
                MTU_SERVER.logger.setLevel(30)
                rpyc_t_id = _thread.start_new_thread(MTU_SERVER.start, ())
                msg = "RPyc Serving on {}:{}".format(settings.HOSTNAME, settings.RPYC_PORT)
                log.info(msg)
            except Exception as err:
                log.error("MTUservice initialization failed: %s", err)
    return MTU_SERVER



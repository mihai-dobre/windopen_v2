import time
import thread
import subprocess
from rpyc.utils.server import ThreadPoolServer
from rpyc_service import MTUService
from django.conf import settings
from windopen_starter.log import logger_rpyc as log

class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class RpycServer(object):
    __metaclass__ = Singleton
    
    def __init__(self):
        print 'a creat un server'
        print settings.HOSTNAME
        try:
            thread.start_new_thread(init_rpyc_server, ())
        except Exception as err:
            log.error('Failed to start rpyc server: %s', err)


# def init_rpyc_server():
#     #init_window()
#     rpyc_t_id = None
#     while 1:
#         if rpyc_t_id:
#             time.sleep(1)
#         else:
#             try:
#                 MTU_SERVER = ThreadPoolServer(MTUService,
#                                               hostname=settings.HOSTNAME,
#                                               reuse_addr = True,
#                                               port=settings.RPYC_PORT,
#                                               protocol_config=settings.R_CONFIG)
#                 MTU_SERVER.logger.setLevel(30)
#                 rpyc_t_id = thread.start_new_thread(MTU_SERVER.start, ())
#                 msg = 'RPyc Serving on {}:{}'.format(settings.HOSTNAME, settings.RPYC_PORT)
#                 log.info(msg)
#                 # MTU_SERVER.start()        
#             except Exception as err:
#                 log.error('MTUservice initialization failed: %s', err)


def init_rpyc_server():
    #init_window()
    rpyc_t_id = None
    MTU_SERVER = None
    while 1:
        if rpyc_t_id:
            break
        else:
            try:
                MTU_SERVER = ThreadPoolServer(MTUService,
                                              hostname=settings.HOSTNAME,
                                              reuse_addr = True,
                                              port=settings.RPYC_PORT,
                                              protocol_config=settings.R_CONFIG)
                MTU_SERVER.logger.setLevel(30)
                rpyc_t_id = thread.start_new_thread(MTU_SERVER.start, ())
                msg = 'RPyc Serving on {}:{}'.format(settings.HOSTNAME, settings.RPYC_PORT)
                log.info(msg)
                # MTU_SERVER.start()        
            except Exception as err:
                log.error('MTUservice initialization failed: %s', err)
#                 log.info('try to kill the thread')
#                 p1 = subprocess.Popen(['netstat', '-tulpn'], stdout=subprocess.PIPE)
#                 out = p1.communicate()[0].split('\n')
#                 log.info('This is the pid: %s', out)
#                 pid = None
#                 for line in out:
#                     if '8010' in line:
#                         #log.info('rpyc pid: %s', line)
#                         pid = line.strip().split(' ')[-1].split('/')[0]
#                         log.info('rpyc pid: %s', pid)
#                         break
#                 if pid:
#                     p = subprocess.Popen(['kill', '-9', pid])
    return MTU_SERVER
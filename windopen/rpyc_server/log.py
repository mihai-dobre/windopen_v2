import logging
def setup_log(log_level):
#     logging.basicConfig(level=log_level)
    log = logging.getLogger('MTUServiceLog')
    hdlr = logging.FileHandler('MTUServiceLog.log', 'a')
    hdlr.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%y-%m-%d %H:%M:%S')
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(log_level)
    log.propagate = True
    return log
    

log = setup_log(logging.DEBUG)

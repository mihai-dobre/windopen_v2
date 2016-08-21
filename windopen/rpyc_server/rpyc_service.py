import rpyc
from datetime import datetime

from windopen.models import Device,UnregisteredDevice
from windopen_starter.log import logger_rpyc as log


class MTUService(rpyc.Service):
    # conns={uuid:self._conn
    conns = {}
    def on_connect(self):
        """
        The method runs when a new connection is accepted.
        Here is registered each new RTU
        """
        #log.info('Connecting device: %s', self._conn._config['connid'])
        return self.register_new_device(self._conn)

    def on_disconnect(self):
        # cod care ruleaza dupa ce o conexiune este inchisa
        # radiere RTU
        log.warning('before disconnect: %s', self.conns)
        for uuid, conn in self.conns.iteritems():
            log.info('DISCONECT uuid: %s  connid: %s', uuid, conn._config['connid'])
            if conn._config['connid'] == self._conn._config['connid']:
                device = Device.objects.get(uuid = uuid)
                if device:
                    log.info('Change status to False to device %s: ', uuid)
                    device.active = False
                    device.last_seen = datetime.now()
                    device.save()
                unreg_device = UnregisteredDevice.objects.get(uuid=uuid)
                if unreg_device:
                    log.info('delete the unregistred device %s: ', uuid)
                    unreg_device.delete()
                try:
                    self.conns.pop(uuid)
                except Exception as err:
                    log.error(err)

    def exposed_register(self, device_sn):
        log.warning('Device %s asked for register', device_sn)
        return True

    def get_status(self): 
        return 'open'

    def open_window(self, rtu_uuid):
        if rtu_uuid in self.conns:
            connection = self.conns['rtu_uuid']
            return connection.root.open_window()
        return False
        
    def close_window(self, rtu_uuid):  
        if rtu_uuid in self.conns:
            connection = self.conns['rtu_uuid']
            return connection.root.close_window()
        return False
    
    def register_new_device(self, conn):
        uuid = conn.root.get_uuid()
        log.info('new_uuid: %s', uuid)
        # search through the paired devices
        dvs = Device.objects.get(uuid=uuid)
        log.info('######### devices already: %s',dvs)
        if dvs:
            dvs.active = True
            dvs.last_seen = datetime.now()
            dvs.save()
        else:
            new_device = UnregisteredDevice(uuid=uuid)
            new_device.save()
        self.conns[uuid] = self._conn
        log.info('registered: %s', uuid)
        return True
import rpyc
from django.utils.timezone import now

from windopen_app.models import Device, UnregisteredDevice, Action
from windopen_starter.log import logger_rpyc as log


class MTUService(rpyc.Service):
    conns = {}

    def on_connect(self, conn):
        """
        The method runs when a new connection is accepted.
        Here is registered each new RTU
        """
        # log.info("Connecting device: %s", conn._config["connid"])
        return self.register_new_device(conn)

    def on_disconnect(self, conn):
        # cod care ruleaza dupa ce o conexiune este inchisa
        # radiere RTU
        log.warning("before disconnect: %s", self.conns)
        for uuid, saved_conn in self.conns.items():
            log.info("DISCONECT uuid: %s  connid: %s", uuid, conn._config["connid"])
            if saved_conn._config["connid"] == conn._config["connid"]:
                device = Device.objects.get(uuid=uuid)
                if device:
                    log.info("Change status to False to device %s: ", uuid)
                    device.active = False
                    device.last_seen = now()
                    device.save()
                unreg_device = UnregisteredDevice.objects.get(uuid=uuid)
                if unreg_device:
                    log.info("delete the unregistred device %s: ", uuid)
                    unreg_device.delete()
                try:
                    self.conns.pop(uuid)
                except Exception as err:
                    log.error(err)
    
    def exposed_action_finished(self, uuid, action):
        """
        change status for device
        """
        log.warning("action finished: %s for device %s", action, uuid)
        try:
            d = Device.objects.get(uuid=uuid)
        except Exception as err:
            d = None
        if d:
            try:
                actions = Action.objects.filter(device=d)
                log.info("toate actiunile: %s", len(actions))
                a = actions[len(actions)-1]
                log.info("action: %s", a.__dict__)
            except Exception as err:
                log.error("Unable to retrieve the action: %s", err)
            if action == "open":
                a.status = "open"
                a.action_end = now()
                a.save()
                d.status = "open"
                d.save()
                log.warning("status update for action %s", action)
            elif action == "close":
                a.status = "close"
                a.action_end = now()
                a.save()
                d.status = "close"
                d.save()
                log.warning("status update for action %s", action)
        return True

    def exposed_register(self, device_sn):
        log.warning("Device %s asked for register", device_sn)
        return True

    def get_status(self): 
        return "open"

    @classmethod
    def open_window(self, rtu_uuid):
        if rtu_uuid in self.conns:
            connection = self.conns[rtu_uuid]
            log.info("window `%s` opens", rtu_uuid)
            return connection.root.open_window()
        return False

    @classmethod
    def close_window(self, rtu_uuid):
        if rtu_uuid in self.conns:
            connection = self.conns[rtu_uuid]
            log.info("window `%s` closes", rtu_uuid)
            return connection.root.close_window()
        return False
    
    def register_new_device(self, conn):
        uuid = conn.root.get_uuid()
        log.info("new_uuid: %s", uuid)
        # search through the paired devices
        try:
            dvs = Device.objects.get(uuid=uuid)
        except Exception as err:
            log.info("Device is not registered: %s", uuid)
            dvs = []
        log.info("######### devices already: %s", dvs)
        if dvs:
            dvs.active = True
            dvs.last_seen = now()
            dvs.save()
        else:
            new_device = UnregisteredDevice(uuid=uuid)
            new_device.save()
        self.conns[uuid] = conn
        log.info("registered: %s | %s", uuid, conn)
        return True

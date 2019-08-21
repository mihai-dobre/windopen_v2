import rpyc
from django.utils.timezone import now
from django.conf import settings

from windopen_app.models import Device, UnregisteredDevice, Action
from windopen_starter.log import logger_rpyc as log


def set_device_status(device_uuid, conn):
    try:
        device = Device.objects.get(uuid=device_uuid)
        device.active = False
        device.last_seen = now()
        device.save()
        log.info("Change status to False to device %s ", device_uuid)
    except Device.DoesNotExist:
        log.warning("Device %s not found in Registered devices. Searching in the unregistred...", device_uuid)
    except Exception:
        log.exception("Unexpected error:")
    log.warning("Shutting down beacon for connection: %s", conn._config["connid"])
    settings.SCHEDULER.remove_job(conn._config["connid"])


def delete_from_unregistered(device_uuid):
    try:
        unreg_device = UnregisteredDevice.objects.get(uuid=device_uuid)
        unreg_device.delete()
        log.info("Delete the unregistred device %s: ", device_uuid)
    except UnregisteredDevice.DoesNotExist:
        log.warning("Device does not exist in unregistered: %s", device_uuid)
    except Exception:
        log.exception("Unexpected error:")


def run_beacon(conn, uuid):
        log.info("Running beacon for device: %s | connection: %s", uuid, conn._config["connid"])
        try:
            device = Device.objects.get(uuid=uuid)
        except Device.DoesNotExist:
            log.info("Device does not exist")
            return
        except Exception:
            log.exception("Don't know what is happening?!?!")
        try:
            status = conn.root.get_status()
            device.active = True
            device.last_seen = now()
            device.save()
        except Exception:
            device.active = False
            device.save()
            log.warning("Device not active!!!")
            log.warning("Shutting down beacon for connection: %s", conn._config["connid"])
            settings.SCHEDULER.remove_job(conn._config["connid"])


class MTUService(rpyc.Service):
    conns = {}

    def on_connect(self, conn):
        """
        The method runs when a new connection is accepted.
        Here is registered each new RTU
        """
        log.info("Connecting device: %s", conn._config["connid"])
        self.register_new_device(conn)

    def on_disconnect(self, conn):
        # cod care ruleaza dupa ce o conexiune este inchisa
        # radiere RTU
        log.warning("before disconnect: %s", MTUService.conns)
        pop_list = []
        for uuid, saved_conn in MTUService.conns.items():
            if saved_conn._config["connid"] == conn._config["connid"]:
                log.info("DISCONECT uuid: %s  connid: %s", uuid, conn._config["connid"])
                # set status offline if device registered. Delete device if unregistered.
                settings.SCHEDULER.add_job(set_device_status, None, args=[uuid, conn])
                settings.SCHEDULER.add_job(delete_from_unregistered, None, args=[uuid])
                pop_list.append(uuid)
        for uuid in pop_list:
            try:
                MTUService.conns.pop(uuid)
            except Exception as err:
                log.exception("Trying to delete connections from pool.")
    
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

    @staticmethod
    def get_status(uuid):
        if uuid in MTUService.conns:
            conn = MTUService.conns[uuid]
            log.info("getting status for device: %s", uuid)
            status = conn.root.get_status()
            log.info("device status is: %s", status)
            return True if status in ["open", "closed"] else False
        return False

    @staticmethod
    def open_window(rtu_uuid):
        if rtu_uuid in MTUService.conns:
            connection = MTUService.conns[rtu_uuid]
            log.info("window `%s` opens", rtu_uuid)
            return connection.root.open_window()
        return False

    @staticmethod
    def close_window(rtu_uuid):
        if rtu_uuid in MTUService.conns:
            connection = MTUService.conns[rtu_uuid]
            log.info("window `%s` closes", rtu_uuid)
            return connection.root.close_window()
        return False

    def register_new_device(self, conn):
        uuid = conn.root.get_uuid()
        log.info("new_uuid: %s", uuid)
        # search through the paired devices
        try:
            dvs = Device.objects.get(uuid=uuid)
            dvs.active = True
            dvs.last_seen = now()
            dvs.save()
            log.info("Device `%s` is already registered.", dvs)
        except Device.DoesNotExist:
            log.info('new device. Adding it to unregistered devices: {}'.format(uuid))
            new_device = UnregisteredDevice(uuid=uuid)
            new_device.save()
        except Exception:
            log.exception("Unable to register new or existing device: %s", uuid)
        MTUService.conns[uuid] = conn
        log.info("Starting the beacon for device: %s | conn: %s", uuid, conn._config["connid"])
        settings.SCHEDULER.add_job(run_beacon, "interval", minutes=1, id=conn._config["connid"], args=[conn, uuid])


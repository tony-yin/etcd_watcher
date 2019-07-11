import sys
import etcd
import traceback
from log import get_logger

logger = get_logger(__name__, '/var/log/etcd_watcher.log')


class EtcdClient(object):
    def __init__(self):
        self.hostname = get_hostname()
        self.connect()
        self.ttl = 60
        self.store_dir = '/etcd_watcher'
        self.master_file = '{}/{}'.format(self.store_dir, 'master')
        self.master_value = self.hostname
        # node status
        self.Master = 'Master'
        self.Slave = 'Slave'
        self.ToMaster = 'ToMaster'
        self.ToSlave = 'ToSlave'
        self.InitMaster = 'InitMaster'
        self.InitSlave = 'InitSlave'
        # basic status: master or slave
        self.last_basic_status = None
        self.current_basic_status = None

    def connect(self):
        try:
            self.client = etcd.Client(
                host='localhost',
                port=2379,
                allow_reconnect=True,
                protocol='https',
                cert=(
                    '/etc/ssl/etcd/ssl/node-{}.pem'.format(self.hostname),
                    '/etc/ssl/etcd/ssl/node-{}-key.pem'.format(self.hostname)
                ),
                ca_cert='/etc/ssl/etcd/ssl/ca.pem'
            )
        except Exception as e:
            logger.error("connect etcd failed: {}".format(str(e)))

    def get(self, key):
        try:
            value = self.client.read(key).value
            return value
        except etcd.EtcdKeyNotFound:
            logger.error("Key {} not found.".format(key))
        except Exception as e:
            logger.error("Get key {} value failed: {}".format(key, str(e)))

    def set(self, key, value):
        try:
            self.client.write(key, value)
            return value
        except etcd.EtcdKeyNotFound:
            logger.error("Key {} not found.".format(key))
        except Exception as e:
            logger.error("Get key {} value failed: {}".format(key, str(e)))

    def delete(self, key):
        try:
            self.client.delete(key)
        except etcd.EtcdKeyNotFound:
            logger.error("Key {} not found.".format(key))
        except Exception as e:
            logger.error("Delete key {} failed: {}".format(key, str(e)))

    def get_dir_items(self, dir_name):
        items = {}
        try:
            r = self.client.read(dir_name, recursive=True, sorted=True)
            for child in r.children:
                items[child.key] = child.value
        except Exception as e:
            logger.error("get dir items failed: {}".format(str(e)))
        return items

    def get_watcher_items(self):
        items = {}
        try:
            items = self.get_dir_items(self.store_dir)
        except Exception as e:
            logger.error("get etcd watcher items failed: {}".format(str(e)))
        return items

    def get_watcher_keys(self):
        keys = []
        try:
            items = self.get_watcher_items()
            keys = items.keys()
        except Exception as e:
            logger.error("get etcd watcher keys failed: {}".format(str(e)))
        return keys

    def create_master(self):
        logger.info('Create master.')
        try:
            self.client.write(
                self.master_file,
                self.master_value,
                ttl=self.ttl,
                prevExist=False
            )
        except Exception as e:
            logger.error("Create master failed: {}".format(str(e)))

    def get_master(self):
        try:
            master_value = self.get(self.master_file)
            return master_value
        except etcd.EtcdKeyNotFound:
            logger.error("Key {} not found.".format(self.master_file))
        except Exception as e:
            logger.error("Get master value failed: {}".format(str(e)))

    def update_master(self):
        try:
            self.client.write(
                self.master_file,
                self.master_value,
                ttl=self.ttl,
                prevValue=self.master_value,
                prevExist=True
            )
        except Exception as e:
            logger.error("Update master failed: {}".format(str(e)))


    def get_node_basic_status(self):
        node_basic_status = None
        try:
            master_value = self.get_master()
            if master_value == self.master_value:
                node_basic_status = self.Master
            else:
                node_basic_status = self.Slave
        except Exception as e:
            logger.error("get node basic status failed: {}".format(str(e)))
        return node_basic_status


def get_hostname():
    with open('/etc/hostname', 'r') as f:
        hostname = f.read().strip()
    return hostname


if __name__ == "__main__":
    try:
        args = sys.argv
        logger.info("etcd client args: {}".format(str(args)))
        if len(args) < 2:
            logger.error("Invalid parameter length!")

        op = args[1]
        etcd_client = EtcdClient()
        if op == "update":
            key, value = args[2:4]
            logger.info("update key {} to {}".format(key, value))
            etcd_client.set(key, value)
        elif op == "get":
            key = args[2]
            value = etcd_client.get(key)
            logger.info("get key {} value: {}".format(key, value))
            print(value)
        elif op == "delete":
            key = args[2]
            logger.info("delete key {}".format(key))
            etcd_client.delete(key)
        elif op == "get_watcher_master":
            value = etcd_client.get(etcd_client.master_file)
            logger.info("get watcher master: {}".format(value))
            print(value)
        elif op == "get_etcd_master":
            value = etcd_client.client.leader
            logger.info("get etcd master: {}".format(value))
            print(value)
        elif op == "get_member_list":
            value = etcd_client.client.machines
            logger.info("get member list: {}".format(value))
            print(value)
        elif op == "get_watcher_items":
            value = etcd_client.get_watcher_items()
            print(value)
        elif op == "get_dir_items":
            dir_name = args[2]
            value = etcd_client.get_dir_items(dir_name)
            print(value)
        else:
            logger.error("Invalid op parameter!")
    except Exception:
        logger.error("Etcd watcher error: {}".format(traceback.format_exc()))

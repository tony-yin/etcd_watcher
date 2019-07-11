#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import traceback
import subprocess
from log import get_logger
from threading import Thread
from etcd_client import EtcdClient

logger = get_logger(__name__, '/var/log/etcd_watcher.log')


class EtcdWatcher(Thread):
    def __init__(self, *args, **kwargs):
        self.interval = 30
        self.etcd_client = EtcdClient()
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
        super(EtcdWatcher, self).__init__(*args, **kwargs)


    def get_node_status(self):
        self.last_basic_status = self.current_basic_status
        self.current_basic_status = self.etcd_client.get_node_basic_status()
        node_status = None
        if self.current_basic_status == self.Master:
            if self.last_basic_status is None:
                node_status = self.InitMaster
            elif self.last_basic_status == self.Master:
                node_status = self.Master
            elif self.last_basic_status == self.Slave:
                node_status = self.ToMaster
            else:
                logger.error("Invalid last basic status for master: {}".format(
                    self.last_basic_status)
                )
        elif self.current_basic_status == self.Slave:
            if self.last_basic_status is None:
                node_status = self.InitSlave
            elif self.last_basic_status == self.Master:
                node_status = self.ToSlave
            elif self.last_basic_status == self.Slave:
                node_status = self.Slave
            else:
                logger.error("Invalid last basic status for slave: {}".format(
                    self.last_basic_status)
                )
        else:
            logger.error("Invalid current basic status: {}".format(
                self.current_basic_status)
            )

        return node_status

    def do_ToMaster_work(self):
        logger.info("===== do ToMaster work =====")
        pass

    def do_InitMaster_work(self):
        logger.info("===== do InitMaster work =====")
        pass

    def do_ToSlave_work(self):
        logger.info("===== do ToSlave work =====")
        pass

    def do_InitSlave_work(self):
        logger.info("===== do ToInit work =====")
        pass

    def run(self):
        try:
            logger.info("===== Init Etcd Wathcer =====")
            self.etcd_client.create_master()
            while True:
                node_status = self.get_node_status()
                logger.info("node status : {}".format(node_status))
                if node_status == self.etcd_client.ToMaster:
                    self.do_ToMaster_work()
                    self.etcd_client.update_master()
                elif node_status == self.etcd_client.InitMaster:
                    self.do_InitMaster_work()
                    self.etcd_client.update_master()
                elif node_status == self.etcd_client.Master:
                    self.etcd_client.update_master()
                elif node_status == self.etcd_client.ToSlave:
                    self.do_ToSlave_work()
                    self.etcd_client.create_master()
                elif node_status == self.etcd_client.InitSlave:
                    self.do_InitSlave_work()
                    self.etcd_client.create_master()
                elif node_status == self.etcd_client.Slave:
                    self.etcd_client.create_master()
                else:
                    logger.error("Invalid node status: {}".format(node_status))
                time.sleep(self.interval)
                self.etcd_client = EtcdClient()
        except Exception:
            logger.error("Etcd watcher run error:{}".format(traceback.format_exc()))


def get_hostname():
    with open('/etc/hostname', 'r') as f:
        hostname = f.read().strip()
    return hostname


def do_shell(cmd):
    p = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    while p.poll() is None:
        try:
            proc = psutil.Process(p.pid)
            for c in proc.children(recursive=True):
                c.kill()
                proc.kill()
        except psutil.NoSuchProcess:
            pass
    if p.returncode == 1:
        logger.error("Cmd {} returncode is error!".format(cmd))
    return output


def main():
    pass


if __name__ == "__main__":
    try:
        watcher = EtcdWatcher()
        watcher.start()
        watcher.join()
    except Exception:
        logger.error("Etcd watcher error: {}".format(traceback.format_exc()))

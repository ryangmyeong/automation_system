#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import os
import sys


def create_relay08_cmd(port_id, stime=0.5, comport='/dev/ttyUSB4'):
    """
    create_relay08_cmd
    auto create relay08 cmd,and run it
    """
    with open("runner/operation_lib/host_passwd") as pwdfp:
        host_passwd = pwdfp.read()

    cmd = 'echo '+host_passwd+' | sudo -S python runner/operation_lib/base_lib/relay08_ctrl_button.py'
    if port_id in range(1, 9):
        cmd = cmd + ' -p ' + str(port_id)
    else:
        print '******please input correct port_id which in (1~8)********'
        sys.exit()

    if not stime == 0.5:
        cmd = cmd + ' -t ' + str(stime)

    if not comport == '/dev/ttyUSB4':
        cmd = cmd + ' -c ' + str(comport)
    os.system(cmd)


def create_relay08_cmd_ifwi(port_id, ifwi, stime=0.5, comport='/dev/ttyUSB4', host_passwd='123456'):
    """
    create_relay08_cmd
    auto create relay08 cmd,and run it
    """
    cmd = 'echo '+host_passwd+' | sudo -S python runner/operation_lib/base_lib/relay08_ctrl_button.py'
    if port_id in range(1, 9):
        cmd = cmd + ' -p ' + str(port_id)
    else:
        print '******please input correct port_id which in (1~8)********'
        sys.exit()

    if not stime == 0.5:
        print 'stime ==== ', stime
        cmd = cmd + ' -t ' + str(stime)
    if not comport == '/dev/ttyUSB4':
        cmd = cmd + ' -c ' + str(comport)

    if ifwi in range(1, 9):
        cmd = cmd + ' -i ' + str(ifwi)
    os.system(cmd)


class control_relay08_port_thread(threading.Thread):
    """
    class control_ignition_thread
    """

    def __init__(self, threadID="", name="", port_id=4, stime=0.5, comport='/dev/ttyUSB4'):
        """
        control_ignition_thread __init__
        """
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.port_id = port_id
        self.stime = stime
        self.comport = comport
        print "*************************************"
        print self.comport
        print "*************************************"

    def run(self): 
        """
        threading run
        """
        create_relay08_cmd(self.port_id, self.stime, self.comport)

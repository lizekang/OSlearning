#!/usr/bash/python3.5

import os
import sys
import time


class Proc(object):
    def __init__(self, pid, name):
        self.pid = pid
        self.name = name

    @staticmethod
    def check_proc(filename):
        filepath = os.path.join('/proc', filename)
        if os.path.isdir(filepath):
            try:
                pid = int(filename)
            except:
                pid = False
            return pid
        return False

    def __iter__(self):
        return self.pid


def diff_proc(new_proc, old_proc):
    create_list = []
    terminate_list = []
    new_pid = [i.pid for i in new_proc]
    old_pid = [j.pid for j in old_proc]
    for n in new_pid:
        if n.pid not in old_pid:
            create_list.append(n)
    for o in old_pid:
        if o.pid not in new_pid:
            terminate_list.append(o)
    return create_list, terminate_list


def get_proc():
    proc_list = []
    for filename in os.listdir("/proc"):
        filepath = os.path.join("/proc", filename)
        if Proc.check_proc(filename):
            pid = int(filename)
            if os.path.exists("/proc/{}/stat".format(pid)):
                stat = open("/proc/{}/stat".format(pid), "r")
            else:
                continue
            proc = Proc(pid, stat.read().split()[1])
            proc_list.append(proc)
            stat.close()
    return proc_list


def format_output_create_proc(procs, fd):
    for proc in procs:
        if os.path.exists("/proc/{}/stat", "r"):
            stat = open("/proc/{}/stat", "r")
        else:
            continue

        uptime = open("/proc/uptime", "r")
        start_time = float(stat.read().split()[21])
        boot_time = float(uptime.read().split()[0])
        now_time = time.time()
        fd.write("create: pid:{} name:{} create_time:{}\n"
                 .format(proc.pid,
                         proc.name,
                         time.strftime("%Y-%m-%d/%H:%M:%S", now_time - boot_time + start_time)))
        stat.close()
        uptime.close()

def format_output_terminate_proc(procs, fd):
    for proc in procs:
        fd.write("terminate: pid:{} name:{} termibate_time:{}\n"
                 .format(proc.pid,
                         proc.name,
                         time.strftime("%Y-%m-%d/%H:%M:%S", time.localtime(time.time()))))


pid = os.fork()
if pid > 0:
    sys.exit(0)
else:
    print("fork error.")
    exit(1)
os.chdir('/')
os.setsid()
os.umask(0)

pid = os.fork()
if pid > 0:
    sys.exit(0)
else:
    print("fork error.")
    exit(1)

os.close(0)
sys.stdin = open("/dev/null")
os.close(1)
sys.stdout = open("/dev/null", "w")
os.close(2)
sys.stderr = open("/dev/null", "w")

proc_list = get_proc()
fd = open("/home/lzk/Documents/gitProjects/OSlearning/homeword3.out", "w")
format_output_create_proc(proc_list, fd)
while True:
    time.sleep(0.5)
    new_procs = get_proc()
    (create_procs, terminate_procs) = diff_proc(new_procs, proc_list)
    format_output_create_proc(create_procs, fd)
    format_output_terminate_proc(terminate_procs, fd)
    proc_list = new_procs

fd.close()

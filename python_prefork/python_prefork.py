#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import signal
import time

class PythonPrefork:
  def __init__(self,
               max_workers=10,
               trap_signals=[signal.SIGTERM],
               on_reap_cb=None):
    self.max_workers     = max_workers
    self.worker_pids     = {}
    self.in_child        = False
    self.trap_signals    = trap_signals
    self.on_reap_cb      = on_reap_cb
    self.signal_received = None
    for sig in trap_signals:
      signal.signal(sig, self._signal_receive)

  def start(self):
    self.manager_pid = os.getpid()
    if self.in_child:
      raise "can't start while you are in subprocess"

    while not self.signal_received:
      pid = None
      if len(self.worker_pids) < self.max_workers:
        # fork anothrer process
        pid = os.fork()
        if pid == 0:
          self.in_child = True
          return False   # return child process
        else:
          self.worker_pids[pid] = 1
      if not pid:
        try:
          (pid, status) = os.wait()
          del(self.worker_pids[pid])
          self._run_reap_cb(pid, status)
        except OSError:  # when parent process is signaled
          pass 

    self._signal_all_children(self.signal_received)
    return True  # return parent process
    
  def finish(self):
    if self.in_child is True:
      os._exit(0)  # not to raise SystemExit

  def wait_all_children(self):
    while len(self.worker_pids) > 0:
      (pid, status) = os.wait()
      del(self.worker_pids[pid])
      self._run_reap_cb(pid, status)

  def _signal_receive(self, sig, status):
    self.signal_received = sig

  def _signal_all_children(self, sig):
    self.signal_received = sig
    for pid in self.worker_pids.keys():
      os.kill(pid, sig)

  def _run_reap_cb(self, pid, status):
    if self.on_reap_cb:
      self.on_reap_cb(pid, status)
    

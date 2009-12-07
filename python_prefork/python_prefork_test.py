#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import os, fcntl, signal, time, unittest
from python_prefork import PythonPrefork

class PyPreforkTest(unittest.TestCase):
  def testBasic(self):
    reap_cnt = [0]
    def callback(pid, status):
      val = reap_cnt.pop() + 1
      reap_cnt.append(val)
    pp  = PythonPrefork(on_reap_cb=callback)
    filename = 'test.txt'
    with file(filename, 'w') as fh:
      fh.write('0')
    
    while pp.signal_received is None:
      if pp.start(): continue
      with file(filename, 'r+') as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        num = int(fh.read()) + 1
        fh.seek(0, os.SEEK_SET)
        fh.write("%d" % (num))
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
      if num == pp.max_workers:
        os.kill(pp.manager_pid, signal.SIGTERM)
      time.sleep(5)
      pp.finish()
    pp.wait_all_children()
    
    self.assertEqual(int(file(filename, 'r').read()), pp.max_workers)
    self.assertEqual(reap_cnt[0], pp.max_workers)
    os.remove(filename)

if __name__ == '__main__':
  unittest.main()
  

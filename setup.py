# -*- coding: utf-8 -*-
from setuptools import setup
import sys
import unittest

import python_prefork
from python_prefork import __version__, __license__, __author__
from python_prefork import python_prefork_test

if __name__ == '__main__':
  # run module test
  loader = unittest.TestLoader()
  result = unittest.TestResult()
  suite  = loader.loadTestsFromModule(python_prefork_test)
  suite.run(result)
  if not result.wasSuccessful():
    print "unit tests have failed!"
    print "aborted to make a source distribution"
    sys.exit(1)

  # build distribution package
  setup(
    name             = 'python_prefork',
    version          = __version__,
    py_modules       = ['python_prefork', 'python_prefork_test'],
    description      = 'parallel processing fork manager inspired by Parallel::Prefork in CPAN',
    long_description = python_prefork.__doc__,
    author           = __author__,
    author_email     = 'taichino@gmail.com',
    url              = 'http://github.com/taichino/python_prefork',
    keywords         = 'multi process, parallel, prefork',
    license          = __license__,
    packages         = ('python_prefork',),
    classifiers      = ["Development Status :: 3 - Alpha",
                        "Intended Audience :: Developers",
                        "License :: OSI Approved :: MIT License",
                        "Operating System :: POSIX",
                        "Programming Language :: Python",
                        "Topic :: Software Development :: Libraries :: Python Modules"]
    )

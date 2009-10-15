# Copyright Sylvain Viollon 2008 (c)
# $Id: tests.py 85 2008-10-18 00:15:41Z sylvain $

from zope.testing import doctest
from zope.testing.doctest import DocFileSuite
from zope.app.testing.functional import FunctionalTestSetup, ZCMLLayer, \
    HTTPCaller, getRootFolder, sync

import zeam.utils.batch
import unittest, os

config = os.path.join(os.path.dirname(zeam.utils.batch.__file__),
                      'ftesting.zcml')
FunctionalLayer = ZCMLLayer(config, __name__, 'FunctionalLayer',
                            allow_teardown=True)

def setUp(test):
    FunctionalTestSetup().setUp()

def tearDown(test):
    FunctionalTestSetup().tearDown()

options=(doctest.ELLIPSIS+
         doctest.NORMALIZE_WHITESPACE+
         doctest.REPORT_NDIFF)

def test_suite():
    batchs = DocFileSuite('batch.txt',
                          optionflags=options)
    views = DocFileSuite('views.txt',
                         globs=dict(getRootFolder=getRootFolder,
                                    sync=sync),
                         optionflags=options)
    views.layer = FunctionalLayer

    suite = unittest.TestSuite()
    suite.addTest(batchs)
    suite.addTest(views)
    return suite


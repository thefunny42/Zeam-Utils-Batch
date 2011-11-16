
import unittest

from zope.testing import doctest
from zeam.utils.batch.tests import FunctionalLayer


def test_suite():
    globs = dict(__name__="zeam.utils.batch.alphabetical",
                 getRootFolder=FunctionalLayer.getRootFolder)
    optionflags = (doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)

    batchs = doctest.DocFileSuite(
        'batch.txt', optionflags=optionflags, globs=globs)

    suite = unittest.TestSuite()
    suite.addTest(batchs)
    return suite

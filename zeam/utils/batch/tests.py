# Copyright Sylvain Viollon 2008 (c)
# $Id: tests.py 85 2008-10-18 00:15:41Z sylvain $

import os.path
import unittest
from zope.testing import doctest, module
from zope.app.testing import functional

ftesting_zcml = os.path.join(os.path.dirname(__file__), 'ftesting.zcml')
FunctionalLayer = functional.ZCMLLayer(
    ftesting_zcml, __name__, 'FunctionalLayer', allow_teardown=True
    )


def test_suite():
    
    batchs = doctest.DocFileSuite('batch.txt',
        optionflags=(doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE),
        )

    readme = functional.FunctionalDocFileSuite('README.txt',
        globs = dict(__name__="zeam.utils.batch"),
        )

    views = functional.FunctionalDocFileSuite('views.txt')
    
    views.layer = FunctionalLayer
    readme.layer = FunctionalLayer

    suite = unittest.TestSuite()
    suite.addTest(readme)
    suite.addTest(batchs)
    suite.addTest(views)
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

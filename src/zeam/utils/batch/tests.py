# Copyright Sylvain Viollon 2008 (c)
# $Id: tests.py 85 2008-10-18 00:15:41Z sylvain $

import unittest

from zope.testing import doctest
from zope.app.wsgi.testlayer import BrowserLayer
import zeam.utils.batch

FunctionalLayer = BrowserLayer(zeam.utils.batch)


def test_suite():
    globs = dict(__name__="zeam.utils.batch",
                 getRootFolder=FunctionalLayer.getRootFolder)
    optionflags = (doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)

    batchs = doctest.DocFileSuite(
        'batch.txt', optionflags=optionflags, globs=globs)
    readme = doctest.DocFileSuite(
        'README.txt', optionflags=optionflags, globs=globs)
    views = doctest.DocFileSuite(
        'views.txt', optionflags=optionflags, globs=globs)

    views.layer = FunctionalLayer
    readme.layer = FunctionalLayer

    suite = unittest.TestSuite()
    suite.addTest(readme)
    suite.addTest(batchs)
    suite.addTest(views)
    return suite

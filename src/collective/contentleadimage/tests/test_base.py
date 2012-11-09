import doctest
import unittest

from plone.testing import layered

from collective.contentleadimage.testing import \
    COLLECTIVE_CONTENTLEADIMAGE_FUNCTIONAL_TESTING

def getdoctestfile(filename):
    return layered(doctest.DocFileSuite(filename,
            package='collective.contentleadimage'),
            layer=COLLECTIVE_CONTENTLEADIMAGE_FUNCTIONAL_TESTING)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(getdoctestfile('README.txt'))
    try:
        from Products.CacheSetup.interfaces import IPurgeUrls
        suite.addTest(getdoctestfile('tests/cachesetup.txt'))
    except ImportError:
        pass
    return suite


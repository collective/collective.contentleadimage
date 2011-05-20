import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import collective.contentleadimage

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             collective.contentleadimage)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass
    

def test_suite():

    suite = [
        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'README.txt', package='collective.contentleadimage',
            test_class=TestCase),
        ]

    try:
        from Products.CacheSetup.interfaces import IPurgeUrls
        suite.append(
            ztc.ZopeDocFileSuite(
                'tests/cachesetup.txt', package='collective.contentleadimage',
                test_class=TestCase)
        )
    except ImportError:
        pass
    
    return unittest.TestSuite(suite)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
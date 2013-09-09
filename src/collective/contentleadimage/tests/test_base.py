# -*- coding: utf-8 -*-
import doctest
import unittest
import os.path

from plone.testing import layered
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from collective.contentleadimage.config import IMAGE_FIELD_NAME

from collective.contentleadimage.testing import (
    COLLECTIVE_CONTENTLEADIMAGE_FUNCTIONAL_TESTING,
    COLLECTIVE_CONTENTLEADIMAGE_INTEGRATION_TESTING)

from collective.contentleadimage.browser.folder_leadimage_view import \
   FolderLeadImageView 

def getdoctestfile(filename):
    return layered(doctest.DocFileSuite(filename,
            package='collective.contentleadimage'),
            layer=COLLECTIVE_CONTENTLEADIMAGE_FUNCTIONAL_TESTING)

class ViewTests(unittest.TestCase):

    layer = COLLECTIVE_CONTENTLEADIMAGE_INTEGRATION_TESTING

    def test_browserview_tag(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Document', 'doc1')
    	doc1 = portal['doc1']
    	doc1.update(title='Kinderbetreuung f\xc3\xbcr Studierende und Mitarbeitende',
                    leadImage_caption='Hügel mit Aussicht')
        field = doc1.getField(IMAGE_FIELD_NAME)
        img = open(os.path.join(os.path.dirname(__file__), 'test_41x41.jpg')).read()
        field.set(doc1, img)
	
        view = FolderLeadImageView(portal, self.layer['request'])
        self.assertEqual(view.tag(doc1), (
           '<img src="http://nohost/plone/doc1/leadImage_thumb" '
           'alt="Kinderbetreuung für Studierende und Mitarbeitende" '
           'title="Hügel mit Aussicht" height="41" width="41" '
           'class="tileImage" />'))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(getdoctestfile('README.txt'))
    suite.addTests(unittest.makeSuite(ViewTests))
    try:
        from Products.CacheSetup.interfaces import IPurgeUrls
        IPurgeUrls  # pyflakes
        suite.addTest(getdoctestfile('tests/cachesetup.txt'))
    except ImportError:
        pass
    return suite

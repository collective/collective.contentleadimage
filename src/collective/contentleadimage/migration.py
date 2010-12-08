from Products.CMFCore.utils import getToolByName
from collective.contentleadimage.interfaces import ILeadImageable
from collective.contentleadimage.config import CONTENT_LEADIMAGE_ANNOTATION_KEY
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.extender import LeadImageExtender
from zope.annotation import IAnnotations
import logging
logger = logging.getLogger('leadimgae.migration')


def migrate0xto1(context):
    portal = context.portal_url.getPortalObject()
    ctool  = getToolByName(portal, 'portal_catalog')
    items = ctool(object_provides=ILeadImageable.__identifier__) 
    cnt = len(items)
    logger.info('Migrating %d items' % cnt)
    for item in items:
        obj = item.getObject()
        image = IAnnotations(obj).get(CONTENT_LEADIMAGE_ANNOTATION_KEY, None)
        if image:
            logger.info('Migrating item %s' % '/'.join(obj.getPhysicalPath()))
            field = obj.getField(IMAGE_FIELD_NAME)
            if field and image.get('data', ''):
                field.set(obj, image['data'], mimetype=image['contenttype'])
            # remove annotation key
            del IAnnotations(obj)[CONTENT_LEADIMAGE_ANNOTATION_KEY]
            
def migrateToBlobs(context):
    from plone.app.blob.interfaces import IBlobWrapper
    portal = context.portal_url.getPortalObject()
    ctool  = getToolByName(portal, 'portal_catalog')
    items = ctool(object_provides=ILeadImageable.__identifier__) 
    cnt = len(items)
    logger.info('Migrating %d items' % cnt)
    for item in items:
        obj = item.getObject()
        field = obj.getField(IMAGE_FIELD_NAME)
        if (field is not None) and not IBlobWrapper.providedBy(field.getUnwrapped(obj)):
            # this is apparently old content. AttributeError is raised 
            # when old site is upgraded to BLOB aware one
            # Let's migrate
            logger.info('Migrating item %s' % '/'.join(obj.getPhysicalPath()))
            extender = LeadImageExtender(obj)
            if extender.fields:
                extfield = extender.fields[0]
                if extfield.getName() == IMAGE_FIELD_NAME:
                    # ok, retrieve the value
                    value = extfield.get(obj)
                    field.set(obj, value)
    logger.info('Migration finished')
                    

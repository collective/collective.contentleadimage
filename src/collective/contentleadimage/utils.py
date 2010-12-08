from collective.contentleadimage.interfaces import ILeadImageable
from collective.contentleadimage.config import IMAGE_FIELD_NAME

from plone.indexer import indexer
from zope.component import provideAdapter

@indexer(ILeadImageable)
def hasContentLeadImage(obj):
    field = obj.getField(IMAGE_FIELD_NAME)
    if field is not None:
        value = field.get(obj)
        return not not value
provideAdapter(hasContentLeadImage, name='hasContentLeadImage')


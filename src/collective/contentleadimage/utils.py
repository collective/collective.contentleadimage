from Acquisition import aq_inner
from zope.component import getUtility
from zope.component import provideAdapter
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.indexer import indexer

from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.config import IMAGE_ALT_FIELD_NAME
from collective.contentleadimage.config import IMAGE_CAPTION_FIELD_NAME
from collective.contentleadimage.interfaces import ILeadImageable
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm


def content_lead_image_tag(obj, css_class='tileImage'):
    portal = getUtility(IPloneSiteRoot)
    prefs = ILeadImagePrefsForm(portal)
    context = aq_inner(obj)
    field = context.getField(IMAGE_FIELD_NAME)
    altf = context.getField(IMAGE_ALT_FIELD_NAME)
    titlef = context.getField(IMAGE_CAPTION_FIELD_NAME)
    alt = None
    title = None
    if altf is not None:
        alt = altf.get(context)
    if titlef is not None:
        title = titlef.get(context)
    tag = ''
    if field is not None:
        if field.get_size(context) != 0:
            scale = prefs.desc_scale_name
            if title:
                tag = field.tag(context,
                                scale=scale,
                                css_class=css_class,
                                alt=alt,
                                title=title)
            else:
                tag = field.tag(context,
                                scale=scale,
                                css_class=css_class,
                                alt=alt)
    return tag


@indexer(ILeadImageable)
def hasContentLeadImage(obj):
    field = obj.getField(IMAGE_FIELD_NAME)
    if field is not None:
        value = field.get(obj)
        return not not value
    else:
        raise AttributeError
provideAdapter(hasContentLeadImage, name='hasContentLeadImage')


@indexer(ILeadImageable)
def contentLeadImageTag(obj):
    field = obj.getField(IMAGE_FIELD_NAME)
    if field is not None:
        image = field.get(obj)
        if image:
            tag = content_lead_image_tag(obj)
            return tag
    else:
        raise AttributeError
provideAdapter(contentLeadImageTag, name='contentLeadImageTag')

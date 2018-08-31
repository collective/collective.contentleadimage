from Acquisition import aq_inner
from zope.component import getUtility
from zope.component import provideAdapter
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.indexer import indexer

from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.config import IMAGE_ALT_FIELD_NAME
from collective.contentleadimage.interfaces import ILeadImageable
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm


def content_lead_image_tag(obj, scale=None, css_class='tileImage'):
    """Never include title attribute, per WCAG"""
    portal = getUtility(IPloneSiteRoot)
    prefs = ILeadImagePrefsForm(portal)
    context = aq_inner(obj)
    field = context.getField(IMAGE_FIELD_NAME)
    altf = context.getField(IMAGE_ALT_FIELD_NAME)
    alt = None
    if altf is not None:
        alt = altf.get(context)
    tag = ''
    if field is not None:
        if field.get_size(context) != 0:
            if not scale:
                scale = prefs.desc_scale_name
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
def contentLeadImageAltText(obj):
    alt = None
    field = obj.getField(IMAGE_ALT_FIELD_NAME)
    if field is not None:
        alt = field.get(obj)
        return alt
    else:
        raise AttributeError
provideAdapter(contentLeadImageAltText, name='contentLeadImageAltText')

from Acquisition import aq_inner
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.layout.viewlets import ViewletBase
from zope.component import getUtility

from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.config import IMAGE_CAPTION_FIELD_NAME
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm


class LeadImageViewlet(ViewletBase):
    """ A simple viewlet which renders leadimage """

    def __init__(self, *args, **kwargs):
        super(LeadImageViewlet, self).__init__(*args, **kwargs)
        self.image_field_name = IMAGE_FIELD_NAME
        self.image_caption_field_name = IMAGE_CAPTION_FIELD_NAME

    @property
    def prefs(self):
        portal = getUtility(IPloneSiteRoot)
        return ILeadImagePrefsForm(portal)

    def bodyTag(self, css_class='newsImage'):
        """ returns img tag """
        context = aq_inner(self.context)
        field = context.getField(IMAGE_FIELD_NAME)
        if field is not None and field.get_size(context) != 0:
            scale = self.prefs.body_scale_name
            return field.tag(context, scale=scale, css_class=css_class)
        return ''

    def descTag(self, css_class='tileImage'):
        """ returns img tag """
        context = aq_inner(self.context)
        field = context.getField(IMAGE_FIELD_NAME)
        if field is not None and field.get_size(context) != 0:
            scale = self.prefs.desc_scale_name
            return field.tag(context, scale=scale, css_class=css_class)
        return ''

    def hasCaption(self):
        context = aq_inner(self.context)
        field = context.getField(IMAGE_CAPTION_FIELD_NAME)
        return field.get_size(self.context) != 0

    def caption(self):
        context = aq_inner(self.context)
        return context.widget(IMAGE_CAPTION_FIELD_NAME, mode='view')

    def render(self):
        context = aq_inner(self.context)
        portal_type = getattr(context, 'portal_type', None)
        if portal_type in self.prefs.allowed_types:
            return super(LeadImageViewlet, self).render()
        else:
            return ''

from Acquisition import aq_inner
from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.app.layout.viewlets import ViewletBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.config import IMAGE_CAPTION_FIELD_NAME
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm

class LeadImageViewlet(ViewletBase):
    """ A simple viewlet which renders leadimage """

    @property
    def prefs(self):
        portal = getUtility(IPloneSiteRoot)
        return ILeadImagePrefsForm(portal)

    def bodyTag(self, css_class='newsImage'):
        """ returns img tag """
        context = aq_inner(self.context)
        field = context.getField(IMAGE_FIELD_NAME)
        if field is not None and \
          field.getFilename(context) is not None and \
            field.get_size(context) != 0:
                scale = self.prefs.body_scale_name
                return field.tag(context, scale=scale, css_class=css_class)
        return ''

    def descTag(self, css_class='tileImage'):
        """ returns img tag """
        context = aq_inner(self.context)
        field = context.getField(IMAGE_FIELD_NAME)
        if field is not None and \
          field.getFilename(context) is not None and \
            field.get_size(context) != 0:
                scale = self.prefs.desc_scale_name
                return field.tag(context, scale=scale, css_class=css_class)
        return ''

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

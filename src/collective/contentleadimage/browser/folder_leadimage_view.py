from Acquisition import aq_inner
from zope.component import getUtility
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.config import IMAGE_ALT_FIELD_NAME
from collective.contentleadimage.config import IMAGE_CAPTION_FIELD_NAME
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm


class FolderLeadImageView(BrowserView):

    template = ViewPageTemplateFile('folder_leadimage_view.pt')

    @property
    def prefs(self):
        portal = getUtility(IPloneSiteRoot)
        return ILeadImagePrefsForm(portal)

    def tag(self, obj, css_class='tileImage'):
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
        if field is not None:
            if field.get_size(context) != 0:
                scale = self.prefs.desc_scale_name
                return field.tag(context,
                                 scale=scale,
                                 css_class=css_class,
                                 alt=alt,
                                 title=title)
        return ''

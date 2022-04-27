from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.contentleadimage.utils import content_lead_image_tag


class FolderLeadImageView(BrowserView):

    template = ViewPageTemplateFile('folder_leadimage_view.pt')

    def tag(self, obj, css_class='tileImage'):
        return content_lead_image_tag(obj, css_class=css_class)

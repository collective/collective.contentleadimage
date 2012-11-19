from collective.contentleadimage.config import IMAGE_FIELD_NAME


class LeadImagePurge(object):

    def __init__(self, context):
        self.context = context

    def getRelativeUrls(self):
        """Return a list of relative URLs that should be purged.

        URLs returned by this list will be rewritten based on the
        CacheSetup proxy configuration.
        """
        context = self.context
        field = context.getField(IMAGE_FIELD_NAME)

        urls = []
        if field:

            path_parts = context.getPhysicalPath()
            if tuple(path_parts[:1]) == ("",):
                # remove leading blank part to prevent returning a non relitave url
                path_parts = path_parts[1:]

            url = '/'.join(path_parts)
            scalenames = field.getAvailableSizes(context)
            urls = ['%s/%s'%(url, IMAGE_FIELD_NAME)]+['%s/%s_'%(url, IMAGE_FIELD_NAME) + s for s in scalenames]

        return urls

    def getAbsoluteUrls(self, relative_urls):
        """Return a list of absolute URLs that should be purged.

        URLs returned by this list will not be rewritten and passed
        as-is to the proxy server(s).

        The list of relative URLs is passed in and should not be modified.
        """
        return []

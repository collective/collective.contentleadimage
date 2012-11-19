from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getUtility
from zope.schema.vocabulary import SimpleTerm
try:
    from plone.app.imaging.utils import getAllowedSizes
    getAllowedSizes  # pyflakes
except ImportError:
    getAllowedSizes = lambda: dict()

from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm
from collective.contentleadimage import config


class ScalesVocabulary(object):
    """ """

    def __call__(self, context):
        portal = getUtility(IPloneSiteRoot)
        cli_prefs = ILeadImagePrefsForm(portal)
        width = cli_prefs.image_width
        height = cli_prefs.image_height
        scale = config.IMAGE_SCALE_NAME
        result = [SimpleTerm(scale, scale, "%s (%dx%d)" % (scale, width, height)), ]

        for scale, (width, height) in config.IMAGE_SIZES.items():
            result.append(SimpleTerm(scale, scale, "%s (%dx%d)" % (
                scale, width, height)))

        return SimpleVocabulary(result)


class  PloneAppImagingScalesVocabulary(object):
    """Obtains available scales from plone.app.imaging
    """

    def __call__(self, context):
        terms = []
        for scale, (width, height) in getAllowedSizes().iteritems():
            terms.append(SimpleTerm(scale, scale, "%s (%dx%d)" % (
                scale, width, height)))

        return SimpleVocabulary(terms)

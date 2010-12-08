from Products.Archetypes.public import ImageField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from Products.Archetypes.public import ImageWidget
from Products.Archetypes.public import AnnotationStorage
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.ATContentTypes.configuration import zconf

from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.http import IHTTPRequest
from ZPublisher.BaseRequest import DefaultPublishTraverse
from Products.validation import V_REQUIRED


from collective.contentleadimage.interfaces import ILeadImageable
from collective.contentleadimage.interfaces import ILeadImageSpecific
from collective.contentleadimage import LeadImageMessageFactory as _
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.config import IMAGE_CAPTION_FIELD_NAME
from collective.contentleadimage.config import IMAGE_SIZES
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm
try:
    from plone.app.blob.field import ImageField as BlobImageField
    HAS_BLOB = True
except ImportError:
    HAS_BLOB = False

class LeadimageCaptionField(ExtensionField, StringField):
    """ A trivial string field """


class LeadimageImageField(ExtensionField, ImageField):
    """A Image field. """

    @property
    def sizes(self):
        # This property is not used in Plone 4 !
        # XXX it's still used in plone4 and thus overrides plone.app.imaging settings
        portal = getUtility(IPloneSiteRoot)
        cli_prefs = ILeadImagePrefsForm(portal)
        sizes = IMAGE_SIZES.copy()
        sizes['leadimage'] = (cli_prefs.image_width, cli_prefs.image_height)
        return sizes

if HAS_BLOB:
    class LeadimageBlobImageField(ExtensionField, BlobImageField):
        """Image Field with blob support that uses sizes defined in plone.app.imaging
        """
        pass

captionField = LeadimageCaptionField(IMAGE_CAPTION_FIELD_NAME,
        required=False,
        searchable=False,
        storage = AnnotationStorage(),
        languageIndependent = False,
        widget = StringWidget(
                    label=_(u"Lead image caption"),
                    description=_(u"You may enter lead image caption text"),
                ),
    )

class LeadImageExtender(object):
    adapts(ILeadImageable)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)

    layer = ILeadImageSpecific



    fields = [
        LeadimageImageField(IMAGE_FIELD_NAME,
          required = False,
          storage = AnnotationStorage(migrate=True),
          languageIndependent = True,
          max_size = zconf.ATNewsItem.max_image_dimension,
          swallowResizeExceptions = zconf.swallowImageResizeExceptions.enable,
          pil_quality = zconf.pil_config.quality,
          pil_resize_algo = zconf.pil_config.resize_algo,
          validators = (('isNonEmptyFile', V_REQUIRED),
                               ('checkNewsImageMaxSize', V_REQUIRED)),
          widget = ImageWidget(
                         label=_(u"Lead image"),
                         description=_(u"You can upload lead image. This image "
                                       u"will be displayed above the content. "
                                       u"Uploaded image will be automatically "
                                       u"scaled to size specified in the leadimage "
                                       u"control panel."),
                         show_content_type=False,
                 ),
        ),

        captionField,

        ]

    def __init__(self, context):
         self.context = context

    def getFields(self):
        portal = getUtility(IPloneSiteRoot)
        cli_prefs = ILeadImagePrefsForm(portal)
        if cli_prefs.cli_props is not None:
            portal_type = getattr(self.context, 'portal_type', None)
            if portal_type in cli_prefs.allowed_types:
                return self.fields
        return []

    def getOrder(self, original):
        """
        'original' is a dictionary where the keys are the names of
        schemata and the values are lists of field names, in order.

        Move leadImage field just after the Description
        """
        default = original.get('default', None)
        if default:
            desc_index = 0
            # if there is no title nor description field, do nothing
            if 'description' in default:
                desc_index = default.index('description')
            elif 'title' in default:
                desc_index = default.index('title')
            if desc_index >= 0 and (IMAGE_FIELD_NAME in default):
                default.remove(IMAGE_FIELD_NAME)
                default.insert(desc_index+1, IMAGE_FIELD_NAME)
                if IMAGE_CAPTION_FIELD_NAME in default:
                    default.remove(IMAGE_CAPTION_FIELD_NAME)
                    default.insert(desc_index+2, IMAGE_CAPTION_FIELD_NAME)
        return original

if HAS_BLOB:
    class LeadImageBlobExtender(LeadImageExtender):

        fields = [
            LeadimageBlobImageField(IMAGE_FIELD_NAME,
                required = False,
                storage = AnnotationStorage(migrate=True),
                languageIndependent = False,
                max_size = zconf.ATNewsItem.max_image_dimension,
                swallowResizeExceptions = zconf.swallowImageResizeExceptions.enable,
                pil_quality = zconf.pil_config.quality,
                pil_resize_algo = zconf.pil_config.resize_algo,
                validators = (('isNonEmptyFile', V_REQUIRED),
                              ('checkNewsImageMaxSize', V_REQUIRED)),
                widget = ImageWidget(
                           label=_(u"Lead image"),
                           description=_(u"You can upload lead image. This image "
                                         u"will be displayed above the content. "
                                         u"Uploaded image will be automatically "
                                         u"scaled to size specified in the leadimage "
                                         u"control panel."),
                           show_content_type=False,
                   ),
            ),

            captionField,

            ]



class LeadImageTraverse(DefaultPublishTraverse):
    implements(IPublishTraverse)
    adapts(ILeadImageable, IHTTPRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        if name.startswith(IMAGE_FIELD_NAME):
            field = self.context.getField(IMAGE_FIELD_NAME)
            if field is not None:
                image = None
                if name == IMAGE_FIELD_NAME:
                    image = field.getScale(self.context)
                else:
                    scalename = name[len(IMAGE_FIELD_NAME + '_'):]
                    if scalename in field.getAvailableSizes(self.context):
                        image = field.getScale(self.context, scale=scalename)
                if image is not None and not isinstance(image, basestring):
                    # image might be None or '' for empty images
                    return image

        return super(LeadImageTraverse, self).publishTraverse(request, name)

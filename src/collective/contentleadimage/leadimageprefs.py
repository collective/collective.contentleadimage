from zope.interface import Interface, implements
from zope.component import adapts
from zope.component import getUtility
from zope.component import getMultiAdapter

from zope.formlib import form
from zope import schema
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.interfaces import IPropertiesTool
from Products.CMFCore.utils import getToolByName
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.validators import null_validator

from Products.statusmessages.interfaces import IStatusMessage
from plone.protect import CheckAuthenticator
from zope.event import notify
from plone.app.controlpanel.events import ConfigurationChangedEvent

from Products.CMFPlone import PloneMessageFactory as _p
from collective.contentleadimage import LeadImageMessageFactory as _
from collective.contentleadimage.interfaces import ILeadImageable
from collective.contentleadimage import config
from ZODB.POSException import ConflictError

try:
    from plone.app.imaging.utils import getAllowedSizes
except ImportError:
    getAllowedSizes = lambda: dict()


class ILeadImagePrefsForm(Interface):    
    """ The view for LeadImage  prefs form. """

    allowed_types = schema.Tuple(title=_(u'Portal types'),
                          description=_(u'Portal types lead image may be attached to.'),
                          missing_value=tuple(),
                          value_type=schema.Choice(
                                   vocabulary="plone.app.vocabularies.UserFriendlyTypes"),
                          required=False)
    
    image_width = schema.Int(title=_(u'Width'),
                       description=_(u'Lead image scale width. Value specified in this field '
                                     u"is used for generating 'leadimage' scale"),
                       default=67,
                       required=True)

    image_height = schema.Int(title=_(u'Height'),
                       description=_(u'Lead image scale height. Value specified in this field '
                                     u"is used for generating 'leadimage' scale"),
                       default=81,
                       required=True)

    desc_scale_name = schema.Choice(title=_(u"'Description' image scale"),
                               description=_(u'Please select scale which will be used next to Description field.'),
                               required=True,
                               default='thumb',
                               vocabulary = u"collective.contentleadimage.scales_vocabulary",
                        )

    body_scale_name = schema.Choice(title=_(u"'Body' image scale"),
                               description=_(u'Please select scale which will be used in the body.'),
                               required=True,
                               default='mini',
                               vocabulary = u"collective.contentleadimage.scales_vocabulary",
                        )

    viewlet_description = schema.Bool(title=_(u'Show image next to Description field'),
                                  default=True,
                          )

    viewlet_body        = schema.Bool(title=_(u'Show image in body area'),
                                  default=False,
                          )


class LeadImageControlPanelAdapter(SchemaAdapterBase):
    """ Control Panel adapter """

    adapts(IPloneSiteRoot)
    implements(ILeadImagePrefsForm)
    
    def __init__(self, context):
        super(LeadImageControlPanelAdapter, self).__init__(context)
        pprop = getUtility(IPropertiesTool)
        self.cli_props = getattr(pprop, 'cli_properties', None)
        self.imaging_props = getattr(pprop, 'imaging_properties', None)
        self.context = context

    def viewletVisible(self, manager, viewlet):
        storage = getUtility(IViewletSettingsStorage)
        skinname = self.context.getCurrentSkinName()
        hidden = storage.getHidden(manager, skinname)
        return viewlet not in hidden

    def setViewletVisibility(self, manager, viewlet, visible):
        storage = getUtility(IViewletSettingsStorage)
        skinname = self.context.getCurrentSkinName()
        hidden = storage.getHidden(manager, skinname)
        if visible:
            # viewlet should be visible
            if viewlet in hidden:
                hidden = tuple(x for x in hidden if x != viewlet)
        else:
            # hide viewlet
            if viewlet not in hidden:
                hidden = hidden + (viewlet,)
        storage.setHidden(manager, skinname, hidden)
        # hide viewlet in default skin as well
        default = storage.getDefault(manager)
        if (default is not None) and default != skinname:
            storage.setHidden(manager, default, hidden)

    def _change_imaging_props(self, w, h):
        if self.imaging_props is not None:
            sizes = self.imaging_props.allowed_sizes
            new_sizes = []
            for row in sizes:
                if row.startswith(config.IMAGE_SCALE_NAME+' '):
                    new_sizes.append(config.IMAGE_SCALE_NAME + ' %s:%s' % (w, h))
                else:
                    new_sizes.append(row)
            self.imaging_props.allowed_sizes = new_sizes

    def get_image_height(self):
        if self.imaging_props is not None:
            # get from plone.app.imaging properties
            size = getAllowedSizes().get(config.IMAGE_SCALE_NAME, None)
            if size is not None:
                return int(size[1])  # height
        # fallback (Plone 3 or wrong configuration)
        return self.cli_props.image_height

    def set_image_height(self, image_height):
        if self.imaging_props is not None:
            # we have plone.app.imaging - store the size to imaging_properties
            sizes = getAllowedSizes()
            if config.IMAGE_SCALE_NAME in sizes.keys():
                w, h = sizes[config.IMAGE_SCALE_NAME]
                h = image_height
                self._change_imaging_props(w, h)
        # store the size to cli_properties in any case
        self.cli_props.image_height = image_height
    
    def get_image_width(self):
        if self.imaging_props is not None:
            # get from plone.app.imaging properties
            size = getAllowedSizes().get(config.IMAGE_SCALE_NAME, None)
            if size is not None:
                return int(size[0])  # height
        # fallback (Plone 3 or wrong configuration)
        return self.cli_props.image_width

    def set_image_width(self, image_width):
        if self.imaging_props is not None:
            # we have plone.app.imaging - store the size to imaging_properties
            sizes = getAllowedSizes()
            if config.IMAGE_SCALE_NAME in sizes.keys():
                w, h = sizes[config.IMAGE_SCALE_NAME]
                w = image_width
                self._change_imaging_props(w, h)
        # store the size to cli_properties in any case
        self.cli_props.image_width = image_width
    
    def get_viewlet_description(self):
        manager = 'plone.belowcontenttitle'
        viewlet = 'collective.contentleadimage.thumbnail'
        return self.viewletVisible(manager, viewlet)

    def set_viewlet_description(self, value):
        manager = 'plone.belowcontenttitle'
        viewlet = 'collective.contentleadimage.thumbnail'
        self.setViewletVisibility(manager, viewlet, value)
        
    def get_viewlet_body(self):
        manager = 'plone.abovecontentbody'
        viewlet = 'collective.contentleadimage.full'
        return self.viewletVisible(manager, viewlet)

    def set_viewlet_body(self, value):
        manager = 'plone.abovecontentbody'
        viewlet = 'collective.contentleadimage.full'
        self.setViewletVisibility(manager, viewlet, value)
        
    def get_allowed_types(self):
        return self.cli_props.allowed_types
        
    def set_allowed_types(self, allowed_types):
        self.cli_props.allowed_types = allowed_types
        
    def get_desc_scale_name(self):
        return self.cli_props.desc_scale_name
        
    def set_desc_scale_name(self, value):
        self.cli_props.desc_scale_name = value
        
    def get_body_scale_name(self):
        return self.cli_props.body_scale_name
    
    def set_body_scale_name(self, value):
        self.cli_props.body_scale_name = value

    image_height  = property(get_image_height, set_image_height)
    image_width   = property(get_image_width, set_image_width)
    viewlet_description  = property(get_viewlet_description, set_viewlet_description)
    viewlet_body  = property(get_viewlet_body, set_viewlet_body)
    allowed_types = property(get_allowed_types, set_allowed_types)
    desc_scale_name = property(get_desc_scale_name, set_desc_scale_name)
    body_scale_name = property(get_body_scale_name, set_body_scale_name)

    
class LeadImagePrefsForm(ControlPanelForm):
    """ The view class for the lead image preferences form. """

    implements(ILeadImagePrefsForm)
    form_fields = form.FormFields(ILeadImagePrefsForm)

    label = _(u'Content Lead Image Settings Form')
    description = _(u'Select properties for Content Lead Image')
    form_name = _(u'Content Lead Image Settings')
            
    # handle_edit_action and handle_cancel_action are copied from 
    # ControlPanelForm because they are overriden by my handle_scales_action
    @form.action(_p(u'label_save', default=u'Save'), name=u'save')
    def handle_edit_action(self, action, data):
        CheckAuthenticator(self.request)
        if form.applyChanges(self.context, self.form_fields, data,
                             self.adapters):
            self.status = _p("Changes saved.")
            notify(ConfigurationChangedEvent(self, data))
            self._on_save(data)
        else:
            self.status = _p("No changes made.")

    @form.action(_p(u'label_cancel', default=u'Cancel'),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        IStatusMessage(self.request).addStatusMessage(_p("Changes canceled."),
                                                      type="info")
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url + '/plone_control_panel')
        return ''
            
    @form.action(_(u'label_recreate_scales', default=u'Recreate scales'), name=u'scales', validator=null_validator)
    def handle_scales_action(self, action, data):
        CheckAuthenticator(self.request)
        number = 0
        ctool = getToolByName(self.context, 'portal_catalog')
        items = ctool(hasContentLeadImage=True)
        for i in items:
            obj = i.getObject()
            if obj is None:
                continue
            if not ILeadImageable.providedBy(obj):
                continue

            try:
                state = obj._p_changed
            except (ConflictError, KeyboardInterrupt):
                raise
            except:
                state = 0

            field = obj.getField(config.IMAGE_FIELD_NAME)
            if field is not None:
                field.removeScales(obj)
                field.createScales(obj)
                number = number + 1

            if state is None:
                obj._p_deactivate()

        self.status = _(u"text_scales_recreated", default=u"${number} scales recreated.", mapping={'number':number})

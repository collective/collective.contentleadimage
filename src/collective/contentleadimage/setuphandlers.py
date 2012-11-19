from Products.CMFCore.utils import getToolByName
from collective.contentleadimage import config
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm


def setupCatalog(portal, indexes=dict(), metadata=list()):
    catalog = getToolByName(portal, 'portal_catalog')

    idxs = catalog.indexes()
    mtds = catalog.schema()

    for index in indexes.keys():
        if index not in idxs:
            catalog.addIndex(index, indexes[index])

    for mt in metadata:
        if mt not in mtds:
            catalog.addColumn(mt)


def importVarious(self):
    if self.readDataFile('contentleadimage.txt') is None:
        return

    portal = self.getSite()
    ptool = getToolByName(portal, 'portal_properties')
    props = ptool.cli_properties

    if not props.hasProperty('image_width'):
        props.manage_addProperty('image_width', config.IMAGE_SCALE_SIZE[0], 'int')
    if not props.hasProperty('image_height'):
        props.manage_addProperty('image_height', config.IMAGE_SCALE_SIZE[1], 'int')
    if not props.hasProperty('desc_scale_name'):
        props.manage_addProperty('desc_scale_name', 'thumb', 'string')
    if not props.hasProperty('body_scale_name'):
        props.manage_addProperty('body_scale_name', 'mini', 'string')

    setupCatalog(portal, indexes=dict(hasContentLeadImage='FieldIndex'),
                 metadata=['hasContentLeadImage'])

    prefs = ILeadImagePrefsForm(portal)
    prefs.viewlet_description = False


def removeConfiglet(self):
    if self.readDataFile('cli-uninstall.txt') is None:
        return
    portal_conf = getToolByName(self.getSite(), 'portal_controlpanel')
    portal_conf.unregisterConfiglet('ContentLeadImage')

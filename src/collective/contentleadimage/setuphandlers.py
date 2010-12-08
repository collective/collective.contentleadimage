from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPropertiesTool
from Products.ZCatalog.ProgressHandler import ZLogHandler
from collective.contentleadimage import config

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
        
    ctool = getToolByName(portal, 'portal_catalog')
    ctool.reindexIndex(['hasContentLeadImage'], portal.REQUEST, pghandler=ZLogHandler())
    
def removeConfiglet(self):
    if self.readDataFile('cli-uninstall.txt') is None:
        return
    portal_conf=getToolByName(self.getSite(),'portal_controlpanel')
    portal_conf.unregisterConfiglet('ContentLeadImage')
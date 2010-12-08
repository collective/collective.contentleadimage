from zope import schema
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

from collective.contentleadimage import LeadImageMessageFactory as _


class ILeadImageSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """

class ILeadImageable(Interface):
    """ marker interface """
    
class IFolderLeadSummaryView(Interface):
    
    def getLeadImageTag(obj):
        """ generate the tag """
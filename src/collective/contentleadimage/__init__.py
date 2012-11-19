from zope.i18n import MessageFactory
LeadImageMessageFactory = MessageFactory('collective.contentleadimage')

# import utils to register indexable attribute
import utils
utils  # pyflakes


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

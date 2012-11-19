from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import quickInstallProduct

from plone.testing import z2


class CollectiveContentLeadImageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.contentleadimage
        self.loadZCML(package=collective.contentleadimage)
        z2.installProduct(app, 'collective.contentleadimage')

    def setUpPloneSite(self, portal):
        quickInstallProduct(portal, 'collective.contentleadimage')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'collective.contentleadimage')


COLLECTIVE_CONTENTLEADIMAGE_FIXTURE = CollectiveContentLeadImageLayer()
COLLECTIVE_CONTENTLEADIMAGE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CONTENTLEADIMAGE_FIXTURE,),
    name="CollectiveContentLeadImage:Integration")
COLLECTIVE_CONTENTLEADIMAGE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CONTENTLEADIMAGE_FIXTURE,),
    name="CollectiveContentLeadImageLayer:Functional")

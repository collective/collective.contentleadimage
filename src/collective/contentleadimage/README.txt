collective.contentleadimage Package Readme
==========================================

Overview
--------

This products adds complete support for adding descriptive image to any Archetypes based
content in Plone site. Each object has new tab "Edit lead image", which allows to upload
new or remove current image. It is similar behaviour as Plone News Item (you can add image
to news item and this image is displayed in news item overview listing.

There is folder_leadimage_view page template, which can be used to list all items in the folder
together with images attached.

There is configuration control panel, where you can set maximum width and height of the uploaded
images. The widht and height is applied on each image upload (image is automatically resized).

There is FieldIndex and metadata in portal_catalog: hasContentLeadImage (True/False).

Tests of the package

    >>> import os
    >>> import PIL
    >>> import os
    >>> from StringIO import StringIO
    >>> from Products.CMFCore.utils import getToolByName
    >>> from collective.contentleadimage.interfaces import ILeadImageable
    >>> from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm
    >>> from collective.contentleadimage.config import IMAGE_FIELD_NAME
    >>> current_file = globals()['__file__']
    >>> tests_dir, _ = os.path.split(current_file)
    >>> tests_dir = os.path.join(tests_dir, 'tests')
    >>> portal_setup = getToolByName(self.portal, 'portal_setup')
    >>> _ = portal_setup.runAllImportStepsFromProfile('profile-collective.contentleadimage:default')

    Test types which are allowed to be attached with lead image
    By default, only Document and Folder are allowed

    >>> _ = self.folder.invokeFactory('Document', 'docA')
    >>> self.folder.docA.getField(IMAGE_FIELD_NAME) is None
    False
    >>> self.folder.getField(IMAGE_FIELD_NAME) is None
    False
    >>> _ = self.folder.invokeFactory('File', 'fileA')
    >>> self.folder.fileA.getField(IMAGE_FIELD_NAME) is None
    True
    >>> _ = self.folder.invokeFactory('Link', 'linkA')
    >>> self.folder.linkA.getField(IMAGE_FIELD_NAME) is None
    True

    >>> self.loginAsPortalOwner()
    >>> prefs = ILeadImagePrefsForm(self.portal)
    >>> types = list(prefs.allowed_types)
    >>> types.append('Link')
    >>> prefs.allowed_types = types
    >>> self.logout()
    >>> self.login()

    >>> _ = self.folder.invokeFactory('Link', 'linkB')
    >>> self.folder.linkA.getField(IMAGE_FIELD_NAME) is None
    False

    >>> _ = self.folder.invokeFactory('Document', 'doc1')
    >>> doc = self.folder['doc1']
    >>> doc.update(title='The Document')
    >>> doc.processForm()

    >>> ILeadImageable.providedBy(doc)
    True

    >>> test_image = os.path.join(tests_dir, 'test_41x41.jpg')
    >>> raw_image = open(test_image, 'rb').read()

    >>> field = doc.getField(IMAGE_FIELD_NAME)
    >>> field
    <Field leadImage(blob:rw)>
    >>> field.set(doc, raw_image)
    >>> stored = field.get(doc)

    Got OFS.OFS.Image object

    By default, image max size is 640x480 px

    >>> image = PIL.Image.open(StringIO(stored.data))
    >>> image.size
    (41, 41)

    Set another size of the image

    >>> self.loginAsPortalOwner()
    >>> prefs = ILeadImagePrefsForm(self.portal)
    >>> prefs.image_height = 20
    >>> prefs.image_width  = 20
    >>> self.logout()
    >>> self.login()

    And store image again

    >>> field.set(doc, raw_image)
    >>> image = PIL.Image.open(StringIO(field.get(doc).data))
    >>> image.size
    (41, 41)
    >>> image = PIL.Image.open(StringIO(field.getScale(doc, 'leadimage').data))
    >>> image.size
    (20, 20)
    >>> image = PIL.Image.open(StringIO(field.getScale(doc, 'mini').data))
    >>> image.size
    (41, 41)
    >>> image = PIL.Image.open(StringIO(field.getScale(doc, 'listing').data))
    >>> image.size
    (16, 16)

    Finally remove the image

    >>> field.set(doc, 'DELETE_IMAGE')
    >>> not not field.get(doc)
    False


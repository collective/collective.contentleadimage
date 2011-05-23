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
images. The width and height is applied on each image upload (image is automatically resized).

There is FieldIndex and metadata in portal_catalog: hasContentLeadImage (True/False).

Tests of the package
--------------------

Set up our test browser instance, and log into the portal as an admin.

    >>> import StringIO
    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> browser.handleErrors = False
    >>> portal_url = self.portal.absolute_url()
    >>> login_url = portal_url + '/login_form'
    >>> self.portal.error_log._ignored_exceptions = ()
    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> browser.open(login_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> "You are now logged in" in browser.contents
    True

Set up the rest of the boilerplate for tests.

    >>> import os
    >>> import PIL
    >>> import os
    >>> from StringIO import StringIO
    >>> from Products.CMFCore.utils import getToolByName
    >>> from collective.contentleadimage.interfaces import ILeadImageable
    >>> from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm
    >>> from collective.contentleadimage.config import IMAGE_FIELD_NAME
    >>> from collective.contentleadimage.config import IMAGE_CAPTION_FIELD_NAME
    >>> from collective.contentleadimage.extender import HAS_BLOB
    >>> current_file = globals()['__file__']
    >>> tests_dir, _ = os.path.split(current_file)
    >>> tests_dir = os.path.join(tests_dir, 'tests')
    >>> portal_setup = getToolByName(self.portal, 'portal_setup')
    >>> _ = portal_setup.runAllImportStepsFromProfile('profile-collective.contentleadimage:default')

Allowed types
~~~~~~~~~~~~~

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

Login into the portal and add 'Link' to the allowed types list.

    >>> self.loginAsPortalOwner()
    >>> prefs = ILeadImagePrefsForm(self.portal)
    >>> types = list(prefs.allowed_types)
    >>> types.append('Link')
    >>> prefs.allowed_types = types
    >>> self.logout()
    >>> self.login()

Create an example 'Link' content item to check this worked.

    >>> _ = self.folder.invokeFactory('Link', 'linkB')
    >>> self.folder.linkA.getField(IMAGE_FIELD_NAME) is None
    False

Create an example 'Document' content item to apply our lead image to.

    >>> _ = self.folder.invokeFactory('Document', 'doc1')
    >>> doc = self.folder['doc1']
    >>> doc.update(title='The Document')
    >>> doc.processForm()

Applying lead images
~~~~~~~~~~~~~~~~~~~~

Check that we can apply lead images to our newly created content.

    >>> ILeadImageable.providedBy(doc)
    True

Firstly, let's check to make sure that the lead image field isn't being
displayed, since we don't have a lead image applied yet.

    >>> browser.open(doc.absolute_url())
    >>> IMAGE_FIELD_NAME in browser.contents
    False

Read in our example lead image and apply it to the field on the content.

    >>> test_image = os.path.join(tests_dir, 'test_41x41.jpg')
    >>> raw_image = open(test_image, 'rb').read()

    >>> field = doc.getField(IMAGE_FIELD_NAME)
    >>> field.type == 'image'
    True
    >>> field.set(doc, raw_image)
    >>> doc.reindexObject()
    >>> doc.reindexObject(idxs=['hasContentLeadImage'])

Check that our save was successful.  We should be able to see our image 
on the page now - only the body content lead image is currently visible.

    >>> browser.open(doc.absolute_url())
    >>> prefs = ILeadImagePrefsForm(self.portal)
    >>> LEADIMAGE_TAG = '<img src="%s/%s' % (doc.absolute_url(), \
    ...                                              IMAGE_FIELD_NAME)
    >>> DESC_LEADIMAGE_TAG = '%s_%s' % (LEADIMAGE_TAG, prefs.desc_scale_name)
    >>> BODY_LEADIMAGE_TAG = '%s_%s' % (LEADIMAGE_TAG, prefs.body_scale_name)
    >>> DESC_LEADIMAGE_TAG in browser.contents
    False
    >>> BODY_LEADIMAGE_TAG in browser.contents
    True 

We shouldn't see a caption container though, since we don't have a caption 
set at the moment.

    >>> IMAGE_CAPTION_FIELD_NAME in browser.contents
    False

By default, image max size is 640x480 px

    >>> stored = field.get(doc)
    >>> image = PIL.Image.open(StringIO(stored.data))
    >>> image.size
    (41, 41)

Set another size for lead images on the portal.

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

Lead image captioning
~~~~~~~~~~~~~~~~~~~~~

Now, check that we can work with a leadimage caption by setting one.

Let's start with checking our field actually exists and is of the correct
type.

    >>> caption_field = doc.getField(IMAGE_CAPTION_FIELD_NAME)
    >>> caption_field.type == 'string'
    True

Set an example caption to check that it gets set.

    >>> EXAMPLE_CAPTION = 'This is my leadimage caption!?'
    >>> caption_field.set(doc, EXAMPLE_CAPTION)
    >>> caption_stored = caption_field.get(doc)
    >>> caption_stored == EXAMPLE_CAPTION
    True

Now, check the render to make sure the caption would be on the page.

    >>> browser.open(doc.absolute_url())
    >>> IMAGE_CAPTION_FIELD_NAME in browser.contents
    True
    >>> EXAMPLE_CAPTION in browser.contents
    True

Changing lead image viewlet preferences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can also configure contentleadimage so that we can see a description
lead image, a body lead image, or both.  At present, we've just got the default
of body lead image turned on. 

Let's check our current state.
 
    >>> self.loginAsPortalOwner()
    >>> prefs = ILeadImagePrefsForm(self.portal)
    >>> prefs.viewlet_description
    False
    >>> prefs.viewlet_body
    True

We can change these options and see that our viewlets have changed.

    >>> prefs.viewlet_description = True
    >>> prefs.viewlet_description
    True
    >>> prefs.viewlet_body = False
    >>> prefs.viewlet_body
    False

and check the results in the browser.

    >>> browser.open(doc.absolute_url())
    >>> DESC_LEADIMAGE_TAG in browser.contents
    True
    >>> BODY_LEADIMAGE_TAG in browser.contents
    False

Or we can even turn off both and not see anything.

    >>> prefs.viewlet_description = False
    >>> prefs.viewlet_description
    False
    >>> prefs.viewlet_body = False
    >>> prefs.viewlet_body
    False

    >>> browser.open(doc.absolute_url())
    >>> DESC_LEADIMAGE_TAG in browser.contents
    False
    >>> BODY_LEADIMAGE_TAG in browser.contents
    False

Let's restore our original state to just have the body lead image present.

    >>> prefs.viewlet_body = True
    >>> prefs.viewlet_body
    True

    >>> browser.open(doc.absolute_url())
    >>> DESC_LEADIMAGE_TAG in browser.contents
    False
    >>> BODY_LEADIMAGE_TAG in browser.contents
    True

Reset our state of authentication on the portal.

    >>> self.logout()
    >>> self.login()


Removing a lead image
~~~~~~~~~~~~~~~~~~~~~

Finally, let's remove the image but leave the caption in place to check the
result.

    >>> field.set(doc, 'DELETE_IMAGE')
    >>> not not field.get(doc)
    False

We'll make doubly sure that our viewlet is actually still turned on.

    >>> prefs = ILeadImagePrefsForm(self.portal)
    >>> prefs.viewlet_body
    True

And we can see that it's now not visible on our page since no image exists.

    >>> browser.open(doc.absolute_url())
    >>> BODY_LEADIMAGE_TAG in browser.contents
    False

Our caption shouldn't be visible, either

    >>> IMAGE_CAPTION_FIELD_NAME in browser.contents
    False 
    >>> EXAMPLE_CAPTION in browser.contents
    False

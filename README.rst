collective.contentleadimage
============================

.. contents :: :local:

Overview
--------

.. image:: https://travis-ci.org/collective/collective.contentleadimage.svg?branch=master
    :target: https://travis-ci.org/collective/collective.contentleadimage

This products adds complete support for adding descriptive image to any
Archetypes based content in Plone site. Each object has new tab "Edit lead
image", which allows to upload new or remove current image. It is similar
behaviour as Plone News Item (you can add image to news item and this image is
displayed in news item overview listing.

There is folder_leadimage_view page template, which can be used to list all
items in the folder together with images attached.

There is configuration control panel, where you can set maximum width and height
of the uploaded images. The width and height is applied on each image upload
(image is automatically resized). You can specify smaller width and height
which is used as image preview in the below content title viewlet (next to
content Description). Large image is used in the above content body viewlet
(floated left at the top of content body).

Below content title viewlet is preffered, but Manager can easily switch
the viewlets on/off in the control panel.

There is FieldIndex and metadata in portal_catalog: hasContentLeadImage
(True/False). This may help developers to create own templates optimized
for displaying lead image.

**Note**: For Plone 4.4+ and plone.app.contenttypes based content
there is support for lead image behavior out of the box. This addon
is only compatible with legacy Archetypes based content.

Installation
------------

If you are using zc.buildout and the plone.recipe.zope2instance recipe to manage
your project, you can do this:

Add ``collective.contentleadimage`` to the list of eggs to install, e.g.::

    [buildout]
    ...
    eggs =
        ...
        collective.contentleadimage

Tell the plone.recipe.zope2instance recipe to install a ZCML slug::

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zcml =
        collective.contentleadimage

Re-run buildout, e.g. with::

    $ ./bin/buildout

More detailed installation instructions may be found in docs/INSTALL.txt.

Using collective.contentleadimage with plone.app.scaling
----------------------------------------------------------

`plone.app.imaging <http://plone.org/products/plone.app.imaging/>`_
provides dynamic image scales for all Plone images since Plone version 4.1.

Below is an example how to use ``@@images`` with with portal_catalog
``hasContentLeadImage`` metadata column to show a custom sized lead image scale
in a folder listing.

Example page template snippet from a folder listing::

   <div class="tileItem visualIEFloatFix"
                     tal:define="item_has_leadimage item/hasContentLeadImage;
                                       item_object item/getObject;
                                       item_hide_from_nav item/exclude_from_nav;
                                   "
                      tal:condition="not:item_hide_from_nav">

                        <img tal:condition="exists:item_has_leadimage"
                             tal:define="scale item_object/@@images; img python:scale.scale('leadImage', width=280, height=280)"
                             tal:replace="structure python: img.tag() if img else None" />

Here is another example how Event content type view template is modified to directly
display lead image next to the event details table.
The modification was done using ``z3c.jbot`` and overriding the template as ``Products.CMFPlone.skins.plone_content.event_view.pt``.

The template head::

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="plone">
    <body>

    <metal:content-core fill-slot="content-core">
        <metal:content-core define-macro="content-core"
                            tal:define="kssClassesView context/@@kss_field_decorator_view;
                                        getKssClasses nocall:kssClassesView/getKssClassesInlineEditable;
                                        templateId template/getId;
                                        toLocalizedTime nocall:context/@@plone/toLocalizedTime;">


            <tal:comment replace="nothing">
                <!-- Show content lead image above event details on the event page.

                Match image dimensions to the event details table size.
                -->
            </tal:comment>

            <div class="lead">

            <div class="lead-image-wrapper" tal:define="scale context/@@images; img python:scale.scale('leadImage', width=300, height=300)" tal:condition="img">
                <img tal:replace="structure python: img.tag() if img else None" />
            </div>


            <div class="eventDetails vcard">
                <table class="vertical listing"
                       summary="Event details" i18n:attributes="summary summary_event_details;">

                    <tbody>




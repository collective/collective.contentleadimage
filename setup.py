from setuptools import setup, find_packages

version = '1.3.6'

tests_require = ['plone.app.testing']

setup(name='collective.contentleadimage',
      version=version,
      description="Adds lead image to any content in plone site",
      long_description=(open("README.rst").read() + "\n\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
                  "Framework :: Plone",
                  "Framework :: Zope2",
                  "Framework :: Zope3",
                  "Programming Language :: Python",
                  "Topic :: Software Development :: Libraries :: Python Modules",
                  ],
      keywords='plone',
      author='Radim Novotny',
      author_email='novotny.radim@gmail.com',
      url='http://pypi.python.org/pypi/collective.contentleadimage',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'archetypes.schemaextender',
          'plone.browserlayer',
          'plone.indexer',
      ],
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

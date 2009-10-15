from setuptools import setup, find_packages
import os

version = '0.4'

install_requires=[
    'setuptools',
    'zope.interface',
    'zope.schema',
    'zope.annotation',
    'zope.traversing',
    'zope.app.pagetemplate',
    'grokcore.view',
    'grokcore.component',
    'megrok.pagetemplate>=0.3',
    ]

tests_requires = install_requires + [
    'zope.testing',
    'zope.app.testing',
    'zope.app.securitypolicy',
    'zope.app.zcmlfiles',
    ],


setup(name='zeam.utils.batch',
      version=version,
      description="Generic Batch support for Zope",
      long_description= "%s\n\n%s" % (
          open(os.path.join("zeam", "utils", "batch", "README.txt")).read(),
          open(os.path.join("docs", "HISTORY.txt")).read()
          ),
      classifiers=[
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        ],
      keywords='batch zope',
      author='Sylvain Viollon',
      author_email='thefunny@gmail.com',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['zeam', 'zeam.utils'],
      include_package_data=True,
      zip_safe=False,
      test_suite='zeam.utils.batch',
      tests_require = tests_requires,
      install_requires=install_requires,
      extras_require = {'test': tests_requires},
      )

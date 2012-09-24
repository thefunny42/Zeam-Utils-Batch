from setuptools import setup, find_packages
import os

version = '1.1'

install_requires=[
    'grokcore.component',
    'grokcore.view',
    'megrok.pagetemplate >=0.7',
    'setuptools',
    'zope.cachedescriptors',
    'zope.i18n',
    'zope.interface',
    'zope.publisher',
    'zope.traversing',
    ]

tests_requires = install_requires + [
    'zope.component',
    'zope.app.wsgi',
    'zope.testing',
    'grokcore.view [test]'
    ],


setup(name='zeam.utils.batch',
      version=version,
      description="Generic Batch support for Zope",
      long_description= "%s\n\n%s" % (
          open(os.path.join("src", "zeam", "utils", "batch", "README.txt")).read(),
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
      url='http://github.com/thefunny42/Zeam-Utils-Batch',
      license='BSD',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['zeam', 'zeam.utils'],
      include_package_data=True,
      zip_safe=False,
      test_suite='zeam.utils.batch',
      tests_require = tests_requires,
      install_requires=install_requires,
      extras_require = {'test': tests_requires},
      )

================
zeam.utils.batch
================

This package provides a batch functionality for Zope 2 and Zope 3.

A very straightforward example::

  >>> import grokcore.view as grok
  >>> from persistent import Persistent
  >>> from zope.component import queryMultiAdapter
  >>> from zeam.utils.batch import batch
  >>> from zeam.utils.batch.interfaces import IBatching

  >>> class Content(Persistent):
  ...     pass

  >>> class MyViewClass(grok.View):
  ...     grok.context(Content)
  ...     def update(self):
  ...          fulllist = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  ...          self.myitems = batch(
  ...                 fulllist , count=3, name='nbs', request=self.request)
  ...
  ...          self.batch = queryMultiAdapter(
  ...	              (self.context, self.myitems, self.request),
  ...          	      IBatching)()
  ...
  ...     template = grok.PageTemplate('''
  ...     <tal:navigation tal:replace="structure view/batch" />
  ...     <span tal:content="item" tal:repeat="item view/myitems" />
  ...     <tal:navigation tal:replace="structure view/batch" />
  ...     ''')

  >>> from grokcore.component import testing
  >>> testing.grok_component("view", MyViewClass)
  True

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

  >>> root = getRootFolder()
  >>> root['myObject'] = Content()
  >>> myobj = root['myObject']
 
  >>> view = queryMultiAdapter((myobj, request), name="myviewclass")
  >>> "batchNav" in view()
  True

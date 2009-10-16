================
zeam.utils.batch
================

This package provides a batch functionality for Zope 2, Zope 3 and Grok.

.. contents::

Example
=======

A very straightforward example. We need to define a context to work
on::

  >>> import grokcore.view as grok
  >>> from persistent import Persistent
  >>> from zope.component import queryMultiAdapter
  >>> from zeam.utils.batch import batch
  >>> from zeam.utils.batch.interfaces import IBatching

  >>> class Content(Persistent):
  ...     pass


And now, you can define a view which use a batch, and render it::

  >>> class MyViewClass(grok.View):
  ...     grok.context(Content)
  ...
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

And this work::

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


API
===

``batch``
   This object implement the batch.

   You create him by giving him a list of objects, and a request, a
   count of object (and potentially a name for your batch).

   Afterwards, you will have an iterable object, that you can access
   as a list as well, which gives you access to *only* the current
   object to work on for this page of the batch.

   You can get as well the number of pages of the batch, where you are
   and so on. Please refer to the interface, inside the package, for
   more information.

   You can render your batch by adapting your context, your batch
   object and request to an ``IBatching``. That will give you a piece
   of HTML to include on your view to control the batch.



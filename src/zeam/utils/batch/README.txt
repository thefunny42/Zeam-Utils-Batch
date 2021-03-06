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
  >>> from zeam.utils.batch import Batch
  >>> from zeam.utils.batch.interfaces import IBatching

  >>> class Content(Persistent):
  ...     pass


And now, you can define a view which use a batch, and render it::

  >>> class MyViewClass(grok.View):
  ...     grok.context(Content)
  ...
  ...     def update(self):
  ...          fulllist = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  ...          self.myitems = Batch(
  ...                 fulllist , count=3, name='nbs', request=self.request,
  ...                 factory=lambda x: str(x))
  ...
  ...          self.batch = queryMultiAdapter(
  ...                 (self, self.myitems, self.request),
  ...                     IBatching)()
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

``Batch``
   This object implements the batch.

   The batch object is instanciated with the following arguments:

   - a list of the objects to batch

   - the request

   - the number of items per page (as count, default to 10)

   - a name (optional)

   - a factory that will be passed each item before each iteration (optional)

   The batch is an iterable object behaving like a list.
   It only gives access to the set of objects for the current page.

   It provides the number of pages generated and the current position.
   Please refer to the interface, for more information.

   A multi adapter providing ``IBatching`` can render the batch.
   It adapts the context, the batch object and the request. The __call__
   method of this component will return a snippet of HTML containing
   basic controls for your batch: a next and previous link and a direct
   access to the other pages.

``DateBatch``
   This object implements a batch for date range. It follows the same
   API than the regular batch, except:

   - the list of objects is replaced by a callable that takes a
     datetime value has parameter and return a list of objects for the
     given periode

   - the count option is changed to use either the ``BATCH_DAY`` or
     ``BATCH_MONTH`` marker object.

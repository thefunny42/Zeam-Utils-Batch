zeam.utils.batch
================

This package provides a batch functionality for Zope 2 and Zope 3.

You can use it like that:

1. Your container which is going to handle the batch must implements
   the marker interface ``zeam.utils.batch.interfaces.IBatchedContent``.

2. You create your batch object in your view code::

     from zope.component import queryMultiAdapter
     from zeam.utils.batch import batch
     from zeam.utils.batch.interfaces import IBatchView


     class MyViewClass(...):

        def update(self):
           fulllist = ...
           self.myitems = batch(fulllist, count=10, name='myitems', request=self.request)
           self.batch = queryMultiAdapter((self.context, self.myitems, self.request),
                                          IBatchView)()


3. You use it in your template::

     <tal:navigation tal:replace="structure view/batch" />

     <tal:items tal:repeat="item view/myitems">
          ...
     </tal:items>

     <tal:navigation tal:replace="structure view/batch" />

That's it.


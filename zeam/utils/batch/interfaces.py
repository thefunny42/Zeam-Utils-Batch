# Copyright Sylvain Viollon 2008 (c)
# $Id: interfaces.py 86 2008-10-18 00:20:21Z sylvain $

from zope import schema
from zope.interface import Interface, Attribute


class IBatch(Interface):
    """A batch object.
    """
    start = schema.Int(
	title=u"Starting indice over the batch"
        )
    
    count = schema.Int(
	title=u"Number of element in a batch"
        )
    
    data = schema.List(
	title=u"Data to be batched"
        )
    
    name = schema.TextLine(
	title=u"Name of the batch",
	required=False,
	default=u""
        )

    first = Attribute("First element")
    last = Attribute("Last element")
    previous = Attribute("Previous index or None")
    next = Attribute("Next index or None")

    def __getitem__(index):
	"""Return item at index.
	"""

    def __iter__():
	"""Returns an iterator on batched content.
	"""

    def all():
	"""Returns an interator on all (index, starting element) of the
	batch.
	"""

    def batchLen():
        """Returns the number of available index in the batch.
        """


class IBatching(Interface):
    """Used to render a batch.
    """
    next = Attribute("Link to the next page or None")
    previous = Attribute("Link to the previous page or None")
    batch = Attribute("List of links to each page, which is current")

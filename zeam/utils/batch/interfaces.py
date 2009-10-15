# Copyright Sylvain Viollon 2008 (c)
# $Id: interfaces.py 86 2008-10-18 00:20:21Z sylvain $

from zope import interface
from zope.annotation.interfaces import IAttributeAnnotatable
from zope import schema

class IBatch(interface.Interface):
    """A batch object.
    """

    start = schema.Int(
	title=u"Starting indice over the batch")
    count = schema.Int(
	title=u"Number of element in a batch")
    data = schema.List(
	title=u"Data to be batched")
    name = schema.TextLine(
	title=u"Name of the batch",
	required=False,
	default=u"")

    first = interface.Attribute("First element")
    last = interface.Attribute("Last element")
    previous = interface.Attribute("Previous index or None")
    next = interface.Attribute("Next index or None")

    def __getitem__(index):
	"""Return item at index.
	"""

    def __iter__():
	"""Return an iterator on batched content.
	"""

    def all():
	"""Return an interator on all (index, starting element) of the
	batch.
	"""

    def batchLen():
        """Return the number of available index in the batch.
        """

class IBatchView(interface.Interface):
    """Used to render a batch.
    """

    next = interface.Attribute("Link to the next page or None")
    previous = interface.Attribute("Link to the previous page or None")
    batch = interface.Attribute("List of links to each page, which is current")

class IBatchedContent(IAttributeAnnotatable):
    """Marker interface for content with batched data.
    """

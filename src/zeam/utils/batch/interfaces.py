# Copyright Sylvain Viollon 2008 (c)
# $Id: interfaces.py 86 2008-10-18 00:20:21Z sylvain $

from zope.interface import Interface, Attribute


class IBatchBehavior(Interface):
    """A basic batch behavior.
    """
    start = Attribute(
        u"Starting indice over the batch")
    count = Attribute(
        u"Number of element in a batch")
    data = Attribute(
        u"Data to be batched (source)")
    name = Attribute(
        u"Name of the batch")
    factory = Attribute(
        u"Factory used to create element returned from the batch")

    def __getitem__(index):
        """Return item at index in the current batch view.
        """

    def __iter__():
        """Returns an iterator on content in the current batch view.
        """

    def __len__():
        """Returns number of items in the curretn batch views.
        """


class IBatch(IBatchBehavior):
    """A batch object.
    """
    first = Attribute("First element")
    last = Attribute("Last element")
    previous = Attribute("Previous index or None")
    next = Attribute("Next index or None")

    def all():
        """Returns an interator on all (index, starting element) of the
        batch.
        """

    def batch_length():
        """Returns the number of available index in the batch.
        """

class IDateBatch(IBatchBehavior):
    """Batch element by date.
    """


class IBatching(Interface):
    """Used to render a batch.
    """
    keep_query_string = Attribute(u"Should query string be kept")

    batch = Attribute(u"Iterate through each batch navigation entry.")
    batch_previous = Attribute(u"Previous batch/navigation entry")
    # Cannot call batch_next next because of a Chameleon issue
    batch_next = Attribute(u"Next batch/navigation entry")

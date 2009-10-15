# Copyright Sylvain Viollon 2008 (c)
# $Id: batch.py 94 2008-10-20 22:20:34Z sylvain $

from interfaces import IBatch
from zope.interface import implements


class batchBaseIterator(object):
    """An iterator on batch object.
    """
    def __init__(self, context):
        self.context = context
        self.start = 0

    def __iter__(self):
        return self


class batchItemIterator(batchBaseIterator):
    """Return the next object in the batch iterator.
    """
    def next(self):
        try:
            elt = self.context[self.start]
        except IndexError:
            raise StopIteration
        self.start += 1
        return elt


class batchIndiceIterator(batchBaseIterator):
    """Return the next indice in the batch iterator.
    """
    def next(self):
        last = self.context.last
        if not last:
            raise StopIteration
        if self.start < last:
            value = self.start
            self.start += self.context.count
            return (value, value / self.context.count + 1)
        raise StopIteration


class batch(object):
    """A simple batch object.
    """
    implements(IBatch)

    def __init__(self, collection, start=0, count=10, name='', request=None):
	if not (request is None):
	    key = 'bstart'
	    if name:
		key += '_' + name
	    start = int(request.form.get(key, 0))
        self.start = start
        self.count = count
        self.data = collection
	self.name = name

    def _setData(self, data):
        self._data = data
        self._end = len(self._data)
        if not self.count or self.count > self._end:
            self._max = self._end
        else:
            self._max = self.count

    def _getData(self):
        return self._data

    data = property(_getData, _setData)

    def __getitem__(self, index):
        if index < 0 or index >= self._max:
            raise IndexError, "invalid index"
        return self.data[self.start + index]

    def batchLen(self):
        if not self.count:
            return 0
        last = self._end % self.count
        if last:
            last = 1
        return (self._end / self.count) + last

    def __iter__(self):
        return batchItemIterator(self)

    def all(self):
        return batchIndiceIterator(self)

    @property
    def first(self):
        return 0

    @property
    def previous(self):
        previous = self.start - self.count
        if previous < 0:
            return None
        return previous

    @property
    def last(self):
        return self.batchLen() * self.count

    @property
    def next(self):
        next = self.start + self.count
        if next >= self.last:
            return None
        return next


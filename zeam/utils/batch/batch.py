# Copyright Sylvain Viollon 2008 (c)
# $Id: batch.py 94 2008-10-20 22:20:34Z sylvain $

from zeam.utils.batch.interfaces import IBatch
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

    def __init__(self, context, factory=None):
        super(batchItemIterator, self).__init__(context)
        self.factory = factory

    def next(self):
        try:
            def fetch():
                return self.context[self.start]
            if self.factory is not None:
                elt = self.factory(fetch())
            else:
                elt = fetch()
        except IndexError:
            raise StopIteration
        self.start += 1
        return elt


class batchIndiceIterator(batchBaseIterator):
    """Return the next indice in the batch iterator.
    """
    def next(self):
        last = self.context.count * self.context.batchLen()
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

    def __init__(self, collection, start=0, count=10, name='',
        request=None, factory=None):
        if not (request is None):
            key = 'bstart'
            if name:
                key += '_' + name
            start = int(request.form.get(key, 0))
        self.start = start
        self.count = count
        self.data = collection
        self.name = name
        self.factory = factory

    def _setData(self, data):
        self._data = data
        self._end = len(self._data)
        if not self.count or self.count > self._end:
            # self._count is the effective count to use.
            self._count = self._end
        else:
            self._count = self.count

    def _getData(self):
        return self._data

    data = property(_getData, _setData)

    def __getitem__(self, index):
        if index < 0 or index >= self._count:
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
        return batchItemIterator(self, factory=self.factory)

    def __len__(self):
        return min(self._end - self.start, self._count)

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
        len = self.batchLen()
        if not len:
            return 0
        return (len - 1) * self.count

    @property
    def next(self):
        next = self.start + self.count
        if next >= (self.count * self.batchLen()):
            return None
        return next


# Copyright Sylvain Viollon 2008 (c)
# $Id: batch.py 94 2008-10-20 22:20:34Z sylvain $

from zeam.utils.batch.interfaces import IBatch, IActiveBatch
from zope.interface import implements


class BatchBaseIterator(object):
    """An iterator on Batch object.
    """
    def __init__(self, context):
        self.context = context
        self.start = 0

    def __iter__(self):
        return self


class BatchItemIterator(BatchBaseIterator):
    """Return the next object in the Batch iterator.
    """

    def __init__(self, context, factory=None):
        super(BatchItemIterator, self).__init__(context)
        self.factory = factory

    def next(self):
        try:
            element = self.context[self.start]
        except IndexError:
            raise StopIteration
        self.start += 1
        return element


class BatchIndiceIterator(BatchBaseIterator):
    """Return the next indice in the Batch iterator.
    """
    def next(self):
        last = self.context.count * self.context.batch_length()
        if not last:
            raise StopIteration
        if self.start < last:
            value = self.start
            self.start += self.context.count
            return (value, value / self.context.count + 1)
        raise StopIteration


class Batch(object):
    """A simple batch object.
    """
    implements(IBatch)

    def __init__(
        self, collection,
        start=0, count=10, name='', request=None, factory=None):

        if request is not None:
            key = 'bstart'
            if name:
                key += '_' + name
            try:
                start = int(request.form.get(key, 0))
            except (ValueError, TypeError):
                pass
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
        element = self.data[self.start + index]
        if self.factory is not None:
            return self.factory(element)
        return element

    def batch_length(self):
        if not self.count:
            return 0
        last = self._end % self.count
        if last:
            last = 1
        return (self._end / self.count) + last

    def __iter__(self):
        return BatchItemIterator(self, factory=self.factory)

    def __len__(self):
        return max(min(self._end - self.start, self._count), 0)

    def all(self):
        return BatchIndiceIterator(self)

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
        len = self.batch_length()
        if not len:
            return 0
        return (len - 1) * self.count

    @property
    def next(self):
        next = self.start + self.count
        if next >= (self.count * self.batch_length()):
            return None
        return next


class ActiveBatch(object):
    implements(IActiveBatch)

    def __init__(
        self, collection,
        start=None, count=None, name='', request=None, factory=None):
        self.start = start
        self.name = name
        self.factory = factory
        self.count = count
        self._setData(collection)

    def _setData(self, collection):
        self._data = list(collection(self.start))
        self._count = len(self._data)

    def _getData(self):
        return self._data

    data = property(_getData, _setData)

    def __getitem__(self, index):
        if index < 0 or index >= self._count:
            raise IndexError("invalid index")
        element = self._data[index]
        if self.factory is not None:
            return self.factory(element)
        return element

    def __iter__(self):
        return BatchItemIterator(self, factory=self.factory)

    def __len__(self):
        return self._count

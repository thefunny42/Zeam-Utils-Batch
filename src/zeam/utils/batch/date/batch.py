
from datetime import datetime

from zeam.utils.batch.interfaces import IDateBatch
from zeam.utils.batch.batch import BatchItemIterator
from zope.interface import implements

# Create a batch level for each ...
BATCH_DAY = object()
BATCH_MONTH = object()


class DateBatch(object):
    implements(IDateBatch)

    def __init__(
        self, collection,
        start=None, count=BATCH_MONTH, name='', request=None, factory=None):
        if request is not None:
            key = 'bstart'
            if name:
                key += '_' + name
            if key in request.form:
                try:
                    start = datetime.fromtimestamp(int(request.form[key]))
                except (ValueError, TypeError):
                    pass
        if start is None:
            start = datetime.now()
        self.start = start
        self.name = name
        self.factory = factory
        self._setData(collection)

    def _setData(self, collection):
        self._data = list(collection(self.start))
        self._count = len(self._data)

    def _getData(self):
        return self._data

    data = property(_getData, _setData)

    def __getitem__(self, index):
        if index < 0 or index >= self._count:
            raise IndexError, "invalid index"
        element = self._data[index]
        if self.factory is not None:
            return self.factory(element)
        return element

    def __iter__(self):
        return BatchItemIterator(self, factory=self.factory)

    def __len__(self):
        return self._count

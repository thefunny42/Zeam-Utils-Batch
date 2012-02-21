
from datetime import datetime

from zeam.utils.batch.interfaces import IDateBatch
from zeam.utils.batch.batch import ActiveBatch
from zope.interface import implements

# Create a batch level for each ...
BATCH_DAY = object()
BATCH_MONTH = object()


class DateBatch(ActiveBatch):
    implements(IDateBatch)

    def __init__(
        self, collection,
        start=None, count=BATCH_MONTH, name='', request=None, factory=None,
        default_all=False):
        if request is not None:
            key = 'bstart'
            if name:
                key += '_' + name
            if key in request.form:
                try:
                    start = datetime.strptime(request.form[key], '%Y-%m')
                except (ValueError, TypeError):
                    pass
        if start is None and not default_all:
            start = datetime.now()
        super(DateBatch, self).__init__(
            collection,
            start=start, count=count, name=name,
            request=request, factory=factory)

    def all(self):
        for month in range(1, 13):
            yield datetime(self.start.year, month, 1)

    def batch_length(self):
        return 12

    @property
    def previous(self):
        return datetime(self.start.year - 1, 12, 1)

    @property
    def next(self):
        return datetime(self.start.year + 1, 1, 1)

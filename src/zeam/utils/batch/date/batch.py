
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
        min=None, max=None):
        if request is not None:
            key = 'bstart'
            if name:
                key += '_' + name
            if key in request.form:
                try:
                    start = datetime.strptime(request.form[key], '%Y-%m')
                except (ValueError, TypeError):
                    pass
        if start is None:
            start = datetime.now()
        self.min = min
        self.max = max
        super(DateBatch, self).__init__(
            collection,
            start=start, count=count, name=name,
            request=request, factory=factory)

    def all(self):
        start = 1
        if self.min is not None:
            if self.min.year == self.start.year:
                # We are on the starting year.
                start = self.min.month
            elif self.min.year > self.start.year:
                # We are before the starting year
                start = 13
        end = 13
        if self.max is not None:
            if self.max.year == self.start.year:
                # We are on the ending year
                end = self.max.month + 1
            elif self.max.year < self.start.year:
                # We are after the ending year
                end = 1
        for month in range(start, end):
            yield datetime(self.start.year, month, 1)

    def batch_length(self):
        return 12

    @property
    def previous(self):
        if self.min is not None and self.min.year >= self.start.year:
            # We are before the minimal year.
            return None
        if self.max is not None and self.max.year < self.start.year:
            # We are after the maximal year.
            return None
        return datetime(self.start.year - 1, 12, 1)

    @property
    def next(self):
        if self.max is not None and self.max.year <= self.start.year:
            # We are after the maximal year.
            return None
        if self.min is not None and self.min.year > self.start.year:
            # We are before the minimal year.
            return None
        return datetime(self.start.year + 1, 1, 1)

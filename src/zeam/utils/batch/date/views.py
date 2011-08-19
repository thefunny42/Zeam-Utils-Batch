
from datetime import datetime

import megrok.pagetemplate
import grokcore.component as grok

from zope.interface import Interface
from zope.publisher.interfaces.http import IHTTPRequest

from zeam.utils.batch.interfaces import IDateBatch
from zeam.utils.batch.views import BasicBatching


class Batching(BasicBatching):
    """View object on batched elements.
    """
    grok.adapts(Interface, IDateBatch, IHTTPRequest)

    def _get_month_names(self):
        dates = self.request.locale.dates
        return dates.calendars['gregorian'].getMonthAbbreviations()

    @property
    def batch(self):
        month_names = self._get_month_names()
        current = self._batch.start
        for month in range(1, 13):
            month_tms = datetime(current.year, month, 1).strftime("%s")
            url_item = self._create_link(month_tms)
            current_item = (month == current.month)
            style = current_item and 'current' or None
            yield dict(year=current.year,
                       month=month_names[month-1],
                       url=url_item,
                       style=style)

    @property
    def batch_previous(self):
        current = self._batch.start
        previous_tms = datetime(current.year - 1, 12, 1).strftime("%s")
        return dict(year=current.year - 1, url=self._create_link(previous_tms))

    @property
    def batch_next(self):
        current = self._batch.start
        next_tms = datetime(current.year + 1, 1, 1).strftime("%s")
        return dict(year=current.year + 1, url=self._create_link(next_tms))


class BatchPages(megrok.pagetemplate.PageTemplate):
    megrok.pagetemplate.view(Batching)

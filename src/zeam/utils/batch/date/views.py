

import megrok.pagetemplate
import grokcore.component as grok

from zope.interface import Interface
from zope.publisher.interfaces.http import IHTTPRequest
from zope.cachedescriptors.property import Lazy

from zeam.utils.batch.interfaces import IDateBatch
from zeam.utils.batch.views import BasicBatching


class DateBatching(BasicBatching):
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
        for date in self._batch.all():
            month_tms = date.strftime("%Y-%m")
            url_item = self._create_link(month_tms)
            current_item = (date.month == current.month)
            style = current_item and 'current' or None
            yield dict(year=current.year,
                       month=month_names[date.month - 1],
                       url=url_item,
                       style=style)

    @Lazy
    def batch_previous(self):
        previous = self._batch.previous
        if previous is not None:
            previous_tms = previous.strftime("%Y-%m")
            return dict(year=previous.year, url=self._create_link(previous_tms))
        return {}

    @Lazy
    def batch_next(self):
        next = self._batch.next
        if next is not None:
            next_tms = next.strftime("%Y-%m")
            return dict(year=next.year, url=self._create_link(next_tms))
        return {}


class BatchPages(megrok.pagetemplate.PageTemplate):
    megrok.pagetemplate.view(DateBatching)

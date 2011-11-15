

import megrok.pagetemplate
import grokcore.component as grok

from zope.interface import Interface
from zope.publisher.interfaces.http import IHTTPRequest

from zeam.utils.batch.interfaces import IAlphabeticalBatch
from zeam.utils.batch.views import Batching


class AlphabeticalBatching(Batching):
    """View object on batched elements.
    """
    grok.adapts(Interface, IAlphabeticalBatch, IHTTPRequest)

    @property
    def batch(self):
        for letter in self._batch.all():
            current_item = (letter == self._batch.start)
            style = current_item and 'current' or None
            yield dict(name=letter, url=self._create_link(letter), style=style)


class BatchPages(megrok.pagetemplate.PageTemplate):
    megrok.pagetemplate.view(AlphabeticalBatching)

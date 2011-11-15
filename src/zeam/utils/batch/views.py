# Copyright Sylvain Viollon 2008 (c)
# $Id: views.py 96 2008-10-20 22:25:04Z sylvain $

from urllib import urlencode

import megrok.pagetemplate
import grokcore.component as grok

from zope.cachedescriptors.property import CachedProperty
from zope.interface import Interface
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.browser import absoluteURL
from zope.traversing.interfaces import ITraversable

from zeam.utils.batch.interfaces import IBatch, IBatching


class BasicBatching(grok.MultiAdapter):
    grok.baseclass()
    grok.implements(IBatching)
    grok.provides(IBatching)

    keep_query_string = True

    def __init__(self, context, batch, request):
        self.context = context
        self.request = request
        self._batch = batch

    def __call__(self):
        template = megrok.pagetemplate.getPageTemplate(self, self.request)
        if template is None:
            return u""
        return template()

    @CachedProperty
    def url(self):
        return absoluteURL(self.context, self.request)

    @CachedProperty
    def query_string(self):
        params = self.request.form.copy()
        for key in params.keys():
            if key.startswith('bstart'):
                del params[key]
        return urlencode(params)

    def default_namespace(self):
        namespace = {}
        namespace['context'] = self.context
        namespace['request'] = self.request
        namespace['batch'] = self
        return namespace

    def namespace(self):
        namespace = {}
        return namespace

    def _create_link(self, position):
        def append_qs(url):
            if not self.keep_query_string:
                return url
            if self.query_string:
                return "%s?%s" % (url, self.query_string,)
            return url

        if not position:
            return append_qs(self.url)
        if self._batch.name:
            return append_qs("%s/++batch++%s+%s" % (
                self.url, self._batch.name, position))
        return append_qs("%s/++batch++%s" % (self.url, position))

    @property
    def batch_length(self):
        return self._batch.batch_length()

    @property
    def batch(self):
        raise NotImplementedError

    @property
    def batch_next(self):
        raise NotImplementedError

    @property
    def batch_previous(self):
        raise NotImplementedError


class Batching(BasicBatching):
    """View object on batched elements.
    """
    grok.adapts(Interface, IBatch, IHTTPRequest)

    @property
    def batch(self):
        end = self._batch.batch_length()
        if end > 1:
            count = 0
            wanted = self._batch.start / self._batch.count
            ldots = False
            for pos, item in self._batch.all():
                if (((count > 2) and (count < (wanted - 3))) or
                    ((count < (end - 3)) and (count > (wanted + 3)))):
                    if not ldots:
                        ldots = True
                        yield dict(name=None, url=None, style=None)

                else:
                    ldots = False
                    url_item = self._create_link(pos)
                    current_item = (pos == self._batch.start)
                    style = current_item and 'current' or None
                    yield dict(name=item, url=url_item, style=style)
                count += 1

    @property
    def batch_previous(self):
        previous = self._batch.previous
        avail = not (previous is None)
        return avail and dict(url=self._create_link(previous)) or None

    @property
    def batch_next(self):
        next = self._batch.next
        avail = not (next is None)
        return avail and dict(url=self._create_link(next)) or None

    @property
    def batch_first(self):
        return dict(url=self._create_link(self._batch.first))

    @property
    def batch_last(self):
        return dict(url=self._create_link(self._batch.last))


class BatchPages(megrok.pagetemplate.PageTemplate):
    megrok.pagetemplate.view(Batching)


class Namespace(grok.MultiAdapter):
    """Make batch works with namespace.
    """
    grok.name('batch')
    grok.provides(ITraversable)
    grok.adapts(Interface, IHTTPRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignored):
        if '+' in name:
            key, value = name.split('+')
            key = 'bstart_' + key
        else:
            key = 'bstart'
            value = name
        self.request.form[key] = value
        return self.context

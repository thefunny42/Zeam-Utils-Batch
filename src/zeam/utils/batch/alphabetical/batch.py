
import string

from zeam.utils.batch.interfaces import IAlphabeticalBatch
from zeam.utils.batch.batch import ActiveBatch
from zope.interface import implements


class AlphabeticalBatch(ActiveBatch):
    implements(IAlphabeticalBatch)

    def __init__(
        self, collection,
        start=None, count=None, name='', request=None, factory=None,
        letters=string.uppercase, no_default=False):
        assert len(letters), 'need a list of letters to iterate through'
        if request is not None:
            key = 'bstart'
            if name:
                key += '_' + name
            if key in request.form:
                start = request.form[key]
        if start is None and not no_default:
            start = letters[0]
        super(AlphabeticalBatch, self).__init__(
            collection,
            start=start, count=count, name=name,
            request=request, factory=factory)
        self.letters = letters

    def all(self):
        return iter(self.letters)

    def batch_length(self):
        return len(self.letters)

    @property
    def first(self):
        return self.letters[0]

    @property
    def last(self):
        return self.letters[-1]

    @property
    def previous(self):
        try:
            if self.start:
                index = self.letters.index(self.start)
                if index:
                    return self.letters[index - 1]
        except ValueError:
            pass
        return None

    @property
    def next(self):
        try:
            if self.start:
                index = self.letters.index(self.start)
                if index < len(self.letters) - 1:
                    return self.letters[index + 1]
        except ValueError:
            pass
        return None

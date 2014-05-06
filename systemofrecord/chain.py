import json
import requests
from .entry import Entry
from .storage import MemoryStorage

class DocumentChain(object):
    def __init__(self, storage=None, webhooks=None):
        self.storage =  storage or MemoryStorage()
        self.webhooks = webhooks or []

    def add(self, content):
        entry = Entry(
            content=content,
            previous_id=self.storage.get_head(),
        )
        id = entry.get_id()
        self.storage.add_entry(id, entry.to_json())
        for url in self.webhooks:
            res = requests.post(
                url,
                data=entry.to_json(),
                headers={'content-type': 'application/json'}
            )
            try:
                res.raise_for_status()
            except:
                print res.content
                raise
        return id

    def get(self, id):
        return Entry.from_json(self.storage.get_entry(id))

    def all(self):
        """
        Returns an iterator of all entries.
        """
        id = self.storage.get_head()
        while id:
            entry = Entry.from_json(self.storage.get_entry(id))
            yield entry
            id = entry.previous_id

    def verify(self):
        for entry in self.invalid_entries():
            return False
        return True

    def invalid_entries(self):
        """
        Returns an iterator of entries which are invalid.
        """
        id = self.storage.get_head()
        while id:
            entry = Entry.from_json(self.storage.get_entry(id))
            if entry.get_id() != id:
                yield entry
            id = entry.previous_id

    def get_head(self):
        id = self.storage.get_head()
        return Entry.from_json(self.storage.get_entry(id))

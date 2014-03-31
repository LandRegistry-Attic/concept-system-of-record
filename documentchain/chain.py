import datetime
import hashlib
import json
from .storage import MemoryStorage

class DocumentChain(object):
    def __init__(self, storage=None):
        if storage is None:
            self.storage = MemoryStorage()
        else:
            self.storage = storage

    def add(self, content):
        entry = json.dumps({
            "content": content,
            "meta": {
                "previous_id": self.storage.get_head(),
                "timestamp": datetime.datetime.utcnow().isoformat(),
            },
        })
        id = hashlib.sha256(entry).hexdigest()
        self.storage.set_entry(id, entry)
        self.storage.set_head(id)
        return id

    def get(self, id):
        return json.loads(self.storage.get_entry(id))['content']

    def all(self):
        """
        Returns an iterator of all entries.
        """
        id = self.storage.get_head()
        while id:
            entry = json.loads(self.storage.get_entry(id))
            yield entry
            id = entry["meta"]["previous_id"]

    def verify(self):
        id = self.storage.get_head()
        while id:
            document = self.storage.get_entry(id)
            if hashlib.sha256(document).hexdigest() != id:
                return False
            id = json.loads(document)["meta"]["previous_id"]
        return True

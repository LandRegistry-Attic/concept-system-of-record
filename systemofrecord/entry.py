import datetime
import hashlib
import json
from .utils import canonical_json

class Entry(object):
    """
    An entry in a document chain.
    """
    def __init__(self, content, previous_id, timestamp=None):
        self.content = content
        self.previous_id = previous_id
        if timestamp is None:
            self.timestamp = datetime.datetime.utcnow().isoformat()
        else:
            self.timestamp = timestamp

    @classmethod
    def from_json(cls, s):
        d = json.loads(s)
        return cls(
            content=d['content'],
            previous_id=d['meta']['previous_id'],
            timestamp=d['meta']['timestamp'],
        )

    def serialize(self, with_id=True):
        d = {
            "meta": self.get_meta(),
            "content": self.content,
        }
        if with_id:
            d['id'] = self.get_id()
        return d

    def to_json(self):
        return canonical_json(self.serialize(with_id=False))

    def get_meta(self):
        return {
            "previous_id": self.previous_id,
            "timestamp": self.timestamp,
        }

    def get_id(self):
        return hashlib.sha256(self.to_json()).hexdigest()

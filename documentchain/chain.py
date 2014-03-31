import datetime
import hashlib
import json

class DocumentChain(object):
    def __init__(self):
        self.documents = {}
        self.head = None

    def add(self, content):
        entry = json.dumps({
            "content": content,
            "meta": {
                "previous_id": self.head,
                "timestamp": datetime.datetime.utcnow().isoformat(),
            },
        })
        id = hashlib.sha256(entry).hexdigest()
        self.documents[id] = entry
        self.head = id
        return id

    def get(self, id):
        return json.loads(self.documents[id])['content']

    def verify(self):
        id = self.head
        while id:
            document = self.documents[id]
            if hashlib.sha256(document).hexdigest() != id:
                return False
            id = json.loads(document)["meta"]["previous_id"]
        return True

import os

class MemoryStorage(object):
    def __init__(self):
        self.entries = {}
        self.head = None

    def set_entry(self, id, content):
        self.entries[id] = content

    def get_entry(self, id):
        return self.entries[id]

    def set_head(self, id):
        self.head = id

    def get_head(self):
        return self.head


class DiskStorage(object):
    def __init__(self, path):
        self.path = path

    def set_entry(self, id, content):
        with open(os.path.join(self.path, id), 'w') as fh:
            fh.write(content)

    def get_entry(self, id):
        with open(os.path.join(self.path, id)) as fh:
            return fh.read()

    def set_head(self, id):
        with open(os.path.join(self.path, 'HEAD'), 'w') as fh:
            fh.write(id)

    def get_head(self):
        try:
            with open(os.path.join(self.path, 'HEAD')) as fh:
                return fh.read()
        except IOError, e:
            # No such file or directory
            if e.errno == 2:
                return None
            else:
                raise

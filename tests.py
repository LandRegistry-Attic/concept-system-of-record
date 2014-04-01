import mock
import os
import tempfile
import unittest
from documentchain import DocumentChain
from documentchain.storage import DiskStorage, MemoryStorage

class DocumentChainTest(unittest.TestCase):
    def test_add(self):
        chain = DocumentChain()
        id1 = chain.add({'owner': 'victor'})
        id2 = chain.add({'owner': 'theodore'})
        self.assertEqual(chain.get(id1).content, {'owner': 'victor'})
        self.assertEqual(chain.get(id2).content, {'owner': 'theodore'})

    def test_verify(self):
        chain = DocumentChain()
        chain.add({'owner': 'victor'})
        self.assertTrue(chain.verify())
        chain.add({'owner': 'theodore'})
        self.assertTrue(chain.verify())

    def test_verify_broken_first_entry(self):
        storage = MemoryStorage()
        chain = DocumentChain(storage=storage)
        id1 = chain.add({'owner': 'victor'})
        id2 = chain.add({'owner': 'theodore'})
        self.assertTrue(chain.verify())
        entry = storage.get_entry(id1)
        storage.set_entry(id1, entry.replace('victor', 'eddie'))
        self.assertFalse(chain.verify())

    def test_verify_broken_second_entry(self):
        storage = MemoryStorage()
        chain = DocumentChain(storage=storage)
        id1 = chain.add({'owner': 'victor'})
        id2 = chain.add({'owner': 'theodore'})
        self.assertTrue(chain.verify())
        entry = storage.get_entry(id2)
        storage.set_entry(id2, entry.replace('theodore', 'eddie'))
        self.assertFalse(chain.verify())

    def test_all(self):
        chain = DocumentChain()
        chain.add({'owner': 'victor'})
        chain.add({'owner': 'theodore'})
        self.assertEqual([e.content for e in chain.all()], [
            {'owner': 'theodore'},
            {'owner': 'victor'},
        ])

    def test_get_head(self):
        chain = DocumentChain()
        chain.add({'owner': 'victor'})
        self.assertEqual(chain.get_head().content, {'owner': 'victor'})

    @mock.patch('requests.post')
    def test_webhooks(self, mock_post):
        chain = DocumentChain(webhooks=['http://example.com/webhook'])
        chain.add({'owner': 'victor'})
        entry = chain.get_head()
        mock_post.assert_called_once_with(
            'http://example.com/webhook',
            data=entry.to_json(),
            headers={'content-type': 'application/json'}
        )

class DiskStorageTest(unittest.TestCase):
    def test_set_entry(self):
        path = tempfile.mkdtemp()
        storage = DiskStorage(path)
        storage.set_entry('abcd', 'content')
        with open(os.path.join(path, 'abcd')) as fh:
            self.assertEqual(fh.read(), 'content')

    def test_get_entry(self):
        path = tempfile.mkdtemp()
        with open(os.path.join(path, '0123'), 'w') as fh:
            fh.write('content')
        storage = DiskStorage(path)
        self.assertEqual(storage.get_entry('0123'), 'content')

    def test_set_head(self):
        path = tempfile.mkdtemp()
        storage = DiskStorage(path)
        storage.set_head('abcd')
        with open(os.path.join(path, 'HEAD')) as fh:
            self.assertEqual(fh.read(), 'abcd')

    def test_get_head(self):
        path = tempfile.mkdtemp()
        with open(os.path.join(path, 'HEAD'), 'w') as fh:
            fh.write('0123')
        storage = DiskStorage(path)
        self.assertEqual(storage.get_head(), '0123')

    def test_get_head_none(self):
        path = tempfile.mkdtemp()
        storage = DiskStorage(path)
        self.assertEqual(storage.get_head(), None)


if __name__ == '__main__':
    unittest.main()

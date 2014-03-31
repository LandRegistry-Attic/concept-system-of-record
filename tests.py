import unittest
from documentchain import DocumentChain

class DocumentChainTest(unittest.TestCase):
    def test_add(self):
        chain = DocumentChain()
        id1 = chain.add({'owner': 'victor'})
        id2 = chain.add({'owner': 'theodore'})
        self.assertEqual(chain.get(id1), {'owner': 'victor'})
        self.assertEqual(chain.get(id2), {'owner': 'theodore'})

    def test_verify(self):
        chain = DocumentChain()
        chain.add({'owner': 'victor'})
        self.assertTrue(chain.verify())
        chain.add({'owner': 'theodore'})
        self.assertTrue(chain.verify())


if __name__ == '__main__':
    unittest.main()

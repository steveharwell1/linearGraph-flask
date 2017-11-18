import os
import graph
import unittest
import tempfile

class graphTestCase(unittest.TestCase):

    def setUp(self):
        #self.db_fd, graph.app.config['DATABASE'] = tempfile.mkstemp()
        graph.app.testing = True
        self.app = graph.app.test_client()
        #with graph.app.app_context():
        #    graph.init_db()

    def tearDown(self):
        pass
        #os.close(self.db_fd)
        #os.unlink(graph.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
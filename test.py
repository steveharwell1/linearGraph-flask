import os
import io
import graph
import unittest
import tempfile


class graphTestCase(unittest.TestCase):

    def setUp(self):
        self.dir = "."
        #self.db_fd, graph.app.config['DATABASE'] = tempfile.mkstemp()
        graph.app.testing = True
        self.app = graph.app.test_client()
        # with graph.app.app_context():
        #    graph.init_db()

    def tearDown(self):
        pass
        # os.close(self.db_fd)
        # os.unlink(graph.app.config['DATABASE'])

    def test_root_path(self):
        response = self.app.get('/')
        self.assertIn(b"<!DOCTYPE html>", response.data)

    def test_image_path(self):
        with open(self.dir + '/img/img.png', 'rb') as img1:
            imgByteIO = io.BytesIO(img1.read())

        response = self.app.get("/api/v1/linear/graph/3.0/2.0")

        imgByteIO.seek(0)
        self.assertEqual(response.data, imgByteIO.read())


if __name__ == '__main__':
    unittest.main()

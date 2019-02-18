import unittest
from app.models import Post,User
from app import db


class PostTest(unittest.TestCase):

    def setUp(self):
        self.user_James = User(username = 'James',password = 'potato', email = 'james@ms.com')
        self.new_post= Post(id=12345,title='Title for pitches',author_id =1)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post,Post))


    def test_to_check_instance_variables(self):
        self.assertEquals(self.new_post.id,12345)
        self.assertEquals(self.new_post.title,'Title for pitches')
        self.assertEquals(self.new_post.author_id,1)
        



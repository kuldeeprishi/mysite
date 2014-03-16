from django.test import TestCase
from django.utils import timezone
from .models import Post


class PostTest(TestCase):
	def test_create_post(self):
		# create a test post
		post = Post()
		post.title = "Test post title"
		post.text = "This is body of test post"
		post.pub_date = timezone.now()
		post.save()

		# check post created
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# check attributes
		self.assertEquals(only_post.title, "Test post title")
		self.assertEquals(only_post.text, "This is body of test post")
		self.assertEquals(only_post.pub_date.day, post.pub_date.day)
		self.assertEquals(only_post.pub_date.month, post.pub_date.month)
		self.assertEquals(only_post.pub_date.year, post.pub_date.year)
		self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
		self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
		self.assertEquals(only_post.pub_date.second, post.pub_date.second)



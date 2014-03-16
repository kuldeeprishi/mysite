from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from .models import Post


class PostTest(TestCase):
	def test_create_post(self):
		# Create a test post
		post = Post()
		post.title = "Test post title"
		post.text = "This is body of test post"
		post.pub_date = timezone.now()
		post.save()

		# Check post created
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Check attributes
		self.assertEquals(only_post.title, "Test post title")
		self.assertEquals(only_post.text, "This is body of test post")
		self.assertEquals(only_post.pub_date.day, post.pub_date.day)
		self.assertEquals(only_post.pub_date.month, post.pub_date.month)
		self.assertEquals(only_post.pub_date.year, post.pub_date.year)
		self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
		self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
		self.assertEquals(only_post.pub_date.second, post.pub_date.second)


class AdminTest(LiveServerTestCase):
	fixtures = ['users.json']
	def test_login(self):
		# Create client
		c = Client()

		# Get login page
		response = c.get('/admin/')

		# Check response code
		self.assertEquals(response.status_code, 200)

		# Check 'Log in' in response
		self.assertTrue('Log in' in response.content)

		# Log the user in
		c.login(username='kuldeeprishi', password='password')

		# Check response code
		response = c.get('/admin/')
		self.assertEquals(response.status_code, 200)

		# Check 'Log out' in response
		self.assertTrue('Log out' in response.content)

		def test_logout(self):
			c = Client()
			c.login(username='kuldeeprishi', password="password")

			response = c.get('/admin/')
			self.assertEquals(response.status_code, 200)

			self.assertTrue('Log out' in response.content)

			c.logout()

			response = c.get('/admin/')
			self.assertEquals(response.status_code, 200)
			self.assertTrue('Log in' in response.content)

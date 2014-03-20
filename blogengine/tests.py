from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from .models import Post, Category, Tag
import markdown


class BaseAcceptanceTest(LiveServerTestCase):
	def setUp(self):
		self.client = Client()


class CategoryTest(LiveServerTestCase):
	fixtures = ['users.json']

	def test_create_tag(self):
		# Create the tag
		tag = Tag()

		# Add attributes
		tag.name = 'python'
		tag.description = 'The Python programming language'

		# Save it
		tag.save()

		# Check we can find it
		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 1)
		only_tag = all_tags[0]
		self.assertEquals(only_tag, tag)

		# Check attributes
		self.assertEquals(only_tag.name, 'python')
		self.assertEquals(only_tag.description, 'The Python programming language')

	def test_create_tag(self):
		# Log in
		self.client.login(username='kuldeeprishi', password="password")

		# Check response code
		response = self.client.get('/admin/blogengine/tag/add/')
		self.assertEquals(response.status_code, 200)

		# Create the new tag
		response = self.client.post('/admin/blogengine/tag/add/', {
		    'name': 'python',
		    'description': 'The Python programming language'
		    },
		    follow=True
		)
		self.assertEquals(response.status_code, 200)

		# Check added successfully
		self.assertTrue('added successfully' in response.content)

		# Check new tag now in database
		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 1)

	def test_edit_tag(self):
		# Create the tag
		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		# Log in
		self.client.login(username='kuldeeprishi', password="password")

		# Edit the tag
		response = self.client.post('/admin/blogengine/tag/1/', {
		    'name': 'perl',
		    'description': 'The Perl programming language'
		    }, follow=True)
		self.assertEquals(response.status_code, 200)

		# Check changed successfully
		self.assertTrue('changed successfully' in response.content)

		# Check tag amended
		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 1)
		only_tag = all_tags[0]
		self.assertEquals(only_tag.name, 'perl')
		self.assertEquals(only_tag.description, 'The Perl programming language')

	def test_delete_tag(self):
		# Create the tag
		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		# Log in
		self.client.login(username='kuldeeprishi', password="password")

		# Delete the tag
		response = self.client.post('/admin/blogengine/tag/1/delete/', {
		    'post': 'yes'
		}, follow=True)
		self.assertEquals(response.status_code, 200)

		# Check deleted successfully
		self.assertTrue('deleted successfully' in response.content)

		# Check tag deleted
		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 0)

class PostTest(TestCase):
	def test_create_category(self):
		category = Category()
		category.name = 'python'
		category.description = 'The python programming language'
		category.save()

		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 1)
		only_category = all_categories[0]
		self.assertEquals(only_category, category)

		self.assertEquals(only_category.name, 'python')
		self.assertEquals(only_category.description, 'The python programming language')


	def test_create_post(self):
		category = Category()
		category.name = 'python'
		category.description = 'The python programming language'
		category.save()

		tag = Tag()
		tag.name = 'python'
		tag.description = 'The python programming language'
		tag.save()

		# Create the author
		author = User.objects.create_user('testuser', 'user@example.com', 'password')
		author.save()

		# Create the site
		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		# Create a test post
		post = Post()
		post.title = "Test post title"
		post.text = "This is body of test post"
		post.slug = 'test-post-title'
		post.pub_date = timezone.now()
		post.author = author
		post.site = site
		post.category = category
		post.save()

		post.tags.add(tag)
		post.save()

		# Check post created
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Check attributes
		self.assertEquals(only_post.title, "Test post title")
		self.assertEquals(only_post.text, "This is body of test post")
		self.assertEquals(only_post.slug, "test-post-title")
		self.assertEquals(only_post.site.name, 'example.com')
		self.assertEquals(only_post.site.domain, 'example.com')
		self.assertEquals(only_post.pub_date.day, post.pub_date.day)
		self.assertEquals(only_post.pub_date.month, post.pub_date.month)
		self.assertEquals(only_post.pub_date.year, post.pub_date.year)
		self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
		self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
		self.assertEquals(only_post.pub_date.second, post.pub_date.second)
		self.assertEquals(only_post.author.username, 'testuser')
		self.assertEquals(only_post.author.email, 'user@example.com')
		self.assertEquals(only_post.category.name, 'python')
		self.assertEquals(only_post.category.description, 'The python programming language')

		post_tags = only_post.tags.all()
		self.assertEquals(len(post_tags), 1)
		only_post_tag = post_tags[0]
		self.assertEquals(only_post_tag, tag)
		self.assertEquals(only_post_tag.name, 'python')
		self.assertEquals(only_post_tag.description, u'The python programming language')


class AdminTest(BaseAcceptanceTest):
	fixtures = ['users.json']

	def test_create_category(self):
		self.client.login(username='kuldeeprishi', password='password')

		response = self.client.get('/admin/blogengine/category/add/')
		self.assertEquals(response.status_code, 200)

		response = self.client.post('/admin/blogengine/category/add/', {
			'name': 'python',
			'description': 'The python programming language'
			},
			follow=True)
		self.assertEquals(response.status_code, 200)

		self.assertTrue('added successfully' in response.content)

		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 1)

	def test_edit_category(self):
		# Create the category
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		# Log in
		self.client.login(username='kuldeeprishi', password="password")

		# Edit the category
		response = self.client.post('/admin/blogengine/category/1/', {
			'name': 'perl',
			'description': 'The Perl programming language'
			}, follow=True)
		self.assertEquals(response.status_code, 200)

		# Check changed successfully
		self.assertTrue('changed successfully' in response.content)

		# Check category amended
		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 1)
		only_category = all_categories[0]
		self.assertEquals(only_category.name, 'perl')
		self.assertEquals(only_category.description, 'The Perl programming language')

	def test_delete_category(self):
		# Create the category
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		# Log in
		self.client.login(username='kuldeeprishi', password="password")

		# Delete the category
		response = self.client.post('/admin/blogengine/category/1/delete/', {
			'post': 'yes'
		}, follow=True)
		self.assertEquals(response.status_code, 200)

		# Check deleted successfully
		self.assertTrue('deleted successfully' in response.content)

		# Check category deleted
		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 0)

	def test_login(self):
		# Get login page
		response = self.client.get('/admin/')

		# Check response code
		self.assertEquals(response.status_code, 200)

		# Check 'Log in' in response
		self.assertTrue('Log in' in response.content)

		# Log the user in
		self.client.login(username='kuldeeprishi', password='password')

		# Check response code
		response = self.client.get('/admin/')
		self.assertEquals(response.status_code, 200)

		# Check 'Log out' in response
		self.assertTrue('Log out' in response.content)

	def test_logout(self):
		self.client = Client()
		self.client.login(username='kuldeeprishi', password="password")

		response = self.client.get('/admin/')
		self.assertEquals(response.status_code, 200)

		self.assertTrue('Log out' in response.content)

		self.client.logout()

		response = self.client.get('/admin/')
		self.assertEquals(response.status_code, 200)
		self.assertTrue('Log in' in response.content)

	def test_create_post(self):
		# Create the category
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		# Create the tag
		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		self.client.login(username="kuldeeprishi", password="password")

		response = self.client.get('/admin/blogengine/post/add/')
		self.assertEquals(response.status_code, 200)

		# Create a new post
		response = self.client.post('/admin/blogengine/post/add/', {
				'title': 'Test post title',
				'text': 'This is body of test post',
				'pub_date_0': '2014-03-16',
				'pub_date_1': '00:00:12',
				'slug' : 'test-post-title',
				'site': '1',
				'category': '1',
				'tags': '1'
			},
			follow=True
			)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('added successfully' in response.content)

		# Check new post in database
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

	def test_edit_post(self):
		# Create the category
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		# Create the author
		author = User.objects.create_user('testuser', 'user@example.com', 'password')
		author.save()

		# Create the site
		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		# Create the post
		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.slug = 'test-post-title'
		post.pub_date = timezone.now()
		post.author = author
		post.site = site
		post.save()
		post.tags.add(tag)
		post.save()
		
		# Log in
		self.client.login(username='kuldeeprishi', password="password")

		# Edit the post
		response = self.client.post('/admin/blogengine/post/1/', {
			'title': 'My second post',
			'text': 'This is my second blog post',
			'pub_date_0': '2013-12-28',
			'pub_date_1': '22:00:04',
			'slug': 'my-second-post',
			'site': '1',
			'category': '1',
			'tags': '1'
		},
		follow=True
		)
		self.assertEquals(response.status_code, 200)

		# Check changed successfully
		self.assertTrue('changed successfully' in response.content)

		# Check post amended
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post.title, 'My second post')
		self.assertEquals(only_post.text, 'This is my second blog post')

	def test_delete_post(self):
		# Create the category
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		author = User.objects.create_user('testuser', 'user@example.com', 'password')
		author.save()

		# Create the site
		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		# Create the post
		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.slug = 'test-post-title'
		post.pub_date = timezone.now()
		post.site = site
		post.author = author
		post.category = category
		post.save()
		post.tags.add(tag)
		post.save()

		# Check new post saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

		# Log in
		self.client.login(username='kuldeeprishi', password="password")

		# Delete the post
		response = self.client.post('/admin/blogengine/post/1/delete/', {
			'post': 'yes'
		}, follow=True)
		self.assertEquals(response.status_code, 200)

		# Check deleted successfully
		self.assertTrue('deleted successfully' in response.content)

		# Check post amended
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 0)


class PostViewTest(BaseAcceptanceTest):
	def test_index(self):
		# Create the category
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		# Tag
		tag = Tag()
		tag.name = 'perl'
		tag.description = 'the perl programming'
		tag.save()

		author = User.objects.create_user('testuser', 'user@example.com', 'password')
		author.save()

		# Create the site
		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		# Create the post
		post = Post()
		post.title = 'My first post'
		post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
		post.slug = 'my-first-post'
		post.pub_date = timezone.now()
		post.author = author
		post.site = site
		post.category = category
		post.save()
		post.tags.add(tag)
		post.save()

		# Check new post saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

		# Fetch the index
		response = self.client.get('/')
		self.assertEquals(response.status_code, 200)

		# Check post title in response
		self.assertTrue(post.title in response.content)

		self.assertTrue(markdown.markdown(post.text) in response.content)

		self.assertTrue(post.category.name in response.content)

		post_tag = all_posts[0].tags.all()[0]
		self.assertTrue(post_tag.name in response.content)

		self.assertTrue(str(post.pub_date.year) in response.content)
		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.pub_date.day) in response.content)

		# Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

	def test_post_page(self):
		# Create the category
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		# Tag
		tag = Tag()
		tag.name = 'perl'
		tag.description = 'the perl programming'
		tag.save()

		author = User.objects.create_user('testuser', 'user@example.com', 'password')
		author.save()

		# Create the site
		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		post = Post()
		post.title = 'My first post'
		post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
		post.slug = 'my-first-post'
		post.pub_date = timezone.now()
		post.author = author
		post.site = site
		post.category = category
		post.save()
		post.tags.add(tag)
		post.save()

		# Check new post saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Get the post URL
		post_url = only_post.get_absolute_url()

		# Fetch the post
		response = self.client.get(post_url)
		self.assertEquals(response.status_code, 200)

		# Check the post title is in the response
		self.assertTrue(post.title in response.content)

		self.assertTrue(post.category.name in response.content)

		post_tag = all_posts[0].tags.all()[0]
		self.assertTrue(post_tag.name in response.content)

		# Check the post text is in the response
		self.assertTrue(markdown.markdown(post.text) in response.content)

		# Check the post date is in the response
		self.assertTrue(str(post.pub_date.year) in response.content)
		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.pub_date.day) in response.content)

		# Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)
	
	def test_category_page(self):
		# Create the category
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		# Create the author
		author = User.objects.create_user('testuser', 'user@example.com', 'password')
		author.save()

		# Create the site
		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		# Create the post
		post = Post()
		post.title = 'My first post'
		post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
		post.slug = 'my-first-post'
		post.pub_date = timezone.now()
		post.author = author
		post.site = site
		post.category = category
		post.save()

		# Check new post saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Get the category URL
		category_url = post.category.get_absolute_url()
		
		# Fetch the category
		response = self.client.get(category_url)
		self.assertEquals(response.status_code, 200)

		# Check the category name is in the response
		self.assertTrue(post.category.name in response.content)

		# Check the post text is in the response
		self.assertTrue(markdown.markdown(post.text) in response.content)

		# Check the post date is in the response
		self.assertTrue(str(post.pub_date.year) in response.content)
		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.pub_date.day) in response.content)

		# Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

	def test_tag_page(self):
		# Create the tag
		tag = Tag()
		tag.name = 'python'
		tag.description = 'The Python programming language'
		tag.save()

		# Create the author
		author = User.objects.create_user('testuser', 'user@example.com', 'password')
		author.save()

		# Create the site
		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		# Create the post
		post = Post()
		post.title = 'My first post'
		post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
		post.slug = 'my-first-post'
		post.pub_date = timezone.now()
		post.author = author
		post.site = site
		post.save()
		post.tags.add(tag)

		# Check new post saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Get the tag URL
		tag_url = post.tags.all()[0].get_absolute_url()

		# Fetch the tag
		response = self.client.get(tag_url)
		self.assertEquals(response.status_code, 200)

		# Check the tag name is in the response
		self.assertTrue(post.tags.all()[0].name in response.content)

		# Check the post text is in the response
		self.assertTrue(markdown.markdown(post.text) in response.content)

		# Check the post date is in the response
		self.assertTrue(str(post.pub_date.year) in response.content)
		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.pub_date.day) in response.content)

		# Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)


class FlatPageViewTest(BaseAcceptanceTest):
	def test_create_flat_page(self):
		page = FlatPage()
		page.url = '/about/'
		page.title = 'About me'
		page.content = 'All about me'
		page.save()

		# Add the site
		page.sites.add(Site.objects.all()[0])
		page.save()

		# Check new page saved
		all_pages = FlatPage.objects.all()
		self.assertEquals(len(all_pages), 1)
		only_page = all_pages[0]
		self.assertEquals(only_page, page)

		# Check data correct
		self.assertEquals(only_page.url, '/about/')
		self.assertEquals(only_page.title, 'About me')
		self.assertEquals(only_page.content, 'All about me')

		page_url = only_page.get_absolute_url()

		response = self.client.get(page_url)
		self.assertEquals(response.status_code, 200)

		self.assertTrue('About me' in response.content)
		self.assertTrue('All about me' in response.content)
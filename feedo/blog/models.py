from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

# менеджер для получения опубликованных постов
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,self).get_queryset().filter(status='published')


class Post(models.Model):
	STATUS_CHOICES = (
		('draft','Draft'),
		('published','Published')
	)

	# поля модели

	title 	= models.CharField(max_length=50)
	slug 	= models.SlugField(max_length=50, unique_for_date='publish')
	author 	= models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_post')
	content = models.TextField(null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	publish = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	status 	= models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

	# managers

	objects = models.Manager()
	published = PublishedManager()
	tags = TaggableManager()

	class Meta:
		ordering = ('-publish',)

	def get_absolute_url(self):
		return reverse('blog:post', args=[
			self.publish.year,
			self.publish.month,
			self.publish.day,
			self.slug
		])

	def get_comments_number(self):
		return len(self.comments.filter(active=True))

	def get_excerpt(self):
		content = self.content
		return content[:250]+('...' if len(content)>100 else '')

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Post,
		on_delete=models.CASCADE,
		related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return f'Comment by {self.name} on {self.post}'










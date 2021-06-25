from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])

    class Meta:
        ordering = ('-publish',)
        db_table = 'Posts'
        managed = True
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(("name"), max_length=50)
    email = models.EmailField(("email"))
    body = models.TextField(("body"))
    created = models.DateTimeField(("created"), auto_now_add=True)
    updated = models.DateTimeField(("updated"), auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment By {self.name} on {self.post}'

    class Meta:
        ordering = ('created',)
        db_table = 'comment'
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

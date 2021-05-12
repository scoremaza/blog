from django.db import models
from django.db.models.base import Model
from django.urls import reverse
from django.db.models.fields import CharField, SlugField, TextField
from django.utils import timezone
from django .contrib.auth.models import User

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset()\
                         .filter(status='published')

class CreationalManager(models.Manager):
    def get_queryset(self):
        return super(CreationalManager,
                     self).get_queryset()\
                     .filter(pattern='creational-pattern')

class StructuralManager(models.Manager):
    def get_queryset(self):
        return super(StructuralManager,
                     self).get_queryset()\
                     .filter(pattern='strutural-pattern')

class BehavioralManager(models.Manager):
    def get_queryset(self):
        return super(BehavioralManager,
                     self).get_queryset()\
                     .filter(pattern='behavioral-pattern')

class Post( models.Model):
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    PATTERN_CLASSIFICATION   = (
        ('creational-pattern', 'Creational Pattern'),
        ('structural-pattern', 'Structural Pattern'),
        ('behavioral-pattern', 'Behavioral Pattern')
    )

    title          =  models.TextField(max_length=150)
    slug           =  models.SlugField(max_length=250,
                                      unique_for_date='publish')
    author         =  models.ForeignKey(User, 
                                        on_delete=models.CASCADE,
                                        related_name='blog_posts')
    description1   =  models.TextField()
    description2   =  models.TextField()
    description3   =  models.TextField()
    intent         =  models.TextField()
    publish        =  models.DateTimeField(default=timezone.now)
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)
    status         = models.CharField(max_length=10,
                                      choices=STATUS_CHOICES,
                                      default='draft')
    pattern        = models.CharField(max_length=50,
                                      choices=PATTERN_CLASSIFICATION,
                                      default= 'creational-pattern') 

    objects    = models.Manager() # The default manager.
    published  = PublishedManager() # Our custom manager.
    creational = CreationalManager() # Our custom manager.
    structural = StructuralManager() # Our custom manager.
    behavioral = BehavioralManager() # Our custom manager. 
    
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", 
                        args=[self.publish.year,
                              self.publish.month,
                              self.publish.day, self.slug])

class Comment(models.Model):
    '''
    Models to Save Comments 
    '''

    post    = models.ForeignKey(Post,
                                on_delete=models.CASCADE,
                                related_name='comments')
    name    = models.CharField(max_length=150)
    email   = models.EmailField()
    body    = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active  = models.BooleanField(default=True)

    class Meta:
        db_table = 'comment'
        ordering = ('created',)
        managed = True
        verbose_name = '\comment'
        verbose_name_plural = '\comments'

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


    

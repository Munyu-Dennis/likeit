from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse
from django.db.models import Q

# Create your models here.


class PostManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | Q(content__icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs

class Post(models.Model):
    author = models.CharField(max_length=100, blank=True)
    link  = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    slug = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    objects = PostManager()

    def __str__(self):
        return self.title

class Prefrances(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)+ ':' + str(self.post) + ':' + str(self.value)
    class Meta:
        unique_together = ("user", "post", "value")

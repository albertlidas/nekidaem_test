from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
# Create your models here.


class Blog(models.Model):
    author = models.OneToOneField(
        verbose_name="user",
        to=User, on_delete=models.CASCADE
    )
    followed = models.ManyToManyField(
        verbose_name="followers",
        to=User, related_name="followers", blank=True
    )

    class Meta:
        verbose_name = "blog"
        verbose_name_plural = "blogs"

    def __str__(self):
        return "{}".format(self.author.username)

    def follow_blog(self, user):
        self.followed.add(user)

    def unfollow_blog(self, user):
        self.followed.remove(user)


class Post(models.Model):
    blog = models.ForeignKey(to=Blog, related_name="blog_post")
    title = models.CharField(max_length=60)
    text = models.TextField(
        validators=[MaxLengthValidator(2000)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.title)

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
# Create your models here.


class Blog(models.Model):
    author = models.OneToOneField(
        verbose_name="user",
        to=User, on_delete=models.CASCADE
    )
    followers = models.ManyToManyField(
        verbose_name="followers",
        to=User, related_name="followers", blank=True
    )

    class Meta:
        verbose_name = "blog"
        verbose_name_plural = "blogs"

    def __str__(self):
        return "{}".format(self.author.username)

    def follow_blog(self, user):
        self.followers.add(user)

    def unfollow_blog(self, user):
        self.followers.remove(user)


class Post(models.Model):
    blog = models.ForeignKey(to=Blog, related_name="blog_post")
    title = models.CharField(max_length=60)
    text = models.TextField(
        validators=[MaxLengthValidator(2000)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(to=Blog, related_name="read_by", blank=True)

    def __str__(self):
        return "{}".format(self.title)

    def read_post(self, user):
        self.read_by.add(user)

    def unread_post(self, user):
        self.read_by.remove(user)


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail


@receiver(post_save, sender=Post)
def send_notification(instance, **kwargs):
    if kwargs['created']:
        followers = instance.blog.followers.all()
        emails = [blog.email for blog in followers]

        from_email = "test@gmail.com"
        email_body = "http://link_for_post.com"
        mail_tuple = ("New post in followed posts", email_body, from_email,  emails)
        send_mass_mail((mail_tuple,))

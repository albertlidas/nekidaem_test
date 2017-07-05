from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import TemplateView
from .models import Blog, Post
# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            current_blog = Blog.objects.get(author=self.request.user)
        except (ObjectDoesNotExist, TypeError):
            current_blog = None
        if self.request.user.is_authenticated() and current_blog:
            followed_posts = Post.objects.filter(blog__followers=current_blog.author)
            context['current_blog'] = current_blog
            context['followed_posts'] = followed_posts.order_by('-pub_date')
            context['followers'] = Blog.objects.all().filter(followers=current_blog.author)
            context['blogs'] = Blog.objects.all().exclude(followers=current_blog.author).exclude(author=current_blog.author)
            return context
        else:
            context['login_please'] = True
            return context

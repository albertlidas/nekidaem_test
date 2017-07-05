from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.views.generic.base import TemplateView

from .models import Blog, Post


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


class FollowBlogAPI(View):

    def get(self, request):
        current_blog = get_object_or_404(Blog, author=request.user)

        follow_blog_id = request.GET.get('follow_blog_id')
        unfollow_blog_id = request.GET.get('unfollow_blog_id')
        if follow_blog_id:
            blog = get_object_or_404(Blog, pk=follow_blog_id)
            blog.follow_blog(current_blog.author)
            return HttpResponse(status=200)
        if unfollow_blog_id:
            blog = get_object_or_404(Blog, pk=unfollow_blog_id)
            blog.unfollow_blog(current_blog.author)
            return HttpResponse(status=200)

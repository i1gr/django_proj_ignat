from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from rest_framework import generics

from news.forms import AddingNewsForm, NewsCommentForm, LikeForm
from news.models import News
from news.serializer import NewsSerializer
from news.services.services import get_unique_slug
from service.models import Services
# Create your views here.
from service.services import get_notifications_count


def home(request):
    services = Services.objects.all()
    context = dict()

    context.update(get_notifications_count(request.user))
    context.update({"title": 'Home page', 'nav_active': 'home', 'services': services, 'block_content': 'full_screen', })
    return render(request, 'news/home.html', context=context)


class NewsPage(ListView):
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news'
    extra_context = {"title": 'News page', 'nav_active': 'news'}
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_notifications_count(self.request.user))
        return context


def article(request, article_slug):
    article_data = get_object_or_404(News.objects.select_related('author'), slug=article_slug)
    comments = article_data.newscomments_set.all().select_related('author')

    user = request.user
    form = None
    like_form = None
    context = dict()

    context.update(get_notifications_count(request.user))

    if user.is_authenticated:
        if request.method == "POST":
            form = NewsCommentForm(request.POST)
            like_form = LikeForm(article_data, user, request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = user
                comment.news = article_data
                comment.save()
                a = article_slug
                return redirect(to='article', article_slug=article_slug)
            if like_form.is_valid():
                like = like_form.cleaned_data['like']
                if like:
                    article_data.users_who_liked.add(user)
                    article_data.save()
                else:
                    article_data.users_who_liked.remove(user)
                    article_data.save()
        else:
            form = NewsCommentForm()
            like_form = LikeForm(article_data, user)

    context.update({
        'title': f'{article_data.title}',
        'nav_active': 'news',
        'article_data': article_data,
        'form': form,
        'like_form': like_form,
        'comments': comments,
        'block_content': 'full_screen',
    })
    return render(request, 'news/article.html', context=context)


@login_required
def add_news(request):
    user = request.user
    context = dict()

    context.update(get_notifications_count(request.user))

    if not user.is_staff:
        raise PermissionDenied

    if request.method == "POST":
        form = AddingNewsForm(user, request.POST)
        if form.is_valid():
            new_news = form.save(commit=False)
            new_news.slug = get_unique_slug(new_news, new_news.title)
            new_news.save()
            return redirect('news')
    else:
        form = AddingNewsForm(user)

    context.update({
        'title': 'Create news',
        'nav_active': 'news',
        'form': form,
    })

    return render(request, 'news/add_news.html', context=context)


class NewsInProfileView(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            return News.objects.filter(author=current_user)
        return None


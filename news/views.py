from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, FormView, CreateView

from news.forms import AddingNewsForm, NewsCommentForm
from news.models import News, NewsComments
from news.services.services import get_unique_slug, get_user_from_instance, change_stars_grading
from service.models import Services


# Create your views here.


def home(request):
    services = Services.objects.all()
    return render(request, 'news/home.html', {"title": 'Home page', 'nav_active': 'home', 'services': services})


# def news(request):
#     all_news = News.objects.all()
#     return render(request, 'news/news.html', {"title": 'News page', 'nav_active': 'news', "news": all_news})


class NewsPage(ListView):
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news'
    extra_context = {"title": 'News page', 'nav_active': 'news'}
    paginate_by = 5


def article(request, article_slug):
    article_data = get_object_or_404(News.objects.select_related('author'), slug=article_slug)
    # comments = NewsComments.objects.filter(news=article_data)
    comments = article_data.newscomments_set.all().select_related('author')

    user = request.user
    form = None

    if user.is_authenticated:
        if request.method == "POST":
            form = NewsCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = user
                comment.news = article_data
                comment.save()
                form = NewsCommentForm()
                change_stars_grading(article_data)
        else:
            form = NewsCommentForm()

    context = {
        'title': f'{article_data.title}',
        'nav_active': 'news',
        'article_data': article_data,
        'form': form,
        'comments': comments,
    }
    return render(request, 'news/article.html', context=context)


class ArticleObject():
    news_instance = None


class ArticleDisplay(DetailView):
    model = News
    template_name = 'news/article.html'
    slug_url_kwarg = 'article_slug'
    extra_context = {'nav_active': 'news'}
    context_object_name = 'article_data'
    paginate_by = 1
    # ArticleObject.news_instance = model
    # print(model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['article_data'].title
        context['comments'] = self.object.newscomments_set.all()
        ArticleObject.news_instance = context['article_data']
        # context['form'] = NewsCommentForm()
        return context


class ArticleCommentsListView(ListView):
    model = NewsComments
    template_name = 'news/news.html'
    context_object_name = 'comments'
    paginate_by = 5


class ArticleCommentsForm(CreateView):
    model = NewsComments
    template_name = 'news/article.html'
    form_class = NewsCommentForm
    success_url = ''
    def form_valid(self, form, *args, **kwargs):
        # self.object = self.get_object()
        self.object = form.save(commit=False)
        print(
            '=========================================================================================================')
        print(type(ArticleObject.news_instance))
        print(ArticleObject.news_instance)
        print(
            '=========================================================================================================')
        self.object.author = self.request.user
        self.success_url = ArticleObject.news_instance.get_absolute_url()
        self.object.news = ArticleObject.news_instance
        self.object.save()

        change_stars_grading(self.object.news)

        return super().post(self.request, *args, **kwargs)


    # def get_initial(self, *args, **kwargs):
    #     initial = super().get_initial(**kwargs)
    #     return initial

    # def post(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return None
    #     print(
    #         '=========================================================================================================')
    #     print(self.__dict__)
    #     print(
    #         '=========================================================================================================')
    #     self.object = self.get_object()
    #     print(
    #         '=========================================================================================================')
    #     print(self.object)
    #     print(
    #         '=========================================================================================================')
    #     self.object.author = request.user
    #
    #     self.object.news = self.model.news
    #     change_stars_grading(self.object.news)
    #
    #     return super().post(request, *args, **kwargs)

    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     user = form.request.user
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.author = user
    #         comment.news = article_data
    #         comment.save()
    #         form = NewsCommentForm()
    #         change_stars_grading(article_data)
    #     form.send_email()
    #     return super().form_valid(form)


class ArticlePage(View):
    def get(self, request, *args, **kwargs):
        view = ArticleDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ArticleCommentsForm.as_view()
        return view(request, *args, **kwargs)


@login_required
def add_news(request):
    user = request.user

    if not user.is_staff:
        raise PermissionDenied

    if request.method == "POST":
        form = AddingNewsForm(user, request.POST)
        if form.is_valid():
            new_news = form.save(commit=False)
            new_news.slug = get_unique_slug(new_news)
            new_news.save()
            return redirect('news')
    else:
        form = AddingNewsForm(user)

    context = {
        'title': 'Create news',
        'nav_active': 'news',
        'form': form,
    }

    return render(request, 'news/add_news.html', context=context)

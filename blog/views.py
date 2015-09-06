from django.shortcuts import render, get_object_or_404, render_to_response
from django.views import generic
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import password_change
from django.utils.decorators import method_decorator
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Article, Comment
from .forms import LoginForm, BlogRegistrationForm, ArticleForm, CommentForm, MyFormView, SearchForm


class BlogIndexView(generic.ListView):
    template_name = 'blog/blog_index.html'
    context_object_name = 'latest_articles_list'

    def get_context_data(self, **kwargs):
        context = super(BlogIndexView, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        context.update(csrf(self.request))
        return context

    #return articles sorted by date
    def get_queryset(self):
        return Article.objects.order_by('-pub_date')


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'blog/article.html'
    pk_url_kwarg = 'article_id'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['comment_form'] = CommentForm()
        context['search_form'] = SearchForm()
        context.update(csrf(self.request))
        return context


class NewArticleView(FormView):
    """ For creating new article/ Available only for registered users
    """
    template_name = 'blog/new_article.html'
    form_class = ArticleForm
    success_url = '/blog/'

    @method_decorator(login_required(login_url='/blog/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super(NewArticleView, self).dispatch(*args, **kwargs)

    # def get(self, request):
    #     args = {}
    #     args.update(csrf(request))
    #     # return render(request, self.template_name, c)
    #     return super(NewArticleView, self).get(args)

    def form_valid(self, form):
        #form.save()
        new_article = Article()
        new_article.headline = self.request.POST.get('headline', '')
        new_article.content = self.request.POST.get('content', '')
        new_article.pub_date = timezone.now()
        new_article.author = self.request.user
        new_article.save()
        return HttpResponseRedirect(reverse('blog:index'))


class ArticleUpdateView(UpdateView):
    """ For editing article by certain user. Available only for registered users
    """
    model = Article
    fields = ['headline', 'content']
    template_name = 'blog/article_update.html'
    success_url = '/blog/user_articles/'
    pk_url_kwarg = 'article_id'

    @method_decorator(login_required(login_url='/blog/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super(ArticleUpdateView, self).dispatch(*args, **kwargs)


@login_required(login_url='/blog/accounts/login')
def article_like_view(request, article_id):
    if request.user.is_authenticated():
        if article_id:
            a = Article.objects.get(pk=article_id)
            a.likes += 1
            a.save()
        return HttpResponseRedirect(reverse('blog:article_detail', args=[article_id]))


@login_required(login_url='/blog/accounts/login')
def article_delete_view(request, article_id):
    if request.user.is_authenticated():
        if article_id:
            article = Article.objects.get(pk=article_id)
            article.delete()
            return HttpResponseRedirect(reverse('blog:user_articles'))


@login_required(login_url='/blog/accounts/login')
def comment_like_view(request, comment_id):
    if request.user.is_authenticated():
        if comment_id:
            c = Comment.objects.get(pk=comment_id)
            c.likes += 1
            c.save()
            article_id = str(c.article_id)
    return HttpResponseRedirect(reverse('blog:article_detail', args=[article_id]))


@login_required(login_url='/blog/accounts/login')
def comment_add_view(request, article_id):
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment()
            new_comment.author = request.user
            new_comment.content = request.POST.get('content')
            article = get_object_or_404(Article, pk=article_id)
            new_comment.article = article
            new_comment.save()
            return HttpResponseRedirect(reverse('blog:article_detail', args=[article_id]))
        else:
            return HttpResponseRedirect(reverse('blog:article_detail', args=[article_id]))
    else:
        return HttpResponseRedirect(reverse('blog:article_detail', args=[article_id]))


class UserLoginView(FormView):
    template_name = 'blog/login.html'
    form_class = LoginForm
    success_url = '/blog/accounts/profile/'

    # def get(self, request):
    #     args = {}
    #     args.update(csrf(request))
    #     # return render(request, self.template_name, c)
    #     return super(UserLoginView, self).get(args)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        username = self.request.POST.get('username', '')
        password = self.request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(self.request, user)
                return super(UserLoginView, self).form_valid(form)
        else:
            return render(self.request, "blog/invalid.html")


class UserRegisterView(MyFormView):
    template_name = 'blog/register.html'
    form_class = BlogRegistrationForm
    success_url = '/blog/accounts/register_success/'

    # def get(self, request):
    #     args = {}
    #     args.update(csrf(request))
    #     # return render(request, self.template_name, c)
    #     return super(UserRegisterView, self).get(args)

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        #context['search_form'] = SearchForm()
        context.update(csrf(self.request))
        return context

    def form_valid(self, form):
        form.save()
        return super(UserRegisterView, self).form_valid(form)


class UserUpdateView(UpdateView):
    model = User

    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'blog/user_update.html'
    success_url = '/blog/accounts/profile/'

    @method_decorator(login_required(login_url='/blog/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated():
            user = User.objects.get(pk=self.request.user.id)
            return user


@login_required(login_url='/blog/accounts/login')
def user_profile_view(request):
    if request.user.is_authenticated():
        return render(request, "blog/profile.html", {'user': request.user})


@login_required(login_url='/blog/accounts/login')
def password_change_view(request):
    return password_change(request, template_name='blog/password_change.html',
                           post_change_redirect=reverse('blog:user_profile'))


class UserArticlesView(generic.ListView):
    template_name = 'blog/user_articles.html'
    context_object_name = 'user_articles_list'

    @method_decorator(login_required(login_url='/blog/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super(UserArticlesView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        articles = Article.objects.filter(author__username=self.request.user)
        return articles.order_by('-pub_date')


def user_logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('blog:index'))


def articles_search_view(request):
    if request.method == 'POST' and request.POST['search_text'] != '':
        search_text = request.POST['search_text']
    else:
        articles = {}
        return render_to_response('blog/search_articles.html', {'articles': articles})

    articles = Article.objects.filter(headline__icontains=search_text)
    # return render(request, 'blog/search_articles.html', {'articles': articles})
    return render_to_response('blog/search_articles.html', {'articles': articles})

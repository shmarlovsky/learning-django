from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # ex: /blog/
    url(r'^$', views.BlogIndexView.as_view(), name='index'),
    # ex: /blog/5/
    url(r'^(?P<article_id>[0-9]+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
    url(r'^new_article/$', views.NewArticleView.as_view(), name='new_article'),
    url(r'^accounts/login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^add_comment/(?P<article_id>[0-9]+)$', views.comment_add_view, name='comment_add'),
    url(r'^like_article/(?P<article_id>[0-9]+)$', views.article_like_view, name='article_like'),
    url(r'^like_comment/(?P<comment_id>[0-9]+)$', views.comment_like_view, name='comment_like'),
    url(r'^edit_article/(?P<article_id>[0-9]+)$', views.ArticleUpdateView.as_view(), name='article_update'),
    url(r'^user_articles/$', views.UserArticlesView.as_view(),name='user_articles'),
    url(r'^delete_article/(?P<article_id>[0-9]+)$',views.article_delete_view, name='article_delete'),
    url(r'^accounts/logout/$', views.user_logout_view, name='logout'),
    #url(r'^accounts/auth/', views.LoginView.as_view(), name='auth'),
    url(r'^accounts/profile/$', views.user_profile_view, name='user_profile'),
   # url(r'^account/edit_profile/(?P<pk>[0-9]+)$', views.UserUpdateView.as_view(), name='user_update'),
    url(r'^accounts/edit_profile/$', views.UserUpdateView.as_view(), name='user_update'),
    url(r'^accounts/password_change/$', views.password_change_view, name='password_change'),
    url(r'^accounts/invalid/$', views.UserLoginView.as_view(), name='login_invalid'),
    url(r'^accounts/register/$', views.UserRegisterView.as_view(), name='user_register'),
    url(r'^accounts/register_success/$', TemplateView.as_view(template_name="blog/register_success.html"), name='register_success'),
    url(r'^search/$', views.articles_search_view, name='articles_search')
    # temp
    #url(r'^your-name/', views.get_name, name = 'get_name'),
    #url(r'^thanks/', views.thanks_for_name),
    #url(r'^contact/', views.contact),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    ]

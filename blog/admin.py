from django.contrib import admin

# Register your models here.
from .models import Article, Comment

class CommentAdmin(admin.TabularInline):
	model = Comment
	extra = 0

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Article', {'fields': ['headline', 'content', 'author', 'pub_date']}),
    ]
    inlines = [CommentAdmin]

admin.site.register(Article, ArticleAdmin)
#admin.site.register(Comment)

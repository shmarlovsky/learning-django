from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import Article, Comment
from django.forms import widgets
from django.views.generic.edit import FormView

class MyFormView(FormView):
    error_css_class = 'class-error'
    required_css_class = 'class-required'

    def __init__(self, *args, **kwargs):
        super(MyFormView, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        #for field in self.fields:
        #    self.fields[field].widget.attrs['class'] = 'some-class other-class'

    def as_div(self):
        return self._html_output(
            normal_row = u'<div%(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</div>',
            error_row = u'<div class="error">%s</div>',
            row_ender = '</div>',
            help_text_html = u'<div class="help-text">%s</div>',
            errors_on_separate_row = False)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class ArticleForm(forms.ModelForm):
    headline = forms.CharField()
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 10}), label='Content')
    class Meta:
        model = Article
        fields = ['headline', 'content']

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 4}), label='')
    class Meta:
        model = Comment
        fields = ['content']
        # widgets = {
        #     'content': forms.Textarea(attrs={'cols': 40, 'rows': 4}),
        # }

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(max_length=30, label="Password", widget=forms.PasswordInput)

class BlogRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    # error_messages = {
    #     'password_mismatch': _("The two password fields didn't match."),
    # }

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    # def as_div(self):
    #     return self._html_output(
    #         normal_row = u'<div%(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</div>',
    #         error_row = u'<div class="error">%s</div>',
    #         row_ender = '</div>',
    #         help_text_html = u'<div class="help-text">%s</div>',
    #         errors_on_separate_row = False)

    def save(self, commit=True):
        user=super(BlogRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class SearchForm(forms.Form):
    search = forms.CharField()
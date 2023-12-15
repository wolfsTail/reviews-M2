from django import forms
from .models import Post, Comment
from django_recaptcha.fields import ReCaptchaField


class PostCreateForm(forms.ModelForm):

    recaptcha = ReCaptchaField()

    class Meta:
        model = Post
        fields = ('title', 'slug', 'category', 'description', 'text', 'thumbnail', 'status', 'recaptcha',)

    def __init__(self, *args, **kwargs):
        """
        Добавление стилей - Bootstrap5
        """        
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class PostUpdateForm(PostCreateForm):

    class Meta:
        model = Post
        fields = PostCreateForm.Meta.fields + ('updater', 'fixed')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fixed'].widget.attrs.update({'class': 'form-check-input'})


class CommentCreateForm(forms.ModelForm):

    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'cols': 30, 'rows': 5, 'placeholder': 'Введите комментарий', 'class': 'form-control'}))
    recaptcha = ReCaptchaField()

    class Meta:
        model = Comment
        fields = ('content', 'recaptcha',)

from django import forms
from .utils import get_input_attrs
from .models import Comment

class EmailPostForm(forms.Form):
	attrs = {'class':'form-control'}

	name = forms.CharField(max_length=25,widget=forms.TextInput(attrs=get_input_attrs('Name')))
	email = forms.EmailField(widget=forms.EmailInput(attrs=get_input_attrs('Email')))
	to = forms.EmailField(widget=forms.EmailInput(attrs=get_input_attrs('To')))
	comments = forms.CharField(required=False,widget=forms.Textarea(attrs=get_input_attrs('Comments')))

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name','email','body')
		widgets = {
			'name': forms.TextInput(attrs=get_input_attrs('Name')),
			'email': forms.EmailInput(attrs=get_input_attrs('Email')),
			'body': forms.Textarea(attrs=get_input_attrs('Comment',classes=['comment-textarea']))
		}
from django import forms
from django.db.models import fields
from .models import Comment

class EmailPostForm(forms.Form):
    name      = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'form-control'}))
    email     = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    to        = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    comments  = forms.CharField(required=False,
                                widget=forms.Textarea(attrs={'class':'form-control'}))

class CommentForm(forms.ModelForm):
    '''
    Form for the Comment section 
    '''
    class Meta:
        model = Comment
        fields = ('name','email','body')
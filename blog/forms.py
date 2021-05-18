from django import forms
from django.forms.fields import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
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
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.helper.label_class = " col-md-8"
        self.helper.field_class = "form-control "
        self.helper.form_method = "post"
        self.helper.form_action = "post_detail"

        self.helper.add_input(Submit('submit', 'Submit'))
    class Meta:
        model = Comment
        fields = ('name','email','body')
    
   
    

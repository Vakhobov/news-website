from django import forms
from .models import Contact, Comment


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

class SubcriptionForm(forms.Form):
    subject = forms.ChoiceField(choices=[('option1', 'Option 1'), ('option2', 'Option 2')])
    message = forms.CharField()
    email = forms.EmailField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']



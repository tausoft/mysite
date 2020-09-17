from django import forms
from django.views.generic import TemplateView, DeleteView
from .models import *
from django.core.validators import *
from multi_email_field.forms import MultiEmailField
from django.db import models
from tinymce import models as tinymce_models
from .views import *
from ckeditor.widgets import CKEditorWidget


class Dekodiranjelist(forms.ModelForm):
    kontakt = forms.CharField(label='kontakt', max_length=20)
    proizvodjac = forms.CharField(label='proizvodjac', max_length=20)
    model = forms.CharField(label='model', max_length=20)
    imei = forms.CharField(label='imei', min_length=15, max_length=15)
    unlock = forms.CharField(label='unlock', max_length=50)
    status = forms.IntegerField(label='status')
    datecreated = forms.DateTimeField(label='datecreated')
    datemodified = forms.DateTimeField(label='datemodified')

class Meta:
    fields = ('kontakt', 'proizvodjac', 'model', 'imei')

class Vendorlist(forms.ModelForm):
    name = forms.CharField(label='name', max_length=20)
    email = forms.CharField(label='subject', max_length=200)
    cc = forms.CharField(label='subject', max_length=200)
    subject = forms.CharField(label='subject', max_length=50)
    mailbody = forms.CharField(label='mailbody', max_length=1000)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

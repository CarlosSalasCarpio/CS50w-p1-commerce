from dataclasses import field
from turtle import width
from xml.dom.minidom import Attr
from xml.etree.ElementTree import Comment
from django import forms
from .models import auctionListingModel, bidsModel, commentsModel

class auctionListingForm(forms.ModelForm):

    class Meta:
        model = auctionListingModel
        fields = ('title', 'description', 'price', 'category', 'image')


class commentsForm(forms.ModelForm):

    comment = forms.CharField(label=False, widget=forms.Textarea)

    class Meta:
        model = commentsModel
        fields = ('comment',)

class bidsForm(forms.ModelForm):

    class Meta:
        model = bidsModel
        fields = ('bid',)
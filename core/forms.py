# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

from django.conf import settings


class ContactForm(forms.Form):
    occupation = forms.CharField(label=_('Occupation'), max_length=128)
    subject = forms.CharField(label=_('Subject'), max_length=128)
    name = forms.CharField(label=_('Name'), max_length=128)
    email = forms.EmailField(label=_('Email'))
    message = forms.CharField(label=_('Message'), max_length=255)

    def send_email(self):
        subject = self.cleaned_data.get('subject')
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        message = self.cleaned_data.get('message')

        recipient_list = ['%s <%s>' % manager for manager in settings.MANAGERS]
        sender = '%s <%s>' % (name, email,)

        send_mail(subject, message, sender, recipient_list, fail_silently=False)

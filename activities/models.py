# -*- coding: utf-8 -*-
import json

from django.db import models
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _
from accounts.models import TimtecUser


class Activity(models.Model):
    """
    Generic class to activities
    Data templates (data e type atributes):
    Multiple choice
        type: multiplechoice
        data: {question: "", choices: ["choice1", "choice2", ...]}
        expected_answer_data: {choices: [0, 2, 5]} # list of espected choices, zero starting
    Single choice
        type: singlechoice
        data: {question: "", choices: ["choice1", "choice2", ...]}
        expected_answer_data: {choice: 1}
    """
    type = models.CharField(_('Type'), max_length=255)
    data = JSONField(_('Data'))
    expected = JSONField(_('Expected answer'))

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
        ordering = [('-id')]

    def question(self):
        try:
            return self.data.get('question')
        except:
            return None

    def __unicode__(self):
        return u'%s dt %s a %s' % (self.type, self.data, self.expected)


class Answer(models.Model):
    activity = models.ForeignKey(Activity, verbose_name=_('Activity'))
    user = models.ForeignKey(TimtecUser, verbose_name=_('Student'))
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    given = JSONField(_('Given answer'))

    @property
    def expected(self):
        if type(self.activity.expected) in [unicode, str]:
            return json.loads(self.activity.expected)
        return self.activity.expected

    def is_correct(self):
        if self.activity.type == 'html5':
            return True

        result = False

        given = self.given
        expected = self.activity.expected

        result = unicode(given) == unicode(expected)
        return result

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
        ordering = ['timestamp']

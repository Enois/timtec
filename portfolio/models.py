__author__ = 'dali'
from django.db import models
from accounts.models import TimtecUser
from core.models import Course,Video
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from django.contrib.staticfiles.storage import staticfiles_storage


class Document(models.Model):
    name = models.CharField(max_length=255)
    document_id = models.CharField(max_length=100)


class PortfolioQuestion(models.Model):

    STATES = (
        ('draft', _('Draft')),
        ('listed', _('Listed')),
        ('published', _('Published')),
    )

    course = models.ForeignKey(Course, related_name='portfolio_questions', verbose_name=_('Course'))
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)
    timestamp = models.DateTimeField(_('Date'), auto_now_add=True)
    video = models.ForeignKey(Video, verbose_name=_('video'), null=True, blank=True)
    document = models.ForeignKey(Document, verbose_name=_('document'), null=True, blank=True)
    status = models.CharField(_('Status'), choices=STATES, default=STATES[0][0], max_length=64)

    def thumbnail(self):
        try:
            vid_portfolio_question = self.video
            thumbnail = 'http://i1.ytimg.com/vi/' + vid_portfolio_question.youtube_id + '/hqdefault.jpg'
            return thumbnail
        except IndexError:
            return staticfiles_storage.url('img/lesson-default.png')
       # except AttributeError:
       #     return staticfiles_storage.url('img/lesson-default.png')


class PortfolioAnswer(models.Model):

    STATES1 = (
        ('draft', _('Draft')),
        ('listed', _('Listed')),
        ('published', _('Published')),
    )
    STATES2 = (
         ('highlight', _('Highlight')),
        ('disparage', _('Disparage')),
    )
    portfolio_question = models.ForeignKey(PortfolioQuestion, verbose_name=_('Portfolio Question'))
    user = models.ForeignKey(TimtecUser, verbose_name=_('Student'))
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    portfolio_answer_video = models.ForeignKey(Video, verbose_name=_('Portfolio answer video'), null=True, blank=True)
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)
    tags = TaggableManager()
    status1 = models.CharField(_('Status'), choices=STATES1, default=STATES1[0][0], max_length=64)
    status2 = models.CharField(_('Status'), choices=STATES2, default=STATES2[0][0], max_length=64)


class Comment(models.Model):
    user = models.ForeignKey(TimtecUser)
    text = models.TextField()
    portfolioAnswer = models.ForeignKey(PortfolioAnswer)
    created_on = models.DateTimeField(auto_now_add=True)


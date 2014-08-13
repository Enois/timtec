__author__ = 'dali'
from django.db import models
from accounts.models import TimtecUser
from core.models import Video
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager


class Portfolio(models.Model):

    STATES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
    )
    user = models.ForeignKey(TimtecUser, verbose_name=_('Student'))
    name = models.CharField(_('Name'), max_length=255, blank=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    timestamp = models.DateTimeField(_('Date'), auto_now_add=True)
    video = models.ForeignKey(Video, verbose_name=_('video'), null=True, blank=True)
    status = models.CharField(_('Status'), choices=STATES, default=STATES[0][0], max_length=64)
    tags = TaggableManager()
    thumbnail = models.ImageField(_('Thumbnail'), upload_to='portfolio_thumbnails', null=True, blank=True)
    home_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Portfolio')
        verbose_name_plural = _('Portfolios')

    def __unicode__(self):
        return self.name

    def get_thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return ''


class Comment(models.Model):
    user = models.ForeignKey(TimtecUser)
    text = models.TextField()
    portfolio = models.ForeignKey(Portfolio)
    created_on = models.DateTimeField(auto_now_add=True)


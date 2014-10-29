# coding: utf-8
from django import forms
from core.models import Video
from portfolio.models import Portfolio
from portfolio.utils import get_youtube_id

class EnoisPortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name', 'video', 'thumbnail', 'description', 'tags', 'home_published')

    new_video = forms.URLField(required=False, label='URL do Vídeo')

    def __init__(self, *args, **kwargs):
        super(EnoisPortfolioForm, self).__init__(*args, **kwargs)
        self.fields['video'].required = False
        self.fields['thumbnail'].label = 'Imagem'

    def clean(self):
        # See http://stackoverflow.com/a/8996801/207119
        video = self.instance.video
        new_video = self.cleaned_data.get('new_video')

        if new_video and not video:
            video = Video.objects.create(
                youtube_id=get_youtube_id(new_video),
                name=self.cleaned_data.get('name', '')
            )

        self.cleaned_data['video'] = video

        return super(EnoisPortfolioForm, self).clean()

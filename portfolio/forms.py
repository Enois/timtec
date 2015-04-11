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
        self.fields['name'].required = True
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

        data = super(EnoisPortfolioForm, self).clean()

        if not (self.cleaned_data['video'] or self.cleaned_data['thumbnail']):
            error_msg = u'Você deve inserir pelo menos o vídeo ou a imagem.'
            self._errors['video'] = self._errors['thumbnail'] = self.error_class([error_msg])
            raise forms.ValidationError(error_msg)

        return data

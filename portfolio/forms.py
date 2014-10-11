from django import forms
from core.models import Video
from portfolio.models import Portfolio
from portfolio.utils import get_youtube_id

class EnoisPortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name', 'video', 'new_video', 'description', 'tags', 'home_published')

    new_video = forms.URLField(required=False, label='Trocar o video')

    def __init__(self, *args, **kwargs):
        super(EnoisPortfolioForm, self).__init__(*args, **kwargs)
        self.fields['video'].required = False

    def clean(self):
        # See http://stackoverflow.com/a/8996801/207119
        video = self.cleaned_data.get('video')
        new_video = self.cleaned_data.get('new_video')

        if not video and not new_video:
            raise forms.ValidationError('Video is required')
        elif not video:
            video = Video.objects.create(youtube_id=get_youtube_id(new_video))
            self.cleaned_data['video'] = video

        return super(EnoisPortfolioForm, self).clean()

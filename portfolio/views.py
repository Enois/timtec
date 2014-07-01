from django.http import Http404
from rest_framework import viewsets
from .models import PortfolioQuestion, PortfolioAnswer
from .serializers import PortfolioQuestionSerializer, PortfolioAnswerSerializer


class PortfolioQuestionViewSet(viewsets.ModelViewSet):
    model = PortfolioQuestion
    serializer_class = PortfolioQuestionSerializer


class PortfolioAnswerViewSet(viewsets.ModelViewSet):
    model = PortfolioAnswer
    serializer_class = PortfolioAnswerSerializer
    filter_fields = ('portfolio_question', 'user',)
    lookup_field = 'portfolio_question'

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        return PortfolioAnswer.objects.filter(user=self.request.user)

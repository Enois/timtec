from rest_framework import viewsets
from django.views.generic import DetailView, ListView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Portfolio, Comment
from .serializers import PortfolioSerializer,CommentSerializer,PortfolioThumbSerializer
from django.views.generic import TemplateView
from braces import views
from django.views.generic.base import TemplateResponseMixin, ContextMixin


class AdminMixin(TemplateResponseMixin, ContextMixin,):

     def get_context_data(self, **kwargs):
        context = super(AdminMixin, self).get_context_data(**kwargs)
        context['in_admin'] = True
        return context

     def get_template_names(self):
        return ['/' + self.template_name, self.template_name]


class AdminView(views.LoginRequiredMixin, AdminMixin, views.GroupRequiredMixin, TemplateView):
    group_required = u'students'
    raise_exception = True


class PortfolioViewSet(viewsets.ModelViewSet):
    model = Portfolio
    lookup_field = 'id'
    filter_fields = ('user', 'home_published',)
    serializer_class = PortfolioSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.user = self.request.user


class PortfolioThumbViewSet(viewsets.ModelViewSet):
    model = Portfolio
    lookup_field = 'id'
    serializer_class = PortfolioThumbSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, **kwargs):
        portfolio = self.get_object()
        serializer = PortfolioThumbSerializer(portfolio, request.FILES)

        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response(serializer.errors, status=400)


class PortfoliosView(ListView):
    context_object_name = 'portfolios'
    template_name = "portfolios.html"


class PortfolioView(DetailView):
    model = Portfolio
    template_name = 'portfolio.html'

    def get_context_data(self, **kwargs):
        context = super(PortfolioView, self).get_context_data(**kwargs)
        user = self.request.user

        return context


class CommentViewSet(viewsets.ModelViewSet):
    model = Comment
    lookup_field = 'id'
    filter_fields = ('user', 'portfolio',)
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


class PortfoliosView(ListView):
    context_object_name = 'portfolios'
    template_name = "portfolios.html"

    def get_queryset(self):
        return Portfolio.objects.all().filter(home_published=True)


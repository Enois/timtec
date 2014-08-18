from rest_framework import viewsets
from django.views.generic import DetailView, ListView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Portfolio, Comment
from .serializers import PortfolioSerializer, CommentSerializer, PortfolioThumbSerializer
from braces import views
from braces.views import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView


class PortfolioCreateView(CreateView, LoginRequiredMixin, views.GroupRequiredMixin,):
    model = Portfolio
    template_name = 'portfolio-edit.html'
    group_required = u'students'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(PortfolioCreateView, self).get_context_data(**kwargs)
        context['in_student'] = True
        if self.request.user is None:
            user = self.request.user
            portfolio_user_id = self.object.user.id
            context['portfolio_user_id'] = portfolio_user_id
            return context
        else:
            return context


class PortfolioEditView(LoginRequiredMixin, UpdateView, views.GroupRequiredMixin,):
    model = Portfolio
    template_name = 'portfolio.html'
    group_required = u'students'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(PortfolioEditView, self).get_context_data(**kwargs)
        context['in_student'] = True
        user = self.request.user

        if user.is_authenticated():
            portfolio_user_id = self.object.user.id
            context['portfolio_user_id'] = portfolio_user_id

        return context


class PortfolioViewSet(viewsets.ModelViewSet):

    model = Portfolio
    lookup_field = 'id'
    filter_fields = ('user', 'home_published', 'status',)
    serializer_class = PortfolioSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, **kwargs):
        response = super(PortfolioViewSet, self).get(request, **kwargs)
        response['Cache-Control'] = 'no-cache'
        return response

    def post(self, request, **kwargs):
        portfolio = self.get_object()
        serializer = PortfolioSerializer(portfolio, request.DATA)

        if serializer.is_valid():
           serializer.save()
           return Response(status=200)
        else:
           return Response(serializer.errors, status=400)

    def metadata(self, request):
        data = super(PortfolioViewSet, self).metadata(request)
        data.get('actions').get('POST').get('status').update({'choices': dict(Portfolio.STATES[1:])})
        return data


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


class PortfolioView(DetailView):
    model = Portfolio
    template_name = 'portfolio.html'

    def get_context_data(self, **kwargs):
        context = super(PortfolioView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated():
            portfolio_user_id = self.object.user.id
            context['portfolio_user_id'] = portfolio_user_id

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
        return Portfolio.objects.all().filter(user=self.request.user)


class PortfoliosTestView(ListView):
    context_object_name = 'portfoliohome'
    template_name = "portfoliohome.html"

    def get_queryset(self):
        return Portfolio.objects.all().filter(home_published=True)

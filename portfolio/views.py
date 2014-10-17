from rest_framework import viewsets
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Portfolio, PortfolioComment
from .serializers import PortfolioSerializer, PortfolioCommentSerializer, PortfolioThumbSerializer
from braces import views
from braces.views import LoginRequiredMixin
from accounts.models import TimtecUser
from django.core.urlresolvers import reverse_lazy
from portfolio.forms import EnoisPortfolioForm


class CreatePortfolioView(CreateView, LoginRequiredMixin, views.GroupRequiredMixin,):
    model = Portfolio
    template_name = 'portfolio-edit.html'
    group_required = 'students'
    raise_exception = True
    fields = ('name', 'video', 'description', 'tags', 'home_published')

    def get_context_data(self, **kwargs):
        context = super(CreatePortfolioView, self).get_context_data(**kwargs)
        context['portfolio'] = self.object
        context['user_can_promote'] = self.request.user.is_staff
        context['right_button_columns'] = 12
        return context

    def get_form_kwargs(self):
        kwargs = super(CreatePortfolioView, self).get_form_kwargs()
        if self.request.method in ['PUT', 'POST'] and kwargs.get('instance', None) is None:
            kwargs['instance'] = self.model(user=TimtecUser.objects.get(pk=self.request.user.id))
        return kwargs

    def get_success_url(self):
        return reverse_lazy('portfolio_view', kwargs={'pk': self.object.id})

class UpdatePortfolioView(LoginRequiredMixin, UpdateView, views.GroupRequiredMixin,):
    model = Portfolio
    template_name = 'portfolio-edit.html'
    group_required = 'students'
    raise_exception = True
    form_class = EnoisPortfolioForm

    def get_context_data(self, **kwargs):
        context = super(UpdatePortfolioView, self).get_context_data(**kwargs)
        context['portfolio'] = self.object
        context['user_can_promote'] = self.request.user.is_staff
        context['right-button-columns'] = 7
        return context

    def get_success_url(self):
        return reverse_lazy('portfolio_view', kwargs={'pk': self.object.id})

class DeletePortfolioView(LoginRequiredMixin, DeleteView, views.GroupRequiredMixin):
    model = Portfolio
    group_required = 'students'
    template_name = 'portfolio-delete.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.object.user_id})


class PortfolioView(DetailView):
    model = Portfolio
    template_name = 'portfolio.html'

    def get_context_data(self, **kwargs):
        context = super(PortfolioView, self).get_context_data(**kwargs)
        context['portfolio_items'] = Portfolio.objects.filter(
            user=self.request.user.id).order_by('-timestamp').exclude(
                id=self.object.id)[:2]
        return context


class UserPortfoliosView(LoginRequiredMixin, ListView):
    context_object_name = 'portfolios'
    template_name = "user-portfolios.html"

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


class PortfoliosView(ListView):
    context_object_name = 'portfolios'
    template_name = "portfolios.html"
    paginate_by = 8

    def get_queryset(self):
        return Portfolio.objects.filter(status='published')


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

    def create(self, request, *args, **kwargs):
        request.DATA.update({'user': request.user.id})
        return super(PortfolioViewSet, self).create(request, *args, **kwargs)

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


class PortfolioCommentViewSet(viewsets.ModelViewSet):
    model = PortfolioComment
    lookup_field = 'id'
    filter_fields = ('user', 'portfolio',)
    serializer_class = PortfolioCommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        return PortfolioComment.objects.filter(user=self.request.user)

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from accounts.models import TimtecUser


class EnoisProfileView(DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        if hasattr(self, 'kwargs') and 'username' in self.kwargs:
            try:
                return get_object_or_404(self.model, username=self.kwargs['username'])
            except:
                return self.request.user
        else:
            return self.request.user

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data()
        context['portfolios'] = context['profile_user'].portfolio_set.all().order_by('-timestamp')[:4]
        import pprint; pprint.pprint(context['profile_user'].__dict__)
        context['courses_given'] = [
            cp.course for cp in
            context['profile_user'].courseprofessor_set.all()[:4]]
        context['courses_enrolled'] = [
            cp.course for cp in
            context['profile_user'].coursestudent_set.all()[:4]]
        return context


class TeachersView(ListView):
    context_object_name = 'teachers'
    template_name = 'teachers.html'

    def get_queryset(self):
        return TimtecUser.objects.all().filter(groups=2)

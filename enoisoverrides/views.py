from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404

from accounts.models import TimtecUser
from core.views import EnrollCourseView, AcceptTermsView


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
        context['portfolios'] = context['profile_user'].portfolio_set.all().order_by('-timestamp')
        context['courses_given'] = [
            cp.course for cp in
            context['profile_user'].courseprofessor_set.all()]
        context['courses_enrolled'] = [
            cp.course for cp in
            context['profile_user'].coursestudent_set.all()]
        return context


class TeachersView(ListView):
    context_object_name = 'teachers'
    template_name = 'teachers.html'

    def get_queryset(self):
        return TimtecUser.objects.all().filter(groups=2)

class EnoisEnrollCourseView(EnrollCourseView):
    def get_redirect_url(self, **kwargs):
        if not self.request.user.accepted_terms:
            return reverse('accept_terms') + '?course=' + self.kwargs['slug']
        else:
            return super(EnoisEnrollCourseView, self).get_redirect_url(**kwargs)

class EnoisAcceptTermsView(AcceptTermsView):
    def get_success_url(self):
        course_slug = self.request.REQUEST.get('course', None)
        if course_slug:
            return reverse('enroll_course', kwargs={'slug': course_slug })
        else:
            return super(AcceptTermsView, self).get_success_url()

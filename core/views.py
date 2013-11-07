# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic.base import RedirectView, View, TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from accounts.utils import LoginRequiredMixin
from rest_framework import viewsets
from rest_framework.response import Response

from serializers import CourseSerializer
from models import Course, StudentProgress


class NewHomeView(ListView):
    """
    // TODO Bruno view temporaria para desenvolvimento do layout da nova home
    """
    model = Course
    template_name = 'index.html'
    context_object_name = 'courses'


class HomeView(View):
    def get(self, request):
        latest = Course.objects.latest('publication')
        return redirect(reverse('course_intro', args=[latest.slug]))


class CourseView(DetailView):
    model = Course
    template_name = 'course.html'

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated():
            units_done = StudentProgress.objects.filter(user=user, unit__lesson__course=self.object)\
                                                .exclude(complete=None)\
                                                .values_list('unit', flat=True)
            context['units_done'] = units_done

            user_is_enrolled = self.object.students.filter(id=user.id).exists()
            context['user_is_enrolled'] = user_is_enrolled

        return context


class UserCoursesView(LoginRequiredMixin, TemplateView):
    template_name = 'user-courses.html'


class EnrollCourseView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_object(self):
        if hasattr(self, 'object'):
            return self.object
        self.object = Course.objects.get(**self.kwargs)
        return self.object

    def get_redirect_url(self, **kwargs):
        course = self.get_object()
        course.enroll_student(self.request.user)
        return reverse('lesson', args=[course.first_lesson().slug])


class AdminCourseView(LoginRequiredMixin, UpdateView):
    model = Course
    template_name = 'admin/_base.html'


class CourseViewSet(viewsets.ModelViewSet):
    model = Course
    lookup_field = 'slug'
    serializer_class = CourseSerializer

    def post(self, request, **kwargs):
        course = self.get_object()
        serializer = CourseSerializer(course, request.DATA)

        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response(serializer.errors, status=403)

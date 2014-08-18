# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from core.models import Course
from course_material.forms import FileForm
from course_material.serializers import CourseMaterialSerializer
from course_material.models import CourseMaterial
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import filters
from administration.views import AdminMixin


class CourseMaterialView(LoginRequiredMixin, DetailView):
    model = CourseMaterial
    context_object_name = 'course_material'
    template_name = 'course-material.html'
    slug_field = 'course__slug'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseMaterialView, self).get_context_data(**kwargs)
        self.course = get_object_or_404(Course, slug=self.kwargs['slug'])
        context['course'] = self.course
        return context


class FileUploadView(LoginRequiredMixin, CreateView):
    form_class = FileForm
    success_url = '/'

    def form_valid(self, form):
        super(FileUploadView, self).form_valid(form)
        return HttpResponse()


class CourseMaterialAdminView(AdminMixin, DetailView):
    model = CourseMaterial
    context_object_name = 'course_material'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseMaterialAdminView, self).get_context_data(**kwargs)
        self.course = get_object_or_404(Course, id=self.kwargs['pk'])
        context['course'] = self.course
        return context


class CourseMaterialViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = CourseMaterial
    serializer_class = CourseMaterialSerializer
    lookup_field = 'course'
    filter_fields = ('course__id',)
    filter_backends = (filters.DjangoFilterBackend,)

    def pre_save(self, obj):

        if 'course' in self.kwargs:
            obj.course = Course.objects.get(id=int(self.kwargs['course']))
            self.kwargs['course'] = obj.course
        return super(CourseMaterialViewSet, self).pre_save(obj)

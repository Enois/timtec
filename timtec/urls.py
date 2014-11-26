# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin as django_admin
django_admin.autodiscover()

from django.views.generic import TemplateView
from accounts.views import CustomLoginView, ProfileEditView
from forum.views import AnswerViewSet as ForumAnswerViewSet

from core.views import (CourseView, CourseViewSet, CourseThumbViewSet,
                        CourseProfessorViewSet,
                        UserCoursesView, ContactView, LessonDetailView,
                        LessonViewSet, StudentProgressViewSet,
                        UserNotesViewSet, CoursesView,
                        ProfessorMessageViewSet, CourseStudentViewSet,
                        CarouselCourseView,)
from homepage.views import HomePageView

from activities.views import AnswerViewSet
from accounts.views import TimtecUserViewSet
from forum.views import CourseForumView, QuestionView, QuestionCreateView, QuestionViewSet, QuestionVoteViewSet, AnswerVoteViewSet
from course_material.views import CourseMaterialView, FileUploadView, CourseMaterialViewSet
from notes.views import NotesViewSet, CourseNotesView, UserNotesView
from reports.views import UserCourseStats, CourseStatsByLessonViewSet
from portfolio.views import (PortfolioViewSet, PortfolioCommentViewSet,
                             PortfolioThumbViewSet, PortfoliosView,
                             UserPortfoliosView, CreatePortfolioView,
                             PortfolioView, UpdatePortfolioView, DeletePortfolioView)
from rest_framework import routers
from django_markdown import flatpages
from enoisoverrides.views import EnoisProfileView, TeachersView, EnoisEnrollCourseView, EnoisAcceptTermsView

flatpages.register()

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', TimtecUserViewSet)
router.register(r'course', CourseViewSet)
router.register(r'course_carousel', CarouselCourseView)
router.register(r'course_professor', CourseProfessorViewSet)
router.register(r'course_student', CourseStudentViewSet)
router.register(r'professor_message', ProfessorMessageViewSet)
router.register(r'coursethumbs', CourseThumbViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'answer', AnswerViewSet)
router.register(r'student_progress', StudentProgressViewSet)
router.register(r'forum_question', QuestionViewSet)
router.register(r'forum_answer', ForumAnswerViewSet)
router.register(r'question_vote', QuestionVoteViewSet)
router.register(r'answer_vote', AnswerVoteViewSet)
router.register(r'course_material', CourseMaterialViewSet)
router.register(r'note', NotesViewSet)
router.register(r'user_notes', UserNotesViewSet)
router.register(r'reports', UserCourseStats)
router.register(r'course_stats', CourseStatsByLessonViewSet)
router.register(r'portfolio', PortfolioViewSet, PortfolioCommentViewSet)
router.register(r'portfoliothumbs', PortfolioThumbViewSet)

urlpatterns = patterns(
    '',
    url(r'^$', HomePageView.as_view(), name='home_view'),
    url(r'^cursos', CoursesView.as_view(), name='courses'),

    # Uncomment the next line to enable the admin:
    url(r'^django/admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^django/admin/', include(django_admin.site.urls)),

    # Privileged browsing
    url(r'^admin/', include('administration.urls')),

    # Public browsing
    url(r'^meus-cursos/$', UserCoursesView.as_view(), name='user_courses'),
    url(r'^accept_terms/$', EnoisAcceptTermsView.as_view(), name='accept_terms'),
    url(r'^curso/(?P<slug>[-a-zA-Z0-9_]+)/$', CourseView.as_view(), name='course_intro'),
    url(r'^curso/(?P<slug>[-a-zA-Z0-9_]+)/matricula/$', EnoisEnrollCourseView.as_view(), name='enroll_course'),
    url(r'^curso/(?P<course_slug>[-a-zA-Z0-9_]+)/aula/(?P<slug>[-a-zA-Z0-9_]+)/$', LessonDetailView.as_view(), name='lesson'),
    url(r'^html5/', TemplateView.as_view(template_name="html5.html")),
    url(r'^empty/', TemplateView.as_view(template_name="empty.html")),
    url(r'^contact/?$', ContactView.as_view(), name="contact"),

    # Services
    url(r'^api/', include(router.urls)),

    # Forum
    url(r'^forum/(?P<course_slug>[-a-zA-Z0-9_]+)/$', CourseForumView.as_view(), name='forum'),
    url(r'^forum/question/(?P<slug>[-a-zA-Z0-9_]+)/$', QuestionView.as_view(), name='forum_question'),
    url(r'^forum/question/add/(?P<course_slug>[-a-zA-Z0-9_]+)/$', QuestionCreateView.as_view(), name='forum_question_create'),

    # Portfolio
    url(r'^trampos/$',
        PortfoliosView.as_view(), name='portfolios'),
    url(r'^trampos/(?P<pk>[1-9][0-9]*)/$',
        PortfolioView.as_view(), name='portfolio_view'),
    url(r'^trampos/(?P<pk>[1-9][0-9]*)/editar$',
        UpdatePortfolioView.as_view(), name='portfolio_edit'),
    url(r'^trampos/(?P<pk>[1-9][0-9]*)/deletar$',
        DeletePortfolioView.as_view(), name='portfolio_delete'),
    url(r'^meus-trampos/$',
        UserPortfoliosView.as_view(), name='user_portfolios'),
    url(r'^meus-trampos/novo/$',
        CreatePortfolioView.as_view(), name='portfolio_new'),

    # Teachers
    url(r'^mentores', TeachersView.as_view(), name='teachers'),

    # Course Material
    url(r'^curso/(?P<slug>[-a-zA-Z0-9_]+)/material/file_upload/$', FileUploadView.as_view(), name='file_upload'),
    url(r'^curso/(?P<slug>[-a-zA-Z0-9_]+)/material/$', CourseMaterialView.as_view(), name='course_material'),

    # Notes
    url(r'^notas/(?P<username>[\w.+-]+)?$', UserNotesView.as_view(), name='user_notes'),
    url(r'^curso/(?P<course_slug>[-a-zA-Z0-9_]+)/minhas-notas/$', CourseNotesView.as_view(), name='user_course_notes'),

    # Authentication
    url(r'^entrar/', CustomLoginView.as_view(), name='timtec_login'),
    url(r'^sair/', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='timtec_logout'),

    # Profiles
    url(r'^perfil/editar/?$', ProfileEditView.as_view(), name="profile_edit"),
    url(r'^perfil/(?P<username>[\w.+-]+)?/?$', EnoisProfileView.as_view(), name="profile"),

    # The django-allauth
    url(r'^accounts/', include('allauth.urls')),

    # The django-rosetta
    url(r'^rosetta/', include('rosetta.urls')),

    url(r'^pages/', include('django.contrib.flatpages.urls')),

    url(r'^markdown/', include('django_markdown.urls')),
)

if settings.TWITTER_USER != '':
    from core.views import TwitterApi
    urlpatterns += url(r'^api/twitter/?$', TwitterApi.as_view(), name='twitter'),


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

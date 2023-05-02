from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [


    path('login/', LoginView.as_view(template_name='registration/login.html'), name='home'),
    path('student/resultat', views.student_resultat, name='student_resultat'),
    path('student/emploi', views.student_emploi, name='student_emploi'),
    path('teacher/', views.teacher_home, name='teacher_home'),
    path('teacher/matiere', views.teacher_matiere, name='teacher_matiere'),
    path('teacher/note/<str:classe>/<str:subject>/',
         views.teacher_note, name='teacher_note'),
    path('', views.home, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

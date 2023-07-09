"""
URL configuration for shtdone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from principal.views import home,LoginUsuarioView,TaskListView,TaskView,TaskDetailView
# ,TaskCreateView,TaskUpdateView,TaskDeleteView,TaskCompleteView,Task

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/view/<int:task_id>/', TaskView.as_view(), name='task_view'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),

    

    
]
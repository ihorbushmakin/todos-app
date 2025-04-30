from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import CustomLoginView


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/add/', views.add_task, name='add-task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete-task'),
    path('tasks/complete/<int:task_id>/', views.complete_task, name='complete-task'),
    path('tasks/uncomplete/<int:task_id>/', views.uncomplete_task, name='uncomplete-task'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit-task'),
]

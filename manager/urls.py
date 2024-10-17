from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path

from Task_manager import settings
from manager.views import (
    index,
    MyProjectListView,
    MyTaskListView,
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
    TeamCreateView,
    TeamDeleteView,
    TeamDetailView,
    TeamListView,
    TeamUpdateView,
    WorkerCreateView,
    WorkerDeleteView,
    WorkerDetailView,
    WorkerListView,
    WorkerUpdateView,
)


urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("task/", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("worker/", WorkerListView.as_view(), name="worker-list"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("worker/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("team/", TeamListView.as_view(), name="team-list"),
    path("team/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("team/create/", TeamCreateView.as_view(), name="team-create"),
    path("team/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("team/<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"),
    path("project/", ProjectListView.as_view(), name="project-list"),
    path("project/<int:pk>", ProjectDetailView.as_view(), name="project-detail"),
    path("project/create/", ProjectCreateView.as_view(), name="project-create"),
    path(
        "project/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"
    ),
    path(
        "project/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"
    ),
    path("my_tasks/", MyTaskListView.as_view(), name="my-task-list"),
    path("my_projects/", MyProjectListView.as_view(), name="my-project-list"),
]


app_name = "manager"

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, \
    UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout


from django.contrib.auth.decorators import login_required

from manager.forms import TaskSearchForm, TaskFilterForm, TaskForm, WorkerSearchForm, WorkerFilterForm, WorkerForm
from manager.models import Task, Team, Worker, Project


# Create your views here.
@login_required
def index(request):
    num_tasks = Task.objects.count()
    num_teams = Team.objects.count()
    num_workers = Worker.objects.count()
    context = {
        "num_tasks": num_tasks,
        "num_teams": num_teams,
        "num_workers": num_workers,
    }
    return render(request, template_name="pages/index.html", context=context)


# ----


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    template_name = "manager/task_list.html"
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("search-name", "")
        print(name)
        context["search_form"] = TaskSearchForm(initial={"search-name": name}, prefix="search")
        context["filter_form"] = TaskFilterForm(prefix="filter")
        return context

    def get_queryset(self):
        queryset = self.queryset
        search_form = TaskSearchForm(self.request.GET)
        filter_form = TaskFilterForm(self.request.GET)
        if filter_form.is_valid():
            is_completed = filter_form.cleaned_data.get("is_completed", None)
            priority = filter_form.cleaned_data.get("priority", None)
            project = filter_form.cleaned_data.get("project", None)
            task_type = filter_form.cleaned_data.get("task_type", None)
            assignees = filter_form.cleaned_data.get("assignees", None)
            if is_completed is not None:
                queryset = queryset.filter(is_completed=is_completed)
            if priority is not None:
                queryset = queryset.filter(priority=priority)
            if task_type is not None:
                queryset = queryset.filter(task_type=task_type)
            if project is not None:
                queryset = queryset.filter(project=project)
            if assignees is not None:
                queryset = queryset.filter(assignees=assignees)
        if search_form.is_valid():
            return (queryset.
                    filter(name__icontains=search_form.cleaned_data.
                           get("search-name", "")))

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_confirm_delete.html"


# ----


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5
    queryset = Worker.objects.select_related("position").select_related("team").prefetch_related("projects")
    ordering = ["last_name", ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(initial={"search-username": username}, prefix="search")
        context["filter_form"] = WorkerFilterForm(prefix="filter")
        return context

    def get_queryset(self):
        queryset = self.queryset
        search_form = TaskSearchForm(self.request.GET)
        filter_form = TaskFilterForm(self.request.GET)
        if filter_form.is_valid():
            position = filter_form.cleaned_data.get("filter-position", None)
            team = filter_form.cleaned_data.get("filter-team", None)
            project = filter_form.cleaned_data.get("filter-project", None)
            if position is not None:
                queryset = queryset.filter(position=position)
            if team is not None:
                queryset = queryset.filter(team=team)
            if project is not None:
                queryset = queryset.filter(project=filter_form.
                                           project)
        if search_form.is_valid():
            queryset = queryset.filter(username__icontains=search_form.cleaned_data.
                                       get("search-username", ""))
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("manager:worker-list")
    template_name = "manager/worker_confirm_delete.html"

# ----


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 5
    queryset = Task.objects.select_related("team_lead")
    ordering = ["name", ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(initial={"search-username": username}, prefix="search")
        context["filter_form"] = WorkerFilterForm(prefix="filter")
        return context

    def get_queryset(self):
        queryset = self.queryset
        search_form = TaskSearchForm(self.request.GET)
        filter_form = TaskFilterForm(self.request.GET)
        if filter_form.is_valid():
            position = filter_form.cleaned_data.get("filter-position", None)
            team = filter_form.cleaned_data.get("filter-team", None)
            project = filter_form.cleaned_data.get("filter-project", None)
            if position is not None:
                queryset = queryset.filter(position=position)
            if team is not None:
                queryset = queryset.filter(team=team)
            if project is not None:
                queryset = queryset.filter(project=filter_form.
                                           project)
        if search_form.is_valid():
            queryset = queryset.filter(username__icontains=search_form.cleaned_data.
                                       get("search-username", ""))
        return queryset

class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    success_url = reverse_lazy("manager:team-list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    success_url = reverse_lazy("manager:team-list")


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("manager:team-list")


# --


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5
    ordering = ["deadline", ]
    queryset = Project.objects.select_related("teams").prefetch_related("participants")


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    success_url = reverse_lazy("manager:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    success_url = reverse_lazy("manager:project-list")


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("manager:project-list")


# Authentication
class UserRegistrationView(CreateView):
    template_name = 'accounts/auth-signup.html'
    form_class = RegistrationForm
    success_url = '/accounts/login/'


class UserLoginView(LoginView):
    template_name = 'accounts/auth-signin.html'
    form_class = LoginForm


class UserPasswordResetView(LoginRequiredMixin, PasswordResetView):
    template_name = 'accounts/auth-reset-password.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(LoginRequiredMixin, PasswordResetConfirmView):
    template_name = 'accounts/auth-password-reset-confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/auth-change-password.html'
    form_class = UserPasswordChangeForm


@login_required
def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')

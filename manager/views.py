from django.utils import timezone
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

from manager.forms import TaskSearchForm, TaskFilterForm, TaskForm, WorkerSearchForm, WorkerFilterForm, WorkerForm, \
    TeamSearchForm, TeamFilterForm, TeamForm, ProjectFilterForm, ProjectSearchForm, ProjectForm
from manager.models import Task, Team, Worker, Project


# Create your views here.
@login_required
def index(request):
    today = timezone.now()
    my_tasks_month = Task.objects.filter(assignees__id=request.user.id, deadline__month=today.month,
                                         deadline__year=today.year).count()
    my_tasks_month_done = Task.objects.filter(assignees__id=request.user.id, deadline__month=today.month,
                                              deadline__year=today.year, is_completed=True).count()
    if my_tasks_month != 0:
        per_my_tasks = round((my_tasks_month_done / my_tasks_month)) * 100
    else:
        per_my_tasks = 0
    my_projects_month = Project.objects.filter(participants__id=request.user.id, deadline__month=today.month,
                                               deadline__year=today.year).count()
    my_projects_month_done = Project.objects.filter(participants__id=request.user.id, deadline__month=today.month,
                                                    deadline__year=today.year, is_completed=True).count()
    if my_projects_month != 0:
        per_my_projects = round((my_projects_month_done / my_projects_month)) * 100
    else:
        per_my_projects = 0

    context = {
        "per_my_tasks": per_my_tasks,
        "per_my_projects": per_my_projects,
    }
    return render(request, template_name="pages/index.html", context=context)


# ----


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    template_name = "manager/task_list.html"
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees").order_by("deadline")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("search-name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name}, prefix="search")
        context["filter_form"] = TaskFilterForm(prefix="filter")
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_form = TaskSearchForm(self.request.GET, prefix="search")
        filter_form = TaskFilterForm(self.request.GET, prefix="filter")
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
            queryset = (queryset.
                        filter(name__icontains=search_form.cleaned_data.
                               get("name", "")))

        return queryset


class MyTaskListView(TaskListView):
    def get_queryset(self):
        return super().get_queryset().filter(assignees=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["mytask"] = "yes"
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


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
        username = self.request.GET.get("search-username", "")
        context["search_form"] = WorkerSearchForm(initial={"username": username}, prefix="search")
        context["filter_form"] = WorkerFilterForm(prefix="filter")
        return context

    def get_queryset(self):
        queryset = self.queryset
        search_form = WorkerSearchForm(self.request.GET, prefix="search")
        filter_form = WorkerFilterForm(self.request.GET, prefix="filter")
        if filter_form.is_valid():
            position = filter_form.cleaned_data.get("position", None)
            team = filter_form.cleaned_data.get("team", None)
            projects = filter_form.cleaned_data.get("projects", None)
            if position:
                queryset = queryset.filter(position=position)
            if team:
                queryset = queryset.filter(team=team)
            if projects:
                queryset = queryset.filter(projects=projects)
        if search_form.is_valid():
            queryset = queryset.filter(username__icontains=search_form.cleaned_data.
                                       get("username", ""))
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
    queryset = (Team.objects.select_related("team_lead").
                prefetch_related("projects").
                prefetch_related("workers")).order_by("name",)
    template_name = "manager/team_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for team in Team.objects.all():
            if self.request.user.id in [worker.id for worker in team.workers.all()]:
                context["team_id"] = team.id
        name = self.request.GET.get("search-name", "")
        context["search_form"] = TeamSearchForm(initial={"search-name": name}, prefix="search")
        context["filter_form"] = TeamFilterForm(prefix="filter")
        return context

    def get_queryset(self):
        queryset = self.queryset
        search_form = TeamSearchForm(self.request.GET, prefix="search")
        filter_form = TeamFilterForm(self.request.GET, prefix="filter")
        if filter_form.is_valid():
            projects = filter_form.cleaned_data.get("projects", None)
            if projects is not None:
                queryset = queryset.filter(projects=projects)
        if search_form.is_valid():
            queryset = queryset.filter(name__icontains=search_form.cleaned_data.
                                       get("name", ""))
        return queryset


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        k = 0
        for worker in Team.objects.get(id=self.kwargs["pk"]).workers.all():
            if worker.id == self.request.user.id:
                context["worker_is_here"] = True
                break
        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    success_url = reverse_lazy("manager:team-list")
    form_class = TeamForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.workers.set(form.cleaned_data["workers"])
        form.instance.projects.set(form.cleaned_data["projects"])
        return response


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    success_url = reverse_lazy("manager:team-list")
    form_class = TeamForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.workers.set(form.cleaned_data["workers"])
        form.instance.projects.set(form.cleaned_data["projects"])
        return response


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("manager:team-list")
    template_name = "manager/team_confirm_delete.html"


# --


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5
    queryset = Project.objects.select_related("team").prefetch_related("participants").order_by("deadline")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("search-name", "")
        context["search_form"] = ProjectSearchForm(initial={"name": name}, prefix="search")
        context["filter_form"] = ProjectFilterForm(prefix="filter")
        return context

    def get_queryset(self):
        queryset = self.queryset
        search_form = ProjectSearchForm(self.request.GET, prefix="search")
        filter_form = ProjectFilterForm(self.request.GET, prefix="filter")
        if filter_form.is_valid():
            deadline = filter_form.cleaned_data.get("deadline", None)
            participants = filter_form.cleaned_data.get("participants", None)
            team = filter_form.cleaned_data.get("team", None)
            if deadline:
                queryset = queryset.filter(deadline=deadline)
            if participants:
                queryset = queryset.filter(participants__in=participants)
            if team:
                queryset = queryset.filter(team__in=team)
        if search_form.is_valid():
            queryset = queryset.filter(name__icontains=search_form.cleaned_data.
                                       get("name", ""))
        return queryset



class MyProjectListView(ProjectListView):
    def get_queryset(self):
        return super().get_queryset().filter(participants=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["myproject"] = "yes"
        return context


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    success_url = reverse_lazy("manager:project-list")
    form_class = ProjectForm

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.participants.set(form.cleaned_data["participants"])
        form.instance.tasks.set(form.cleaned_data["tasks"])
        return response


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    success_url = reverse_lazy("manager:project-list")
    form_class = ProjectForm

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.participants.set(form.cleaned_data["participants"])
        form.instance.tasks.set(form.cleaned_data["tasks"])
        return response


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("manager:project-list")
    template_name = "manager/project_confirm_delete.html"


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

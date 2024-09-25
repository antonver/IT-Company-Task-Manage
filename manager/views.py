from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from manager.models import Task, Team, Worker


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
    render(request, template_name="pages/index.html", context=context)

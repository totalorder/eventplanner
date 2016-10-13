from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as _login, logout as _logout
from app import models


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                _login(request, user)
                return redirect(reverse("index"))
    return render(request, "login.html")


def logout(request):
    _logout(request)
    return redirect(reverse("login"))


def edit_planning_request(request, request_id):
    if not(in_group(request.user, "scso")):
        return HttpResponse("You are not authorized to access this page", status=401)

    planning_request = models.PlanningRequest.objects.get(pk=request_id)
    saved = False

    if request.method == "POST":
        planning_request_form = models.PlanningRequestForm(
            request.POST, instance=planning_request)
        if planning_request_form.is_valid():
            planning_request_form.save()
            saved = True


    planning_request_form = models.PlanningRequestForm(instance=planning_request)
    return render(request, "planning_request_edit.html", {
        "form": planning_request_form,
        "request_id": request_id,
        "saved": saved
    })


def write_planning_request_feedback(request, request_id):
    if not(in_group(request.user, "fm")):
        return HttpResponse("You are not authorized to access this page", status=401)

    planning_request = models.PlanningRequest.objects.get(pk=request_id)
    if planning_request.state != "scso_approved":
        return HttpResponse("State now allowed", status=400)
    saved = False

    if request.method == "POST":
        if "feedback" in request.POST:
            planning_request.budget_feedback = request.POST["feedback"]
            planning_request.state = "fm_commented"
            planning_request.save()
            saved = True

    planning_request = model_to_dict(planning_request)
    return render(request, "planning_request_write_feedback.html", {
        "planning_request": planning_request,
        "request_id": request_id,
        "saved": saved
    })


def planning_request(request):
    if not(in_group(request.user, "cso") or in_group(request.user, "scso") or in_group(request.user, "fm")):
        return HttpResponse("You are not authorized to access this page", status=401)
    planning_request_form = models.PlanningRequestForm(request.POST)

    if request.method == "POST":
        if planning_request_form.is_valid():
            planning_request_form.save()

    planning_requests = models.PlanningRequest.objects.all()
    if "state" in request.GET:
        planning_requests = planning_requests.filter(
            state=request.GET["state"])

    return render(request, "planning_request.html", {
        "form": planning_request_form,
        "planning_requests": models_to_dicts(planning_requests),
        "groups": [group.name for group in request.user.groups.all()],
        "states": [choice[0] for choice in models.state_choices],
        "current_state": request.GET.get("state")
    })


def model_to_dict(obj):
    obj.dict = {(field.attname, getattr(obj, field.attname)) for field in obj._meta.fields}
    return obj


def models_to_dicts(objs):
    return [model_to_dict(obj) for obj in objs]


def in_group(user, group_name):
    return user.groups.filter(name=group_name).count() > 0


@login_required(login_url=reverse_lazy("login"))
def index(request):
    return render(request, "index.html", {"groups": request.user })


def approve(request):
    planning_request = models.PlanningRequest.objects.get(
        pk=request.POST.get("planning_request_id"))

    new_state = request.POST["new_state"]
    planning_request.state = new_state
    planning_request.save()
    return redirect("planning_request")

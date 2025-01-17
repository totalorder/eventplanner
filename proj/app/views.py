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
    planning_request = models.PlanningRequest.objects.get(pk=request_id)

    if not(in_group(request.user, "scso") and planning_request.state in ("new", "cso_approved") or
           in_group(request.user, "adm") or
           in_group(request.user, "psm") and planning_request.state == "adm_approved"):
        return HttpResponse("You are not authorized to access this page", status=401)
    saved = False

    details_form = models.PlanningRequestDetailsForm(
        data={
            "decoration_descr": planning_request.decoration_descr,
            "parties_descr": planning_request.parties_descr,
            "drinks_descr": planning_request.drinks_descr,
            "food_descr": planning_request.food_descr,
            "media_descr": planning_request.media_descr,
            "expected_budget": planning_request.expected_budget,
        })

    if request.method == "POST":
        if in_group(request.user, "psm"):
            details_form = models.PlanningRequestDetailsForm(request.POST)
            if details_form.is_valid():
                for key, value in details_form.cleaned_data.items():
                    setattr(planning_request, key, value)
                planning_request.save()
                saved = True
        else:
            planning_request_form = models.PlanningRequestForm(
                request.POST, instance=planning_request)
            if planning_request_form.is_valid():
                planning_request_form.save()
                saved = True


    planning_request_form = models.PlanningRequestForm(instance=planning_request)
    return render(request, "planning_request_edit.html", {
        "form": planning_request_form,
        "details_form": details_form,
        "request_id": request_id,
        "groups": [group.name for group in request.user.groups.all()],
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
    if not(in_group(request.user, "cso") or
           in_group(request.user, "scso") or
           in_group(request.user, "fm") or
           in_group(request.user, "adm") or
           in_group(request.user, "hrm") or
           in_group(request.user, "psm")):
        return HttpResponse("You are not authorized to access this page", status=401)
    planning_request_form = models.PlanningRequestForm()

    if request.method == "POST":
        planning_request_form = models.PlanningRequestForm(request.POST)
        if planning_request_form.is_valid():
            planning_request_form.save()
            planning_request_form = models.PlanningRequestForm()

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
    obj.dict = sorted([(field.attname, getattr(obj, field.attname)) for field in obj._meta.fields],
                      cmp=lambda x, y: -1 if x[0] == "id" else 1 if y[0] == "id" else cmp(x[0], y[0]))

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
    if new_state == "scso_approved":
        if planning_request.client is None:
            return HttpResponse("Client has to be set before sending to finance")

    planning_request.state = new_state
    planning_request.save()
    return redirect("planning_request")


def create_task(request, request_id):
    planning_request = models.PlanningRequest.objects.get(
        pk=request_id)

    if not(in_group(request.user, "psm")):
        return HttpResponse("You are not authorized to access this page", status=401)

    task_form = models.TaskForm()
    if request.method == "POST":
        task_form = models.TaskForm(request.POST)
        if task_form.is_valid():
            task = models.Task(planning_request=planning_request,
                               **task_form.cleaned_data)
            task.save()
            task_form = models.TaskForm()

    planning_request = models.PlanningRequest.objects.get(
        pk=request_id)
    planning_request = model_to_dict(planning_request)
    planning_request.tasks_dicts = models_to_dicts(planning_request.tasks.all())
    return render(request, "tasks.html", {
        "planning_request": planning_request,
        "form": task_form
    })


def create_recruitment_request(request, request_id):
    planning_request = models.PlanningRequest.objects.get(
        pk=request_id)

    if not(in_group(request.user, "psm")):
        return HttpResponse("You are not authorized to access this page", status=401)

    recruitment_request_form = models.RecruitmentRequestForm()
    if request.method == "POST":
        recruitment_request_form = models.RecruitmentRequestForm(request.POST)
        if recruitment_request_form.is_valid():
            recruitment_request = models.RecruitmentRequest(planning_request=planning_request,
                               **recruitment_request_form.cleaned_data)
            recruitment_request.save()
            recruitment_request_form = models.RecruitmentRequestForm()

    planning_request = models.PlanningRequest.objects.get(
        pk=request_id)
    planning_request = model_to_dict(planning_request)
    planning_request.recruitment_requests_dicts = models_to_dicts(planning_request.recruitment_requests.all())
    return render(request, "recruitment_requests.html", {
        "planning_request": planning_request,
        "form": recruitment_request_form
    })


def create_financial_request(request, request_id):
    planning_request = models.PlanningRequest.objects.get(
        pk=request_id)

    if not(in_group(request.user, "psm")):
        return HttpResponse("You are not authorized to access this page", status=401)

    financial_request_form = models.FinancialRequestForm()
    if request.method == "POST":
        financial_request_form = models.FinancialRequestForm(request.POST)
        if financial_request_form.is_valid():
            financial_request = models.FinancialRequest(planning_request=planning_request,
                                                            **financial_request_form.cleaned_data)
            financial_request.save()
            financial_request_form = models.FinancialRequestForm()

    planning_request = models.PlanningRequest.objects.get(
        pk=request_id)
    planning_request = model_to_dict(planning_request)
    planning_request.financial_requests_dicts = models_to_dicts(planning_request.financial_requests.all())
    return render(request, "financial_requests.html", {
        "planning_request": planning_request,
        "form": financial_request_form
    })

def manage_recruitment_request(request, request_id):
    if not(in_group(request.user, "hrm")):
        return HttpResponse("You are not authorized to access this page", status=401)

    action = request.GET.get("action")
    recruitment_request_id = request.GET.get("recruitment_request_id")
    if action == "hired":
        recruitment_request = models.RecruitmentRequest.objects.get(pk=recruitment_request_id)
        recruitment_request.state = "hired"
        recruitment_request.save()
    elif action == "deny":
        recruitment_request = models.RecruitmentRequest.objects.get(pk=recruitment_request_id)
        recruitment_request.state = "denied"
        recruitment_request.save()

    planning_request = models.PlanningRequest.objects.get(
        pk=request_id)
    planning_request = model_to_dict(planning_request)
    planning_request.recruitment_requests_dicts = models_to_dicts(planning_request.recruitment_requests.all())
    return render(request, "manage_recruitment_requests.html", {
        "planning_request": planning_request
    })


def client(request):

    client_form = models.ClientForm()
    if request.method == "POST":
        client_form = models.ClientForm(request.POST)
        if not(in_group(request.user, "scso")):
            return HttpResponse("You are not authorized to access this page", status=401)

        if client_form.is_valid():
                client_form.save()

    clients = models.Client.objects.all()

    return render(request, "client.html", {
        "form": client_form,
        "clients": models_to_dicts(clients),
        "current_state": request.GET.get("state"),
        "groups": [group.name for group in request.user.groups.all()],
    })


def client_edit(request, client_id):
    client = models.Client.objects.get(pk=client_id)

    if not(in_group(request.user, "scso")):
        return HttpResponse("You are not authorized to access this page", status=401)
    saved = False
    
    if request.method == "POST":
        client_form = models.ClientForm(
            request.POST, instance=client)
        if client_form.is_valid():
            client_form.save()
            saved = True
    
    client_form = models.ClientForm(instance=client)
    return render(request, "client_edit.html", {
        "form": client_form,
        "client_id": client_id,
        "saved": saved
    })
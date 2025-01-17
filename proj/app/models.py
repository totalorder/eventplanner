from __future__ import unicode_literals
from django import forms

from django.forms.extras import SelectDateWidget
from django.db import models
from django.forms import ModelForm, fields

state_choices = (
    ("new", "New"),
    ("cso_approved", "CSO Approved"),
    ("scso_approved", "SCSO Approved"),
    ("fm_commented", "FM Commented"),
    ("adm_approved", "ADM Approved"),
)


class Client(models.Model):
    client_name = models.CharField(max_length=128)
    contact_information = models.TextField()

    def __str__(self):
        return self.client_name


class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = []


class PlanningRequest(models.Model):
    client = models.ForeignKey(Client, related_name='planning_requests', null=True)
    event_type = models.CharField(max_length=128)
    from_date = models.DateField()
    to_date = models.DateField()
    expected_no_attending = models.IntegerField()
    decoration = models.BooleanField()
    parties = models.BooleanField()
    drinks = models.BooleanField()
    food = models.BooleanField()
    media = models.BooleanField()
    expected_budget = models.IntegerField()
    state = models.CharField(max_length=15, choices=state_choices, default="new")
    budget_feedback = models.TextField(null=True)

    decoration_descr = models.TextField(null=True)
    parties_descr = models.TextField(null=True)
    drinks_descr = models.TextField(null=True)
    food_descr = models.TextField(null=True)
    media_descr = models.TextField(null=True)

class PlanningRequestForm(ModelForm):
    class Meta:
        model = PlanningRequest
        exclude = ["state", "budget_feedback",
                   "decoration_descr",
                   "parties_descr",
                   "drinks_descr",
                   "food_descr",
                   "media_descr"]

    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False)
    from_date = fields.DateField(widget=SelectDateWidget())
    to_date = fields.DateField(widget=SelectDateWidget())


class PlanningRequestDetailsForm(forms.Form):
    decoration_descr = forms.fields.CharField(required=False)
    parties_descr = forms.fields.CharField(required=False)
    drinks_descr = forms.fields.CharField(required=False)
    food_descr = forms.fields.CharField(required=False)
    media_descr = forms.fields.CharField(required=False)
    expected_budget = forms.fields.IntegerField()


class Task(models.Model):
    planning_request = models.ForeignKey(PlanningRequest,
                                         related_name='tasks')
    name = models.CharField(max_length=128)
    description = models.TextField()
    extra_needs = models.TextField(null=True)
    sub_team = models.CharField(choices=(
        ("video_photo", "Video and photography unit"),
        ("audio", "Audio unit"),
        ("graphics", "Graphics unit"),
        ("decoration", "Decoration unit"),
        ("network", "Networking unit"),
        ("food", "Food unit"),
        ("waiters", "Waiter staff"),
    ), max_length=128)


class TaskForm(ModelForm):
    name = models.CharField(max_length=128)
    description = models.TextField()
    extra_needs = models.TextField()

    class Meta:
        model = Task
        exclude = ["planning_request", "extra_needs"]


class RecruitmentRequest(models.Model):
    planning_request = models.ForeignKey(PlanningRequest,
                                         related_name='recruitment_requests')

    state = models.CharField(
        max_length=15, choices=(
            ("new", "New"),
            ("approved", "Approved"),
            ("denied", "Denied")),
        default="new")
    years_of_experience = models.IntegerField()
    job_title = models.CharField(max_length=512)
    job_description = models.TextField()

    contract_type = models.CharField(choices=(
        ("full_time", "Full time"),
        ("part_time", "Part time"),
    ), max_length=128)

    requesting_department = models.CharField(choices=(
        ("administration", "Administration"),
        ("service", "Service"),
        ("production", "Production"),
        ("financial", "Financial"),
    ), max_length=128)


class RecruitmentRequestForm(ModelForm):
    class Meta:
        model = RecruitmentRequest
        exclude = ["planning_request", "state"]


class FinancialRequest(models.Model):
    planning_request = models.ForeignKey(PlanningRequest,
                                         related_name='financial_requests')

    required_amount = models.IntegerField()
    reason = models.TextField()
    state = models.CharField(
        max_length=15, choices=(
            ("new", "New"),
            ("hired", "Hired"),
            ("denied", "Denied")),
        default="new")

    requesting_department = models.CharField(choices=(
        ("administration", "Administration"),
        ("service", "Service"),
        ("production", "Production"),
        ("financial", "Financial"),
    ), max_length=128)


class FinancialRequestForm(ModelForm):
    class Meta:
        model = FinancialRequest
        exclude = ["planning_request", "state"]

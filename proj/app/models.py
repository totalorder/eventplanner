from __future__ import unicode_literals

from django.forms.extras import SelectDateWidget
from django.db import models
from django.forms import ModelForm, fields


class PlanningRequest(models.Model):
    client_name = models.CharField(max_length=128)
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
    state = models.CharField(max_length=15, choices=(
        ("new", "New"),
        ("cso_approved", "CSO Approved"),
        ("fm_commented", "FM Commented"),
    ), default="new")


class PlanningRequestForm(ModelForm):
    class Meta:
        model = PlanningRequest
        exclude = []

    from_date = fields.DateField(widget=SelectDateWidget())
    to_date = fields.DateField(widget=SelectDateWidget())

from datetime import datetime, timedelta
from django.contrib.auth.models import User, Group
from django.test import TestCase
from app import models

planning_request_data = dict(
    expected_no_attending=1,
    client_name="client_name",
    event_type="event_type",
    decoration=False,
    parties=False,
    drinks=False,
    food=False,
    media=False,
    expected_budget=3,
    from_date=datetime.now(),
    to_date=datetime.now() + timedelta(days=3),
)

class TestView(TestCase):
    def setUp(self):
        cso_user = User.objects.create_user('cso', 'cso@cso.com', 'eventplanner')
        cso = Group.objects.create()
        cso.name = 'cso'
        cso.save()
        cso_user.groups.add(cso)
        cso_user.save()

        scso_user = User.objects.create_user('scso', 'scso@scso.com', 'eventplanner')
        scso = Group.objects.create()
        scso.name = 'scso'
        scso.save()
        scso_user.groups.add(scso)
        scso_user.save()


        models.PlanningRequest.objects.create(**planning_request_data)
        models.PlanningRequest.objects.create(
            **dict(state="cso_approved", **planning_request_data))

    def test_planning_not_accessible_by_anonymous(self):
        response = self.client.get('/planning-request/')
        self.assertEqual(response.status_code, 401)

    def test_planning_accessible_by_cso(self):
        self.client.login(username='cso', password='eventplanner')
        response = self.client.get('/planning-request/')
        self.assertEqual(response.status_code, 200)

    def test_list_planning(self):
        self.client.login(username='scso', password='eventplanner')
        response = self.client.get('/planning-request/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["planning_requests"]), 2)

    def test_list_planning_with_state(self):
        self.client.login(username='scso', password='eventplanner')
        response = self.client.get('/planning-request/?state=cso_approved')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["planning_requests"]), 1)

    def test_create_planning_request(self):
        self.client.login(username='cso', password='eventplanner')
        response = self.client.post('/planning-request/', {
            "client_name": "Client",
            "event_type": "fiesta",
            "from_date": "2016-10-12",
            "to_date": "2016-10-15",
            "expected_no_attending": 40000,
            "decoration": "",
            "parties": "",
            "drinks": "",
            "food": "",
            "media": "",
            "expected_budget": 4000000
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.PlanningRequest.objects.all().count(), 1)

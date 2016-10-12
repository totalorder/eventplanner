from django.contrib.auth.models import User, Group
from django.test import TestCase
from app import models


class TestView(TestCase):
    def setUp(self):
        cso_user = User.objects.create_user('cso', 'cso@cso.com', 'eventplanner')
        cso = Group.objects.create()
        cso.name = 'cso'
        cso.save()

        cso_user.groups.add(cso)
        cso_user.save()

    def test_planning_not_accessible_by_anonymous(self):
        response = self.client.get('/planning-request/')
        self.assertEqual(response.status_code, 401)

    def test_planning_accessible_by_cso(self):
        self.client.login(username='cso', password='eventplanner')
        response = self.client.get('/planning-request/')
        self.assertEqual(response.status_code, 200)

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

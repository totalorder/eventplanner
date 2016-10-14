from copy import copy
from datetime import datetime, timedelta
from django.contrib.auth.models import User, Group
from django.test import TestCase
from app import models

planning_request_data = dict(
    expected_no_attending=1,
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

planning_request_form_data = {
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
}

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

        fm_user = User.objects.create_user('fm', 'fm@fm.com', 'eventplanner')
        fm = Group.objects.create()
        fm.name = 'fm'
        fm.save()
        fm_user.groups.add(fm)
        fm_user.save()

        adm_user = User.objects.create_user('adm', 'adm@adm.com', 'eventplanner')
        adm = Group.objects.create()
        adm.name = 'adm'
        adm.save()
        adm_user.groups.add(adm)
        adm_user.save()

        psm_user = User.objects.create_user('psm', 'psm@psm.com', 'eventplanner')
        psm = Group.objects.create()
        psm.name = 'psm'
        psm.save()
        psm_user.groups.add(psm)
        psm_user.save()

        hrm_user = User.objects.create_user('hrm', 'hrm@hrm.com', 'eventplanner')
        hrm = Group.objects.create()
        hrm.name = 'hrm'
        hrm.save()
        hrm_user.groups.add(hrm)
        hrm_user.save()        
        
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
        response = self.client.post('/planning-request/', planning_request_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.PlanningRequest.objects.all().count(), 3)

    def test_edit_planning_request(self):
        self.client.login(username='scso', password='eventplanner')

        planning_request = models.PlanningRequest.objects.all().first()
        self.assertEquals(planning_request.event_type, "event_type")

        planning_request_form_data_copy = copy(planning_request_form_data)
        planning_request_form_data_copy["event_type"] = "korv"
        response = self.client.post('/planning-request/edit/%s' % planning_request.id,
                                    planning_request_form_data_copy)
        self.assertEqual(response.status_code, 200)
        planning_request = models.PlanningRequest.objects.get(pk=planning_request.id)
        self.assertEquals(planning_request.event_type, "korv")

    def test_write_planning_request_feedback(self):
        self.client.login(username='fm', password='eventplanner')

        planning_request = models.PlanningRequest.objects.all().first()
        planning_request.state = "scso_approved"
        planning_request.save()
        self.assertEquals(planning_request.budget_feedback, None)

        response = self.client.post('/planning-request/write-feedback/%s' % planning_request.id,
                                    {"feedback": "Korv"})
        self.assertEqual(response.status_code, 200)
        planning_request = models.PlanningRequest.objects.get(pk=planning_request.id)
        self.assertEquals(planning_request.budget_feedback, "Korv")
        self.assertEquals(planning_request.state, "fm_commented")

    def test_adm_approve_planning_request(self):
        planning_request = models.PlanningRequest.objects.all().first()
        planning_request.state = "fm_commented"
        planning_request.save()

        self.client.login(username='adm', password='eventplanner')

        response = self.client.post('/planning-request/approve', {
            "new_state": "adm_approved",
            "planning_request_id": planning_request.id
        })

        planning_request = models.PlanningRequest.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(planning_request.state, "adm_approved")

    def test_create_task(self):
        planning_request = models.PlanningRequest.objects.all().first()
        self.assertEqual(planning_request.tasks.all().count(), 0)

        self.client.login(username='psm', password='eventplanner')
        response = self.client.post(
            '/task/create/%s' % planning_request.id, {
                "name": "Name",
                "description": "Description",
                "sub_team": "food",
            })

        self.assertEqual(response.status_code, 200)
        planning_request = models.PlanningRequest.objects.all().first()
        self.assertEqual(planning_request.tasks.all().count(), 1)

    def test_create_recruitment_request(self):
        planning_request = models.PlanningRequest.objects.all().first()
        self.assertEqual(planning_request.recruitment_requests.all().count(), 0)

        self.client.login(username='psm', password='eventplanner')
        response = self.client.post(
            '/recruitment-request/create/%s' % planning_request.id, {
                "years_of_experience": 3,
                "job_title": "Job title",
                "job_description": "Job description",
                "contract_type": "full_time",
                "requesting_department": "service",
            })

        self.assertEqual(response.status_code, 200)
        planning_request = models.PlanningRequest.objects.all().first()
        self.assertEqual(planning_request.recruitment_requests.all().count(), 1)

    def test_create_financial_request(self):
        planning_request = models.PlanningRequest.objects.all().first()
        self.assertEqual(planning_request.financial_requests.all().count(), 0)

        self.client.login(username='psm', password='eventplanner')
        response = self.client.post(
            '/financial-request/create/%s' % planning_request.id, {
                "required_amount": 30000,
                "reason": "Give me all your money",
                "requesting_department": "service",
            })

        self.assertEqual(response.status_code, 200)
        planning_request = models.PlanningRequest.objects.all().first()
        self.assertEqual(planning_request.financial_requests.all().count(), 1)


    def test_manage_recruitment_request(self):
        planning_request = models.PlanningRequest.objects.all().first()
        recruitment_request = models.RecruitmentRequest(**{"years_of_experience": 3,
                                   "job_title": "Job title",
                                   "job_description": "Job description",
                                   "contract_type": "full_time",
                                   "requesting_department": "service"})
        recruitment_request.planning_request = planning_request
        recruitment_request.save()
        self.client.login(username='hrm', password='eventplanner')
        response = self.client.get(
            '/recruitment-request/manage/%s?recruitment_request_id=%s&action=hired' %
            (planning_request.id, recruitment_request.id))

        self.assertEqual(response.status_code, 200)
        planning_request = models.PlanningRequest.objects.all().first()
        recruitment_request = planning_request.recruitment_requests.all().first()

        self.assertEqual(recruitment_request.state, "hired")

    def test_create_client(self):
        self.client.login(username='scso', password='eventplanner')
        response = self.client.post('/client/', {
            "client_name": "Client name",
            "contact_information": "Contact information"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Client.objects.all().count(), 1)

    def test_edit_planning_request_details(self):
        self.client.login(username='psm', password='eventplanner')

        planning_request = models.PlanningRequest.objects.all().first()
        planning_request.state = "adm_approved"
        planning_request.save()
        self.assertEquals(planning_request.food_descr, None)

        response = self.client.post('/planning-request/edit/%s' % planning_request.id,
                                    {"food_descr": "korv",
                                     "parties_descr": "",
                                     "drinks_descr": "",
                                     "media_descr": "",
                                     "decoration_descr": "",
                                     "expected_budget": 334})
        self.assertEqual(response.status_code, 200)
        planning_request = models.PlanningRequest.objects.get(pk=planning_request.id)
        self.assertEquals(planning_request.food_descr, "korv")
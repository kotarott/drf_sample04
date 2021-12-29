import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from profiles.models import Profile, ProfileStatus
from profiles.api.serializers import ProfileSerializer, ProfileStatusSerialzier


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {
            "username": "testcase",
            "email": "test@testcase.com",
            "password1": "pass202112",
            "password2": "pass202112"
        }
        
        response = self.client.post("/api/rest-auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileViewSetTestCase(APITestCase):

    list_url = reverse("profile-list")

    def setUp(self):
        self.user = User.objects.create_user(username="davinci",
                                             password="pass202201")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_detail_retrieve(self):
        response = self.client.get(reverse("profile-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], "davinci")

    def test_profile_update_by_owner(self):
        response = self.client.put(reverse("profile-detail", kwargs={"pk": 1}),
                                   {"city": "Kyoto", "bio": "Renaissance Genius"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"id": 1, "user": "davinci", "bio": "Renaissance Genius",
                                                        "city": "Kyoto", "avater": None})
        
    def test_profile_update_by_random_user(self):
        random_user = User.objects.create_user(username="random", password="psw123123")
        self.client.force_authenticate(user=random_user)
        response = self.client.put(reverse("profile-detail", kwargs={"pk": 1}),
                                   {"city": "Kyoto", "bio": "hacked!!"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProfileStatusViewSetTestCase(APITestCase):

    list_url = reverse("status-list")

    def setUp(self):
        self.user = User.objects.create_user(username="davinci",
                                             password="pass202201")
        self.status = ProfileStatus.objects.create(user_profile=self.user.profile,
                                                    status_content="statusstest")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_status_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_status_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_status_create(self):
        data = {"status_content": "a test content"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_profile'], "davinci")
        self.assertEqual(response.data['status_content'], "a test content")

    def test_single_status_retrieve(self):
        serializer_data = ProfileStatusSerialzier(instance=self.status).data
        response = self.client.get(reverse('status-detail', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_status_update_owner(self):
        data = {"status_content": "content updated"}
        response = self.client.put(reverse("status-detail", kwargs={"pk": 1}),data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status_content"], "davinci")

    def test_status_update_random_user(self):
        random_user = User.objects.create_user(username="random", password="psw123123")
        data = {"status_conten": "you hacked!!"}
        self.client.force_authenticate(user=random_user)
        response = self.client.put(reverse('status-detail', kwargs={"pk": 1}),
                                            data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

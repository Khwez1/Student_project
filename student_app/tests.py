from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Student, ClassGroup
from django.contrib.auth.models import User
# Create your tests here.
class StudentAPITests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="password123"
        )

        self.other_user = User.objects.create_user(
            username="other",
            password="password123"
        )

        self.group = ClassGroup.objects.create(name="Test Class")
        self.student = Student.objects.create(
            name="Test Student",
            mark=75,
            created_by=self.owner,
            class_group=self.group
        )

    def test_DOC_001_list_students_returns_200(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_DOC_002_create_student_with_invalid_mark_returns_400(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            '/students/',
            data={
                "name":"fake student",
                "mark":150
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_DOC_003_update_student_with_credentials_returns_204(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            f'/students/{self.student.id}',
            data={
                'mark': 89
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
from datetime import datetime
import unittest

from django.db import models
from models import *

class UserProfileTestCase(unittest.TestCase):
    """ Test the user profile convenience methods """
    def setUp(self):
        self.user = User.objects.create_user("John Doe", "test@test.com",
                "password")
        self.faculty = FacultyTable.objects.create(Username=self.user,
                Faculty_GName="John", Faculty_SName="Doe", Review_Term=2,
                Department="Test", Faculty_Start=datetime.now())

    def testGetFullName(self):
        self.assertEquals(self.faculty.get_full_name(), "John Doe")

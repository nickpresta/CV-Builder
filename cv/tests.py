from datetime import datetime
import unittest

from django.db import models
from models import *

class UserProfileTestCase(unittest.TestCase):
    """ Test the user profile convenience methods """
    def setUp(self):
        self.user = User.objects.create_user("John Doe", "test@test.com",
                "password")
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.save()

    def testGetFullName(self):
        self.assertEquals(self.user.get_full_name(), "John Doe")

import os

from django.db import models
from django.contrib.auth.models import User

# This autogenerates a tuple list of departments from a
# departments.txt file that can be manually edited
# The file is initially generated from the utils/generate_departments.py
try:
    # department file in the current directory
    path = os.path.abspath(os.path.dirname(__file__) + os.sep + "departments.txt")
    with open(path) as f:
        tmp_list = map(lambda s: s.strip(), f.readlines())
        departments = [(d, d)for d in tmp_list]
except IOError:
    print "Could not find department list!"
    departments = ()

class UserProfile(models.Model):
    """ This class is used to hold additional information
        related to the user itself """
    DEPARTMENT_CHOICES = departments

    # This links the already created user (from LDAP login)
    # to our profile
    user = models.ForeignKey(User, unique=True)

    review_term = models.IntegerField(default=2)
    faculty_start = models.DateField()
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)

class DistributionOfEffort(models.Model):
    """ This class holds information about the DoE for a
        given employee (Teaching, Research, Service) """
    user = models.ForeignKey(User)
    year = models.DateField()
    # These three fields should add up to 100 (%)
    research = models.IntegerField(default=40)
    teaching = models.IntegerField(default=40)
    service = models.IntegerField(default=20)

class Summary(models.Model):
    user = models.ForeignKey(User)
    executive = models.TextField()




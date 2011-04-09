# -*- coding: utf-8 -*-
import os
import datetime
import re

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class FacultyKeyMixin:
    def setPK(self, pk):
        self.user_id = pk

class GrantKeyMixin:
    def setPK(self, pk):
        self.grant = pk

class UserProfile(models.Model):
    """ This class is used to hold additional information
        related to the user itself """

    # This links the already created user (from LDAP login)
    # to our profile
    user = models.ForeignKey(User, unique=True)

    review_term = models.IntegerField("Review Term (in years)", default=2,
            blank=True, null=True)
    faculty_start = models.DateField("Faculty Start Date", blank=True, null=True)
    departments = models.CharField("Departments (comma delimited)",
            max_length=100, blank=True, null=True)

def create_user_profile(sender, instance, created, **kwargs):
    """ Automatically create a profile when a user is created """
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

# Connect them
post_save.connect(create_user_profile, sender=User)

SEMESTERS = [('f', 'Fall'), ('w', 'Winter'), ('s', 'Summer')]

class DistributionOfEffort(models.Model, FacultyKeyMixin):
    """ This class holds information about the DoE for a
        given employee (Teaching, Research, Service) """
    user = models.ForeignKey(User)
    year = models.DateField(unique=False)
    # These three fields should add up to 100 (%)
    research = models.IntegerField(default=40)
    teaching = models.IntegerField(default=40)
    service = models.IntegerField(default=20)

class Summary(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    executive = models.TextField("Executive Summary", max_length=10000, blank=True)
    off_campus = models.TextField(max_length=10000, blank=True)

    # the following fields refer to research
    research  = models.TextField(max_length=10000, blank=True)
    research_professional_consulting = models.CharField(max_length=10000, blank=True)
    research_patents = models.CharField(max_length=10000, blank=True)
    research_other_activities = models.CharField(max_length=10000, blank=True)
    research_recognition = models.CharField(max_length=10000, blank=True)

    # the following fields refer to teaching
    teaching = models.CharField(max_length=10000, blank=True)
    teaching_counselling = models.CharField(max_length=10000, blank=True)
    teaching_course_development = models.CharField(max_length=10000, blank=True)
    teaching_recognition = models.CharField(max_length=10000, blank=True)
    teaching_support = models.CharField(max_length=10000, blank=True)
    teaching_scholarship = models.CharField(max_length=10000, blank=True)
    teaching_other = models.CharField(max_length=10000, blank=True)

class Accred(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    degree = models.CharField(max_length=200, blank=True)
    discipline = models.CharField(max_length=200, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    date = models.DateField(blank=True)

class Honor(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    description = models.CharField(max_length=500, blank=True)

class PositionHeld(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    rank = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    location = models.CharField(max_length=200, blank=True)

class PositionPrior(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=200, blank=True)

class PositionElsewhere(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=200, blank=True)

class Grant(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    agency = models.CharField(max_length=200, blank=True, null=True)
    support_type = models.CharField(max_length=200, blank=True, null=True)
    project_title = models.CharField(max_length=200, blank=True, null=True)
    held = models.BooleanField()

    def __unicode__(self):
        rv = self.agency
        if self.support_type:
            rv += ", " + self.support_type
        if self.project_title:
            rv += ": " + self.project_title
        return rv

class GrantYear(models.Model, GrantKeyMixin):
    grant = models.ForeignKey(Grant)
    amount = models.FloatField(blank=True, null=True)
    start_year = models.DateField(blank=True, null=True)
    end_year = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=200, blank=True)

class Investigator(models.Model, GrantKeyMixin):
    grant = models.ForeignKey(Grant)
    name = models.CharField(max_length=200, blank=True)
    amount = models.FloatField(blank=True)
    role = models.CharField(max_length=2, choices=(('p', 'Principle'), ('s', 'Other')))

class Course(models.Model):
    code = models.CharField(max_length=200, blank=True, primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    info = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.code

    def save(self, *args, **kwargs):
        """ We need to ensure that there is some form of uniformity when storing
            course codes """

        # replace multiple spaces with one
        self.code = re.sub("\s+", "", self.code)
        self.code = self.code.replace("*", "")
        # Ensure that course codes of CIS375 get saved as CIS3750
        num = re.split("(\D)", self.code)
        if len(num[-1]) < 4:
            self.code = self.code + "0"
        # call the "real" save
        super(Course, self).save(*args, **kwargs)

class FacultyCourseJoin(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    year = models.DateField(blank=True, null=True)
    semester = models.CharField(max_length=200, blank=True, choices=SEMESTERS)
    num_students = models.IntegerField(blank=True, null=True)

class BaseGradAdvisor(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    student_name = models.CharField(max_length=200, blank=True)
    degree = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

class GradAdvisor(BaseGradAdvisor):
    pass

class GradAdvisorCommitteeMember(BaseGradAdvisor):
    pass

class GradExaminer(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    student_name = models.CharField(max_length=200, blank=True)
    degree = models.CharField(max_length=200, blank=True)
    date = models.DateField(blank=True, null=True)

roles = [('c', 'Chair'), ('m', 'Member')]

class Service(models.Model, FacultyKeyMixin):
    service_levels = [('u', 'University'), ('d', 'Department'), ('c', 'College'), ('e', 'External')]
    user = models.ForeignKey(User)
    start_semester = models.CharField(max_length=200, blank=True, choices=SEMESTERS)
    start_year = models.DateField(blank=True, null=True)
    end_semester = models.CharField(max_length=200, blank=True, choices=SEMESTERS)
    end_year = models.DateField(blank=True, null=True)
    committee = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=200, blank=True, choices=roles)
    chair = models.CharField(max_length=200, blank=True)
    other = models.CharField(max_length=200, blank=True)
    level = models.CharField(max_length=200, blank=True, choices=service_levels)

    def __unicode__(self):
        return self.committee

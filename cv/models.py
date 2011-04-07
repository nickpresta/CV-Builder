# -*- coding: utf-8 -*-
import os
import datetime

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

class DistributionOfEffort(models.Model, FacultyKeyMixin):
    """ This class holds information about the DoE for a
        given employee (Teaching, Research, Service) """
    user = models.ForeignKey(User)
    year = models.DateField()
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

class PositionPriorTable(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    StartDate = models.DateField(blank=True)
    EndDate = models.DateField(blank=True)
    Location = models.CharField(max_length=200, blank=True)
    Position = models.CharField(max_length=200, blank=True)

class PositionElsewhereTable(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    StartDate = models.DateField(blank=True)
    EndDate = models.DateField(blank=True)
    Location = models.CharField(max_length=200, blank=True)
    Position = models.CharField(max_length=200, blank=True)

class GrantTable(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    Agency = models.CharField(max_length=200, blank=True)
    SupportType = models.CharField(max_length=200, blank=True)
    ProjectTitle = models.CharField(max_length=200, blank=True)
    Held = models.BooleanField()

    def __unicode__(self):
        rv = self.Agency
        if self.SupportType:
            rv += ", " + self.SupportType
        if self.ProjectTitle:
            rv += ": " + self.ProjectTitle
        return rv

class GrantYearTable(models.Model, GrantKeyMixin):
    Grant = models.ForeignKey(GrantTable)
    Amount = models.FloatField(blank=True)
    StartYear = models.DateField(blank=True)
    EndYear = models.DateField(blank=True)
    Title = models.CharField(max_length=200, blank=True)

class InvestigatorTable(models.Model, GrantKeyMixin):
    Grant = models.ForeignKey(GrantTable)
    Name = models.CharField(max_length=200, blank=True)
    Amount = models.FloatField(blank=True)
    Role = models.CharField(max_length=2, choices=(('p', 'Principle'), ('s', 'Other')))

class CourseTable(models.Model): 
    #CID = models.IntegerField()
    CCode = models.CharField(max_length=200, blank=True, unique=True)
    Name = models.CharField(max_length=200, blank=True)
    Info = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.CCode + ': ' + self.Name

class FacultyCourseJoinTable(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    CCode = models.ForeignKey(CourseTable)
    Year = models.DateField(blank=True)
    Semester = models.CharField(max_length=200, blank=True)
    NumStudents = models.IntegerField(blank=True)

class GradTable(models.Model, FacultyKeyMixin):
    user = models.ForeignKey(User)
    GName = models.CharField(max_length=200, blank=True)
    GDegree = models.CharField(max_length=200, blank=True)
    SDate = models.DateField(blank=True)
    EDate = models.DateField(blank=True)
    Note = models.CharField(max_length=200, blank=True)


class ServiceTable(models.Model, FacultyKeyMixin):
    service_levels = [('u', 'University'), ('d', 'Department'), ('c', 'College'), ('e', 'External')]
    roles = [('c', 'Chair'), ('m', 'Member')]
    semesters = [('f', 'Fall'), ('w', 'Winter'), ('s', 'Summer')]

    user = models.ForeignKey(User)
    SSem = models.CharField(max_length=200, blank=True, choices=semesters)
    SYear = models.IntegerField(blank=True)
    ESem = models.CharField(max_length=200, blank=True, choices=semesters)
    EYear = models.IntegerField(blank=True)
    Committee = models.CharField(max_length=200, blank=True)
    Role = models.CharField(max_length=200, blank=True, choices=roles)
    Chair = models.CharField(max_length=200, blank=True)
    Other = models.CharField(max_length=200, blank=True)
    Level = models.CharField(max_length=200, blank=True, choices=service_levels)

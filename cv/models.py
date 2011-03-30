# -*- coding: utf-8 -*-
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

    review_term = models.IntegerField(default=2, blank=True)
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

# using this model for Demo 2. Didn't have time to adapt models.
class Summary(models.Model):
    user = models.ForeignKey(User)
    executive = models.TextField()


class FacultyTable(models.Model):
    Faculty_ID = models.AutoField( primary_key=True )
    
    # This links the already created user (from LDAP login)
    # to our profile
    Username = models.ForeignKey(User, unique=True)

    Faculty_GName = models.CharField(max_length=200, blank=True)
    Faculty_SName = models.CharField(max_length=200, blank=True)
    Review_Term = models.IntegerField(null=True, blank=True)
    Department = models.CharField(max_length=200, blank=True )
    Faculty_Start = models.DateField( blank=True, null=True )
    
class DoETable(models.Model):
    #DoE_ID = models.IntegerField() #TODO: 
    Faculty_ID = models.ForeignKey(FacultyTable)
    Year = models.DateField(blank=True, unique=True )
    #These three fields should add up to 100 (%)
    Research = models.IntegerField( default=40 )
    Teaching = models.IntegerField( default=40 )
    Service = models.IntegerField( default=20 )
    
class SummaryTable(models.Model):
    Faculty_ID = models.ForeignKey(FacultyTable)
    Executive = models.TextField(max_length=10000, blank=True )
    Research  = models.TextField(max_length=10000, blank=True )
    R_Consulting = models.CharField(max_length=10000, blank=True )
    R_Patents = models.CharField(max_length=10000, blank=True )
    R_Other = models.CharField(max_length=10000, blank=True )
    R_Recognition = models.CharField(max_length=10000, blank=True )
    Teaching = models.CharField(max_length=10000, blank=True )
    T_Counselling = models.CharField(max_length=10000, blank=True )
    T_CourseDevel = models.CharField(max_length=10000, blank=True )
    T_Recognition = models.CharField(max_length=10000, blank=True )
    T_Support = models.CharField(max_length=10000, blank=True )
    T_Scholarship = models.CharField(max_length=10000, blank=True )
    T_Offer = models.CharField(max_length=10000, blank=True )
    OffCampus = models.TextField(max_length=10000, blank=True )

class AccredTable(models.Model):
    #Accred_ID = models.IntegerField()
    Faculty_ID = models.ForeignKey(FacultyTable)
    Degree = models.CharField(max_length=200, blank=True )
    Discipline = models.CharField(max_length=200, blank=True )
    Institution = models.CharField(max_length=200, blank=True )
    Date = models.DateField( blank=True )
    
class HonorTable(models.Model):
    #Honor_ID = models.IntegerField()
    Faculty_ID = models.ForeignKey(FacultyTable)
    Honor_desc = models.CharField(max_length=500, blank=True )
    
#class PositionTable(models.Model):
#    #Pos_ID = models.IntegerField()
#    Faculty_ID = models.ForeignKey(FacultyTable)
#    #Rank = models.CharField(max_length=200, blank=True )
#    StartDate = models.DateField( blank=True )
#    EndDate = models.DateField( blank=True )
#    Location = models.CharField(max_length=200, blank=True )

class PositionHeldTable(models.Model):
    #Pos_ID = models.IntegerField()
    Faculty_ID = models.ForeignKey(FacultyTable)
    Rank = models.CharField(max_length=200, blank=True )
    StartDate = models.DateField( blank=True )
    EndDate = models.DateField( blank=True )
    Location = models.CharField(max_length=200, blank=True )

class PositionPriorTable(models.Model):
    #Pos_ID = models.IntegerField()
    Faculty_ID = models.ForeignKey(FacultyTable)
    StartDate = models.DateField( blank=True )
    EndDate = models.DateField( blank=True )
    Location = models.CharField(max_length=200, blank=True )
    Position = models.CharField(max_length=200, blank=True )

class PositionElsewhereTable(models.Model):
    #Pos_ID = models.IntegerField()
    Faculty_ID = models.ForeignKey(FacultyTable)
    StartDate = models.DateField( blank=True )
    EndDate = models.DateField( blank=True )
    Location = models.CharField(max_length=200, blank=True )
    Position = models.CharField(max_length=200, blank=True )
    
class GrantTable(models.Model):
    #Grant_ID = models.IntegerField()
    Faculty_ID = models.ForeignKey( FacultyTable )
    PInvest = models.IntegerField( blank=True )
    SYear = models.DateField( blank=True )
    EYear = models.DateField( blank=True )
    Amount = models.FloatField( blank=True )

class InvestTable(models.Model):
    #Invest_ID = models.IntegerField()
    Faculty_ID = models.ForeignKey( FacultyTable )
    Invest_Name = models.CharField(max_length=200, blank=True )
    Grant_ID = models.IntegerField( blank=True )
    Portion = models.FloatField( blank=True )

class CourseTable(models.Model): 
    #CID = models.IntegerField()
    CCode = models.CharField(max_length=200, blank=True, unique=True )
    Name = models.CharField(max_length=200, blank=True )
    Info = models.CharField(max_length=200, blank=True )
 
class FacultyCourseJoinTable( models.Model ):
    Faculty_ID = models.ForeignKey( FacultyTable )
    CCode = models.ForeignKey( CourseTable )
    Year = models.DateField( blank=True )
    Semester = models.CharField(max_length=200, blank=True )
    NumStudents = models.IntegerField( blank=True )

class GradTable(models.Model):
    #GID = models.IntegerField()
    Faculty_ID = models.ForeignKey( FacultyTable )
    GName = models.CharField(max_length=200, blank=True )
    GDegree = models.CharField(max_length=200, blank=True )
    SDate = models.DateField( blank=True )
    EDate = models.DateField( blank=True )
    Note = models.CharField(max_length=200, blank=True )

class ServiceTable(models.Model):
    #GID = models.IntegerField()
    Faculty_ID = models.ForeignKey( FacultyTable )
    S_ID = models.IntegerField(blank=True)
    SSem = models.CharField(max_length=200, blank=True)
    SYear = models.IntegerField(blank=True)
    ESem = models.CharField(max_length=200, blank=True)
    EYear = models.IntegerField(blank=True)
    Committee = models.CharField(max_length=200, blank=True)
    Role = models.CharField(max_length=200, blank=True)
    Chair = models.CharField(max_length=200, blank=True)
    Other = models.CharField(max_length=200, blank=True)
    Level = models.CharField(max_length=200, blank=True)

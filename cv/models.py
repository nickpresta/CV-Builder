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


class FacultyTable(models.Model):
    #Faculty_ID = models.IntegerField()
    Faculty_GName = models.CharField( max_length=200 )
    Faculty_SName = models.CharField( max_length=200 )
    Review_Term = models.IntegerField()
    Department = models.CharField( max_length=200 ) #TODO: Pre-pop?
    Faculty_Start = models.DateTimeField(  ) #TODO: trigger
    
class DoETable(models.Model):
    #DoE_ID = models.IntegerField() #TODO: 
    Faculty_ID = models.ForeignKey( FacultyTable )
    Year = models.IntegerField( max_length=4 )
    Research = models.IntegerField()
    Teaching = models.IntegerField()
    Service = models.IntegerField()
    
class SummaryTable(models.Model):
    Faculty_ID = models.ForeignKey( FacultyTable )
    Executive = models.CharField( max_length=10000 )
    Research  = models.CharField( max_length=10000 )
    R_Consulting = models.CharField( max_length=10000 )
    R_Patents = models.CharField( max_length=10000 )
    R_Other = models.CharField( max_length=10000 )
    R_Recognition = models.CharField( max_length=10000 )
    Teaching = models.CharField( max_length=10000 )
    T_Counselling = models.CharField( max_length=10000 )
    T_CourseDevel = models.CharField( max_length=10000 )
    T_Recognition = models.CharField( max_length=10000 )
    T_Support = models.CharField( max_length=10000 )
    T_Scholarship = models.CharField( max_length=10000 )
    T_Offer = models.CharField( max_length=10000 )
    OffCampus = models.CharField( max_length=10000 )

class AccredTable(models.Model):
    #Accred_ID = models.IntegerField()
    Faculty_ID = models.ForeignKey( FacultyTable )
    Degree = models.CharField( max_length=200 )
    Discipline = models.CharField( max_length=200 )
    Institution = models.CharField( max_length=200 )
    Date = models.DateTimeField() #TODO: Trigger
    
class HonorTable(models.Model):
    #Honor_ID = models.IntegerField()
    Faculty_ID = models.ForeignKey( FacultyTable )
    Honor_desc = models.CharField( max_length=500 )
    
class PositionTable(models.Model):
    #Pos_ID = models.IntegerField()
    Faculty_ID = models.ForeignKey( FacultyTable )
    Rank = models.CharField( max_length=200 )
    StartDate = models.DateTimeField() #TODO: Trigger
    EndDate = models.DateTimeField()
    Location = models.CharField( max_length=200 )
    
class GrantTable(models.Model):
    #Grant_ID = models.IntegerField()
    PInvest = models.IntegerField()
    SYear = models.DateTimeField() #TODO: Trigger
    EYear = models.DateTimeField() #TODO: Trigger
#TODO:  Amount = Formatted Float

class InvestTable(models.Model):
    #Invest_ID = models.IntegerField()
    Invest_Name = models.CharField( max_length=200 )
    Grant_ID = models.IntegerField()
#TODO:  Portion Formatted Float
 
class CourseTable(models.Model): 
    #CID = models.IntegerField()
    CCode = models.CharField( max_length=200 )
    Semester = models.CharField( max_length=200 )
    Year = models.DateTimeField() #TODO: Trigger
    Name = models.CharField( max_length=200 )
    Info = models.CharField( max_length=200 )
    NumStudents = models.IntegerField()
 
class GradTable:
    #GID = models.IntegerField()
    Faculty_ID = models.IntegerField()
    GName = models.CharField( max_length=200 )
    GDegree = models.CharField( max_length=200 )
    SDate = models.DateTimeField() #TODO: Trigger
    EDate = models.DateTimeField() #TODO: Trigger
    Note = models.CharField( max_length=200 )

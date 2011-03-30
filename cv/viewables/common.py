from cv.forms import *
from cv.models import *

def getFaculty(user):
    """ Retrieve a member from the FacultyTable by username, or create one if it
        does not exist """

    try:
        return FacultyTable.objects.get(Username=user)
    except FacultyTable.DoesNotExist:
        fac = FacultyTable(Username=user)
        fac.save()
        return fac


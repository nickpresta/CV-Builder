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

def createContext(formsetInfo, formInfo, postData=None, files=None):
    formsets = dict((
        formsetName,
        Formset(postData, files, pk=key, queryset=qs, prefix=pf)
    ) for formsetName, (Formset, qs, pf, key) in formsetInfo.iteritems())

    forms = dict((
        formName,
        Form(postData, files, pk=key, instance=ins, prefix=pf)
    ) for formName, (Form, ins, pf, key) in formInfo.iteritems())
    return formsets, forms


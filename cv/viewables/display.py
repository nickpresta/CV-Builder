# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory

from cv.forms import *
from cv.models import *

# utility functions

def getFaculty(user):
    """ Retrieve a member from the FacultyTable by username, or create one if it
        does not exist """
        
    try:
        return FacultyTable.objects.get(Username=user)
    except FacultyTable.DoesNotExist:
        return FacultyTable(Username=user)

def index(request):
    """ Responsible for showing the index page """

    return direct_to_template(request, 'index.html', {'status': 'works!'})

@login_required
def editcv(request):
    return direct_to_template(request, 'editcv.html', {})

@login_required
def form1(request):
    return direct_to_template(request, 'form1.html', {})

@login_required
def executive(request):
    """ Create a form view for the Distribution of Effort """

    faculty = getFaculty(request.user)

    # get this user's Summary or else create a new one
    try:
        summaryData = SummaryTable.objects.get(Faculty_ID=faculty)
    except SummaryTable.DoesNotExist:
        summaryData = SummaryTable(Faculty_ID=faculty)

    # get this user's DoEs or else create a new one
    try:
        doeData = DoETable.objects.filter(Faculty_ID=faculty).order_by('Year')
    except DoETable.DoesNotExist:
        doeData = DoETable(Faculty_ID=faculty)

    if request.method == 'POST':
        summaryFormset = ExecutiveSummaryForm(request.POST, request.FILES,
                instance=summaryData, prefix='summary')
        doeFormset = modelformset_factory(DoETable,
                form=DoEForm, extra=1, can_delete=True)(request.POST,
                        request.FILES, queryset=doeData, prefix='doe')

        if summaryFormset.is_valid() and doeFormset.is_valid():
            # Save the form data, ensure they are updating as themselves
            summary = summaryFormset.save(commit=False)
            summary.Faculty_ID = faculty
            summary.save()
            summaryFormset.save_m2m()

            doe = doeFormset.save(commit=False)

            # add user to each table row
            for d in doe:
                d.Faculty_ID = faculty
                d.save()

            doeFormset.save_m2m()
            return HttpResponseRedirect('/executive/')
    else:
        # Show the Executive Summary form
        summaryFormset = ExecutiveSummaryForm(instance=summaryData, prefix='summary')
        doeFormset = modelformset_factory(DoETable,
                form=DoEForm, extra=1, can_delete=True)(queryset=doeData, prefix='doe')

    return direct_to_template(request, 'executive.html', {'summaryFormset': summaryFormset, 'doeFormset': doeFormset})

@login_required
def biographical(request):
    faculty = getFaculty(request.user)
    
    # get this user's degrees or else create a new one
    try:
        accredData = AccredTable.objects.filter(Faculty_ID=faculty).order_by('Date')
    except AccredTable.DoesNotExist:
        accredData = AccredTable(Faculty_ID=faculty)
        
    try:
        honorData = HonorTable.objects.filter(Faculty_ID=faculty)    
    except HonorTable.DoesNotExist:
        honorData = HonorTable(Faculty_ID=faculty)
        
    try:
        positionData = PositionTable.objects.filter(Faculty_ID=faculty)
    except PositionTable.DoesNotExist:
        positionData = PositionTable(FacultyID=faculty)
    
    if request.method == 'POST':
        facultyNameDeptForm = FacultyNameDeptForm(request.POST, request.FILES,
                instance=faculty, prefix='namedept')
    else:
        facultyNameDeptForm = FacultyNameDeptForm(instance=faculty, prefix='namedept')
        
        AccredFormset = modelformset_factory(AccredTable, form=AccredForm)
        accredFormset = AccredFormset(queryset=accredData, prefix='accred')
        
        HonorFormset = modelformset_factory(HonorTable, form=HonorForm)
        honorFormset = HonorFormset(queryset=honorData, prefix='honor')
        
        facultyStartForm = FacultyStartForm(instance=faculty, prefix='facultystart')
        
        PositionFormset = modelformset_factory(PositionTable, form=PositionForm)
        positionFormset = PositionFormset(queryset=positionData, prefix='position')
        
    #modelformset_factory(FacultyTable, fields=('Faculty_GName', 'Faculty_SName', 'Department'))

    return direct_to_template(request, 'biographical.html', {
        'facultyNameDeptForm': facultyNameDeptForm,
        'accredFormset': accredFormset,
        'honorFormset': honorFormset,
        'facultyStartForm': facultyStartForm,
        'positionFormset': positionFormset,
    })

@login_required
def offCampusRecognition(request):
    return direct_to_template(request, 'OffCampusRecognition.html', {})

@login_required
def ServiceAndAdmin(request):
    return direct_to_template(request, 'ServiceAndAdministrativeContributions.html', {})

@login_required
def ReportOnTeaching(request):
    return direct_to_template(request, 'ReportOnTeaching.html', {})

@login_required
def ResearchGrants(request):
    return direct_to_template(request, 'ResearchGrants.html', {})

@login_required
def Courses(request):
    return direct_to_template(request, 'Courses.html', {})

@login_required
def ResearchActivity(request):
    return direct_to_template(request, 'ResearchActivity.html', {})

@login_required
def distribution_of_effort(request):
    """ Create a form view for the Distribution of Effort """

    # get this user's DoE or else create a new one
    try:
        data = DistributionOfEffort.objects.get(user=request.user)
    except:
        data = DistributionOfEffort()

    if request.method == 'POST':
        formset = DistributionOfEffortForm(request.POST, request.FILES, instance=data)
        if formset.is_valid():
            # Save the form data, ensure they are updating as themselves
            doe = formset.save(commit=False)
            doe.user = request.user
            doe.save()
            formset.save_m2m()
    else:
        # Show the DoE form
        formset = DistributionOfEffortForm(instance=data)
    return direct_to_template(request, 'doe.html', {'formset': formset})

# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
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
        fac = FacultyTable(Username=user)
        fac.save()
        return fac

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
        positionHeldData = PositionHeldTable.objects.filter(Faculty_ID=faculty)
    except PositionHeldTable.DoesNotExist:
        positionHeldData = PositionHeldTable(Faculty_ID=faculty)

    try:
        positionPriorData = PositionPriorTable.objects.filter(Faculty_ID=faculty)
    except PositionPriorTable.DoesNotExist:
        positionPriorData = PositionPriorTable(Faculty_ID=faculty)

    try:
        positionElsewhereData = PositionElsewhereTable.objects.filter(Faculty_ID=faculty)
    except PositionElsewhereTable.DoesNotExist:
        positionElsewhereData = PositionElsewhereTable(Faculty_ID=faculty)
    
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
        
        PositionHeldFormset = modelformset_factory(PositionHeldTable, form=PositionHeldForm)
        positionHeldFormset = PositionHeldFormset(queryset=positionHeldData, prefix='positionheld')

        PositionPriorFormset = modelformset_factory(PositionPriorTable, form=PositionPriorForm)
        positionPriorFormset = PositionPriorFormset(queryset=positionPriorData, prefix='positionprior')

        PositionElsewhereFormset = modelformset_factory(PositionElsewhereTable, form=PositionElsewhereForm)
        positionElsewhereFormset = PositionElsewhereFormset(queryset=positionElsewhereData, prefix='positionelsewhere')

    return direct_to_template(request, 'biographical.html', {
        'facultyNameDeptForm': facultyNameDeptForm,
        'accredFormset': accredFormset,
        'honorFormset': honorFormset,
        'facultyStartForm': facultyStartForm,
        'positionHeldFormset': positionHeldFormset,
        'positionPriorFormset': positionPriorFormset,
        'positionElsewhereFormset': positionElsewhereFormset,
    })

@login_required
def offCampusRecognition(request):

    """ Create a form view for the off campus recognition """

    faculty = getFaculty(request.user)


    try:
        offCampusData = SummaryTable.objects.get(Faculty_ID = faculty)
    except SummaryTable.DoesNotExist:
        offCampusData = SummaryTable(Faculty_ID = faculty)


    if request.method == 'POST':
        offCampusFormset =  OffCampusRecognitionForm(request.POST, request.FILES, instance=offCampusData, prefix="OffCampus")


        if offCampusFormset.is_valid():
            offcampus = offCampusFormset.save(commit=False)
            offcampus.user = request.user
            offcampus.save()
            offCampusFormset.save_m2m()

    else:
        offCampusFormset = OffCampusRecognitionForm(instance=offCampusData, prefix="OffCampus")

    return direct_to_template(request, 'OffCampusRecognition.html', {'offCampusForm': offCampusFormset})

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

    """ Create a form view for Research Activity """

    faculty = getFaculty(request.user)


    try:
        ResearchData = SummaryTable.objects.get(Faculty_ID = faculty)
    except SummaryTable.DoesNotExist:
        ResearchData = SummaryTable(Faculty_ID = faculty)


    if request.method == 'POST':
        ResearchFormset =  ResearchActivityForm(request.POST, request.FILES, instance=ResearchData, prefix="Research")


        if ResearchFormset.is_valid():
            Research = ResearchFormset.save(commit=False)
            Research.user = request.user
            Research.save()
            ResearchFormset.save_m2m()

    else:
        ResearchFormset = ResearchActivityForm(instance=ResearchData, prefix="Research")

    return direct_to_template(request, 'ResearchActivity.html', {'ResearchActivityForm': ResearchFormset})

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

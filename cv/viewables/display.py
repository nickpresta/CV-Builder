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
                form=DoEForm, extra=1, can_delete=True, formset=FormsetMixin)(request.POST,
                        request.FILES, queryset=doeData, prefix='doe')

        if summaryFormset.is_valid() and doeFormset.is_valid():
            summaryFormset.save(Faculty_ID=faculty)
            doeFormset.save(Faculty_ID=faculty)

            return HttpResponseRedirect('/executive/')
    else:
        # Show the Executive Summary form
        summaryFormset = ExecutiveSummaryForm(instance=summaryData, prefix='summary')
        doeFormset = modelformset_factory(DoETable,
                form=DoEForm, extra=1, can_delete=True, formset=FormsetMixin)(queryset=doeData, prefix='doe')

    return direct_to_template(request, 'executive.html', {'summaryFormset': summaryFormset, 'doeFormset': doeFormset})

@login_required
def biographical(request):
    faculty = getFaculty(request.user)
    
    formInfo = {
        'facultyNameDeptForm': (
            FacultyNameDeptForm,
            faculty,
            'namedept',
        ),
        'facultyStartForm': (
            FacultyStartForm,
            faculty,
            'facultystart'
        )
    }

    formsetInfo = {
        'accredFormset': (
            modelformset_factory(AccredTable, form=AccredForm, extra=1, formset=FormsetMixin, can_delete=True),
            AccredTable.objects.filter(Faculty_ID=faculty).order_by('Date'),
            'accred'
        ),
        'honorFormset': (
            modelformset_factory(HonorTable, form=HonorForm, extra=1, formset=FormsetMixin, can_delete=True),
            HonorTable.objects.filter(Faculty_ID=faculty),
            'honor'
        ),
        'positionHeldFormset': (
            modelformset_factory(PositionHeldTable, form=PositionHeldForm, extra=1, formset=FormsetMixin, can_delete=True),
            PositionHeldTable.objects.filter(Faculty_ID=faculty),
            'positionheld'
        ),
        'positionPriorFormset': (
            modelformset_factory(PositionPriorTable, form=PositionPriorForm, extra=1, formset=FormsetMixin, can_delete=True),
            PositionPriorTable.objects.filter(Faculty_ID=faculty),
            'positionprior'
        ),
        'positionElsewhereFormset': (
            modelformset_factory(PositionElsewhereTable, form=PositionElsewhereForm, extra=1, formset=FormsetMixin, can_delete=True),
            PositionElsewhereTable.objects.filter(Faculty_ID=faculty),
            'positionelsewhere'
        )
    }
    
    if request.method == 'POST':
        formsets = dict((
            formsetName, 
            Formset(request.POST, request.FILES, queryset=qs, prefix=pf)
        ) for formsetName, (Formset, qs, pf) in formsetInfo.iteritems())
        forms = dict((
            formName,
            Form(request.POST, request.FILES, instance=ins, prefix=pf)
        ) for formName, (Form, ins, pf) in formInfo.iteritems())
        
        context = dict([('forms', forms), ('formsets', formsets)])
        
        print context
        
        allForms = dict(formsets)
        allForms.update(forms)        
        
        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save(Faculty_ID=faculty)
                print formset
                
            return HttpResponseRedirect('/biographical/')
            
    else:
        formsets = dict((
            formsetName,
            Formset(queryset=qs, prefix=pf)
        ) for formsetName, (Formset, qs, pf) in formsetInfo.iteritems())
        forms = dict((
            formName,
            Form(instance=ins, prefix=pf)
        ) for formName, (Form, ins, pf) in formInfo.iteritems())
        
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'biographical.html', context)

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

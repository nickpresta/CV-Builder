# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.forms import ModelChoiceField
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.core import serializers

from cv.forms import *
from cv.models import *

# These are utility functions that we need through all views
from common import *

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
                form=DoEForm, extra=0, can_delete=True, formset=FormsetMixin)(
                    request.POST, request.FILES, queryset=doeData, 
                    prefix='doe', pk=faculty)

        if summaryFormset.is_valid() and doeFormset.is_valid():
            summaryFormset.save()
            doeFormset.save()

            return HttpResponseRedirect('/executive/')
    else:
        # Show the Executive Summary form
        summaryFormset = ExecutiveSummaryForm(instance=summaryData, prefix='summary')
        doeFormset = modelformset_factory(DoETable,
                form=DoEForm, extra=0, can_delete=True, formset=FormsetMixin)(queryset=doeData, prefix='doe')

    return direct_to_template(request, 'executive.html', {'summaryFormset': summaryFormset, 'doeFormset': doeFormset})

@login_required
def biographical(request):
    faculty = getFaculty(request.user)
    
    formInfo = {
        'facultyNameDeptForm': (
            FacultyNameDeptForm,
            faculty,
            'namedept',
            None
        ),
        'facultyStartForm': (
            FacultyStartForm,
            faculty,
            'facultystart',
            None
        )
    }

    formsetInfo = {
        'accredFormset': (
            modelformset_factory(AccredTable, form=AccredForm, extra=0, formset=FormsetMixin, can_delete=True),
            AccredTable.objects.filter(Faculty_ID=faculty).order_by('Date'),
            'accred',
            faculty
        ),
        'honorFormset': (
            modelformset_factory(HonorTable, form=HonorForm, extra=0, formset=FormsetMixin, can_delete=True),
            HonorTable.objects.filter(Faculty_ID=faculty),
            'honor',
            faculty
        ),
        'positionHeldFormset': (
            modelformset_factory(PositionHeldTable, form=PositionHeldForm, extra=0, formset=FormsetMixin, can_delete=True),
            PositionHeldTable.objects.filter(Faculty_ID=faculty),
            'positionheld',
            faculty
        ),
        'positionPriorFormset': (
            modelformset_factory(PositionPriorTable, form=PositionPriorForm, extra=0, formset=FormsetMixin, can_delete=True),
            PositionPriorTable.objects.filter(Faculty_ID=faculty),
            'positionprior',
            faculty
        ),
        'positionElsewhereFormset': (
            modelformset_factory(PositionElsewhereTable, form=PositionElsewhereForm, extra=0, formset=FormsetMixin, can_delete=True),
            PositionElsewhereTable.objects.filter(Faculty_ID=faculty),
            'positionelsewhere',
            faculty
        )
    }
    
    if request.method == 'POST':
        formsets, forms = createContext(formsetInfo, formInfo, postData=request.POST, files=request.FILES)
        context = dict([('forms', forms), ('formsets', formsets)])

        allForms = dict(formsets)
        allForms.update(forms)        
        
        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save()
                
            return HttpResponseRedirect('/biographical/')
            
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
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
def reportOnTeaching(request):
    faculty = getFaculty(request.user)
    
    formsetInfo = { }
    formInfo = {
        'reportOnTeaching': (
            ReportOnTeachingForm,
            SummaryTable.objects.get(Faculty_ID=faculty),
            'report',
            faculty
        )
    }
    
    if request.method == 'POST':
        formsets, forms = createContext(formsetInfo, formInfo, postData=request.POST, files=request.FILES)
        
        context = dict([('forms', forms), ('formsets', formsets)])

        allForms = dict(formsets)
        allForms.update(forms)        
        
        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save()
                
            return HttpResponseRedirect('/ReportOnTeaching/')
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])
    
    return direct_to_template(request, 'ReportOnTeaching.html', context)
    
@login_required
def researchConsulting(request):
    faculty = getFaculty(request.user)
    
    formsetInfo = { }
    formInfo = {
        'consulting': (
            ConsultingResearchForm,
            SummaryTable.objects.get(Faculty_ID=faculty),
            'consulting',
            faculty
        )
    }
    
    if request.method == 'POST':
        formsets, forms = createContext(formsetInfo, formInfo, postData=request.POST, files=request.FILES)
        
        context = dict([('forms', forms), ('formsets', formsets)])

        allForms = dict(formsets)
        allForms.update(forms)        
        
        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save()
                
            return HttpResponseRedirect('/research/consulting/')
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])
    
    return direct_to_template(request, 'researchconsulting.html', context)

@login_required
def researchPatents(request):
    faculty = getFaculty(request.user)
    
    formsetInfo = { }
    formInfo = {
        'patents': (
            PatentsResearchForm,
            SummaryTable.objects.get(Faculty_ID=faculty),
            'consulting',
            faculty
        )
    }
    
    if request.method == 'POST':
        formsets, forms = createContext(formsetInfo, formInfo, postData=request.POST, files=request.FILES)
        
        context = dict([('forms', forms), ('formsets', formsets)])

        allForms = dict(formsets)
        allForms.update(forms)        
        
        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save()
                
            return HttpResponseRedirect('/research/patents/')
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])
    
    return direct_to_template(request, 'researchpatents.html', context)

@login_required
def researchOther(request):
    faculty = getFaculty(request.user)
    
    formsetInfo = { }
    formInfo = {
        'other': (
            OtherResearchForm,
            SummaryTable.objects.get(Faculty_ID=faculty),
            'other',
            faculty
        )
    }
    
    if request.method == 'POST':
        formsets, forms = createContext(formsetInfo, formInfo, postData=request.POST, files=request.FILES)
        
        context = dict([('forms', forms), ('formsets', formsets)])

        allForms = dict(formsets)
        allForms.update(forms)        
        
        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save()
                
            return HttpResponseRedirect('/research/other/')
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])
    
    return direct_to_template(request, 'researchother.html', context)

@login_required
def researchRecognition(request):
    faculty = getFaculty(request.user)
    
    formsetInfo = { }
    formInfo = {
        'recognition': (
            RecognitionResearchForm,
            SummaryTable.objects.get(Faculty_ID=faculty),
            'recognition',
            faculty
        )
    }
    
    if request.method == 'POST':
        formsets, forms = createContext(formsetInfo, formInfo, postData=request.POST, files=request.FILES)
        
        context = dict([('forms', forms), ('formsets', formsets)])

        allForms = dict(formsets)
        allForms.update(forms)        
        
        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save()
                
            return HttpResponseRedirect('/research/recognition/')
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])
    
    return direct_to_template(request, 'researchrecognition.html', context)

@login_required
def researchGrants(request):
    faculty = getFaculty(request.user)
    formInfo = {

    }    
    formsetInfo = {
        'grants': (
            modelformset_factory(GrantTable, form=GrantForm, extra=0, formset=GrantFormset, can_delete=True),
            GrantTable.objects.filter(Faculty_ID=faculty),
            'grant',
            faculty
        )
    }
    
    if request.method == 'POST':
        formsets, forms = createContext(formsetInfo, formInfo, postData=request.POST, files=request.FILES)
        context = dict([('forms', forms), ('formsets', formsets)])

        allForms = dict(formsets)
        allForms.update(forms)        
        
        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save_all()
                
            return HttpResponseRedirect('/research/grants/')
            
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    forms['grants'] = GrantSelectForm()
    forms['grants'].fields['grantSelect'] = ModelChoiceField(queryset=GrantTable.objects.filter(Faculty_ID=faculty), label="Grant")

    return direct_to_template(request, 'researchgrants.html', context)

@login_required
def courses(request):
    faculty = getFaculty(request.user)
    formInfo = {
        'coursesJoined': (
            inlineformset_factory(FacultyTable, FacultyCourseJoinTable, form=CourseJoinForm, extra=0, formset=InlineFormsetMixin, can_delete=True),
            faculty,
            'cjoin',
            faculty
        )
    }    
    formsetInfo = {
        'courses': (
            modelformset_factory(CourseTable, form=CourseForm, extra=0, formset=FormsetMixin, can_delete=True),
            CourseTable.objects.all(),
            'courses',
            None
        )
    }
    
    if request.method == 'POST':
        formsets, forms = createContext(formsetInfo, formInfo, postData=request.POST, files=request.FILES)
        context = dict([('forms', forms), ('formsets', formsets)])

        allForms = dict(formsets)
        allForms.update(forms)        
        
        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save()
                
            return HttpResponseRedirect('/courses/')
            
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'courses.html', context)
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

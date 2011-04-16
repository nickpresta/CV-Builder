# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.forms import ModelChoiceField
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.core import serializers
from django.core.urlresolvers import reverse

from cv.forms import *
from cv.models import *

# These are utility functions that we need through all views
from common import *

SECTION_LABELS = {
    'teaching': (
        'Teaching and Learning', {
            'summary': 'Report on Teaching',
            'counselling': 'Contributions to Student Counselling',
            'course_development': 'Major Work in Graduate and Undergraduate Course Development',
            'recognition': 'Recognition of Teaching Ability and Achievement',
            'support': 'Support Received for Major Teaching and Projects',
            'scholarship': 'Scholarship in Education',
            'other': 'Other Contributions to Education',
            'courses': 'Courses Taught',
            'graduate': 'Graduate Advising and Examining'
        }
    ),
    'research': (
        'Research', {
            'summary': 'Summary of Research Activity',
            'professional_consulting': 'Professional Consulting',
            'patents': 'Patents',
            'other': 'Other Activities',
            'recognition': 'Recognition of Research and Scholarship',
            'grants': 'Research Grants and Contracts'
        }
    ),
    'off_campus': (
        'Off-Campus Recognition', {
        }
    ),
    'executive': (
        'Executive Summary', {
            'doe': 'Distribution of Effort'
        }
    ),
    'service': (
        'Service and Administrative Contributions', {
        
        }
    )
}

def index(request):
    """ Responsible for showing the index page """

    return direct_to_template(request, 'index.html', {'status': 'works!'})

@login_required
def editcv(request):
    return direct_to_template(request, 'editcv.html', {})

@login_required
def distribution_of_effort(request):
    """ Create a form view for the Distribution of Effort """

    doeData = DistributionOfEffort.objects.filter(user=request.user).order_by('year')

    if request.method == 'POST':
        doeFormset = modelformset_factory(DistributionOfEffort,
                form=DoEForm, extra=0, can_delete=True, formset=FormsetMixin)(
                    request.POST, request.FILES, queryset=doeData,
                    prefix='doe', pk=request.user.id, label='Distribution of Effort')

        if doeFormset.is_valid():
            doeFormset.save()

            return HttpResponseRedirect(reverse('cv-distribution-of-effort'))
    else:
        doeFormset = modelformset_factory(DistributionOfEffort,
                form=DoEForm, extra=0, can_delete=True, formset=FormsetMixin)(
                        queryset=doeData, prefix='doe',  label='Distribution of Effort')

    return direct_to_template(request, 'distribution_of_effort.html',
            {'doeFormset': doeFormset})

@login_required
def biographical(request):
    formInfo = {
        'facultyNameDeptForm': (
            FacultyNameDeptForm,
            request.user,
            'namedept',
            None
        ),
        'facultyStartForm': (
            FacultyStartForm,
            request.user.get_profile(),
            'facultystart',
            None
        ),
        'facultyDepartmentsForm': (
            FacultyDepartmentsForm,
            request.user.get_profile(),
            'facultydepartments',
            None
        )
    }

    formsetInfo = {
        'accredFormset': (
            modelformset_factory(Accred, form=AccredForm, extra=0,
                formset=FormsetMixin, can_delete=True),
            {
                'queryset': Accred.objects.filter(user=request.user).order_by('date'),
                'prefix': 'accred',
                'pk': request.user.id,
                'label': 'Degrees'
            }
        ),
        'honorFormset': (
            modelformset_factory(Honor, form=HonorForm, extra=0,
                formset=FormsetMixin, can_delete=True),
            {
                'queryset': Honor.objects.filter(user=request.user),
                'prefix': 'honor',
                'pk': request.user.id,
                'label': 'Major Honours & Fellowships'
            }
        ),
        'positionHeldFormset': (
            modelformset_factory(PositionHeld, form=PositionHeldForm, extra=0, formset=FormsetMixin, can_delete=True),
            {
                'queryset': PositionHeld.objects.filter(user=request.user),
                'prefix': 'positionheld',
                'pk': request.user.id,
                'label': 'Positions Held at University of Guelph'
            }
        ),
        'positionPriorFormset': (
            modelformset_factory(PositionPrior, form=PositionPriorForm, extra=0, formset=FormsetMixin, can_delete=True),
            {
                'queryset': PositionPrior.objects.filter(user=request.user),
                'prefix': 'positionprior',
                'pk': request.user.id,
                'label': 'Experience Prior to Appointment at Guelph'
            }
        ),
        'positionElsewhereFormset': (
            modelformset_factory(PositionElsewhere, form=PositionElsewhereForm,
                extra=0, formset=FormsetMixin, can_delete=True),
            {
                'queryset': PositionElsewhere.objects.filter(user=request.user),
                'prefix': 'positionelsewhere',
                'pk': request.user.id,
                'label': 'Visiting Professorships'
            }
        )
    }

    if request.method == 'POST':
        formsets, forms = createContext(formsetInfo, formInfo, postData=request.POST,
                files=request.FILES)
        context = dict([('forms', forms), ('formsets', formsets)])

        allForms = dict(formsets)
        allForms.update(forms)

        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save()

            return HttpResponseRedirect(reverse('cv-biographical'))
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'biographical.html', context)

@login_required
def off_campus_recognition(request):
    """ Create a form view for the off campus recognition """

    try:
        offCampusData = Summary.objects.get(user=request.user)
    except Summary.DoesNotExist:
        offCampusData = Summary(user=request.user)


    if request.method == 'POST':
        offCampusFormset =  OffCampusRecognitionForm(request.POST, request.FILES,
                instance=offCampusData, prefix="OffCampus")

        if offCampusFormset.is_valid():
            offcampus = offCampusFormset.save(commit=False)
            offcampus.user = request.user
            offcampus.save()
            offCampusFormset.save_m2m()

    else:
        offCampusFormset = OffCampusRecognitionForm(instance=offCampusData, prefix="OffCampus")

    return direct_to_template(request, 'off_campus_recognition.html',
            {'offCampusForm': offCampusFormset})

@login_required
def research_grants(request):
    formInfo = {}
    formsetInfo = {
        'grants': (
            modelformset_factory(Grant, form=GrantForm, extra=0,
                formset=GrantFormset, can_delete=True),
            {
                'queryset': Grant.objects.filter(user=request.user),
                'prefix': 'grants',
                'pk': request.user.id,
                'label': 'Research Grants and Contracts'
            }
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

            return HttpResponseRedirect(reverse('cv-research-grants'))

    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'research_grants.html', context)

@login_required
def teaching_courses(request):
    formInfo = {
    }
    formsetInfo = {
        'coursesJoined': (
            inlineformset_factory(User, FacultyCourseJoin,
                form=CourseJoinForm, extra=0, formset=InlineFormsetMixin, can_delete=True),
            {
                'instance': request.user,
                'prefix': 'cjoin',
                'pk': request.user.id,
                'label': 'Courses Taught'
            }
        )
    }

    if request.method == 'POST':
        formsets, forms = createContext(formsetInfo, formInfo,
                postData=request.POST, files=request.FILES)
        context = dict([('forms', forms), ('formsets', formsets)])

        allForms = dict(formsets)
        allForms.update(forms)

        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save()

            return HttpResponseRedirect(reverse('cv-teaching-courses'))

    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'courses.html', context)

@login_required
def freeformat(request, subsection='', section=''):
    context = {
        'action': request.path
    }

    field = ''

    # determine which Summary field to edit as section[_subsection]
    if section:
        field = section
        if section in SECTION_LABELS:
            context['section'] = SECTION_LABELS[section][0]

        if subsection:
            field += '_' + subsection
            if section in SECTION_LABELS and subsection in SECTION_LABELS[section][1]:
                context['subsection'] = SECTION_LABELS[section][1][subsection]
        elif section in SECTION_LABELS and 'summary' in SECTION_LABELS[section][1]:
            context['subsection'] = SECTION_LABELS[section][1]['summary']    

    try:
        summary = Summary.objects.get(user=request.user)
    except Summary.DoesNotExist:
        summary = Summary(user=request.user)

    if request.method == 'POST':
        form = FreeFormatForm(request.POST, request.FILES,
                pk=request.user.id, instance=summary, field=field)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(request.path)
    else:
        form = FreeFormatForm(pk=request.user.id, instance=summary, field=field)

    context['form'] = form
    return direct_to_template(request, 'freeformat.html', context)

@login_required
def service(request):
    formInfo = {}
    formsetInfo = {
        'service': (
            modelformset_factory(Service, form=ServiceForm,
                extra=0, formset=FormsetMixin, can_delete=True),
            {
                'queryset': Service.objects.filter(user=request.user),
                'prefix': 'service',
                'pk': request.user.id,
                'label': 'Committees and Similar Bodies'
            }
        )
    }

    if request.method == 'POST':
        formsets, forms = createContext(formsetInfo, formInfo,
                postData=request.POST, files=request.FILES)          
        context = dict([('forms', forms), ('formsets', formsets)])

        allForms = dict(formsets)
        allForms.update(forms)

        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save()

            return HttpResponseRedirect(reverse('cv-service'))

    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'service.html', context)

@login_required
def teaching_graduate(request):
    formInfo = {
    }
    formsetInfo = {
        'advisor': (
            modelformset_factory(GradAdvisor, form=AdvisorForm, extra=0,
                formset=FormsetMixin, can_delete=True),
            {
                'queryset': GradAdvisor.objects.filter(user=request.user),
                'prefix': 'gradad',
                'pk': request.user.id,
                'label': 'Advisor'
            }
        ),
        'committee': (
            modelformset_factory(GradAdvisorCommitteeMember, form=AdvisorCommitteeForm, extra=0,
                formset=FormsetMixin, can_delete=True),
            {
                'queryset': GradAdvisorCommitteeMember.objects.filter(user=request.user),
                'prefix': 'gradmem',
                'pk': request.user.id,
                'label': 'Advising Committee Member'
            }
        ),
        'examiner': (
            modelformset_factory(GradExaminer, form=ExaminerForm, extra=0,
                formset=FormsetMixin, can_delete=True),
            {
                'queryset': GradExaminer.objects.filter(user=request.user),
                'prefix': 'gradexam',
                'pk': request.user.id,
                'label': 'Examining Committee Member'
            }
        )
    }

    if request.method == 'POST':
        formsets, forms = createContext(formsetInfo, formInfo,
                postData=request.POST, files=request.FILES)
        context = dict([('forms', forms), ('formsets', formsets)])

        allForms = dict(formsets)
        allForms.update(forms)

        if reduce(lambda f1, f2: f1 and f2.is_valid(), allForms.values(), True):
            # Save the form data, ensure they are updating as themselves
            for form in forms.values():
                form.save()
            for formset in formsets.values():
                formset.save()

            return HttpResponseRedirect(reverse('cv-teaching-graduate'))

    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'teaching_graduate.html', context)

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
            'other': 'Other Contributions to Education'
        }
    ),
    'research': (
        'Research', {
            'summary': 'Summary of Research Activity',
            'professional_consulting': 'Professional Consulting',
            'patents': 'Patents',
            'other': 'Other Activities',
            'recognition': 'Recognition of Research and Scholarship'
        }
    ),
    'off_campus': (
        'Off-Campus Recognition', {
        }
    ),
    'executive': (
        'Executive Summary', {
        }
    ),
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
                    prefix='doe', pk=request.user.id)

        if doeFormset.is_valid():
            doeFormset.save()

            return HttpResponseRedirect(reverse('cv-distribution-of-effort'))
    else:
        doeFormset = modelformset_factory(DistributionOfEffort,
                form=DoEForm, extra=0, can_delete=True, formset=FormsetMixin)(
                        queryset=doeData, prefix='doe')

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
            Accred.objects.filter(user=request.user).order_by('date'),
            'accred',
            request.user.id
        ),
        'honorFormset': (
            modelformset_factory(Honor, form=HonorForm, extra=0,
                formset=FormsetMixin, can_delete=True),
            Honor.objects.filter(user=request.user),
            'honor',
            request.user.id
        ),
        'positionHeldFormset': (
            modelformset_factory(PositionHeld, form=PositionHeldForm, extra=0, formset=FormsetMixin, can_delete=True),
            PositionHeld.objects.filter(user=request.user),
            'positionheld',
            request.user.id
        ),
        'positionPriorFormset': (
            modelformset_factory(PositionPrior, form=PositionPriorForm, extra=0, formset=FormsetMixin, can_delete=True),
            PositionPrior.objects.filter(user=request.user),
            'positionprior',
            request.user.id
        ),
        'positionElsewhereFormset': (
            modelformset_factory(PositionElsewhere, form=PositionElsewhereForm,
                extra=0, formset=FormsetMixin, can_delete=True),
            PositionElsewhere.objects.filter(user=request.user),
            'positionelsewhere',
            request.user.id
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
            Grant.objects.filter(user=request.user),
            'grants',
            request.user.id
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

    forms['grants'] = GrantSelectForm()
    forms['grants'].fields['grantSelect'] = ModelChoiceField(queryset=Grant.objects.filter(
        user=request.user), label="Grant")

    return direct_to_template(request, 'research_grants.html', context)

@login_required
def teaching_courses(request):
    formInfo = {
        'coursesJoined': (
            inlineformset_factory(User, FacultyCourseJoin,
                form=CourseJoinForm, extra=0, formset=InlineFormsetMixin, can_delete=True),
            request.user,
            'cjoin',
            request.user.id
        )
    }
    formsetInfo = {

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
            Service.objects.filter(user=request.user),
            'service',
            request.user.id
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

    forms['service'] = ServiceSelectForm()
    forms['service'].fields['serviceSelect'] = ModelChoiceField(
        queryset=Service.objects.filter(user=request.user), label="Service")


    return direct_to_template(request, 'service.html', context)

@login_required
def teaching_graduate(request):
    formInfo = {
    }
    formsetInfo = {
        'advisor': (
            modelformset_factory(GradAdvisor, form=AdvisorForm, extra=0,
                formset=FormsetMixin, can_delete=True),
            GradAdvisor.objects.filter(user=request.user),
            'gradad',
            request.user.id
        ),
        'committee': (
            modelformset_factory(GradAdvisorCommitteeMember, form=AdvisorCommitteeForm, extra=0,
                formset=FormsetMixin, can_delete=True),
            GradAdvisorCommitteeMember.objects.filter(user=request.user),
            'gradmem',
            request.user.id
        ),
        'examiner': (
            modelformset_factory(GradExaminer, form=ExaminerForm, extra=0,
                formset=FormsetMixin, can_delete=True),
            GradExaminer.objects.filter(user=request.user),
            'gradexam',
            request.user.id
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

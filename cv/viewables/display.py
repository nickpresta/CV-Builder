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

def index(request):
    """ Responsible for showing the index page """

    return direct_to_template(request, 'index.html', {'status': 'works!'})

@login_required
def editcv(request):
    return direct_to_template(request, 'editcv.html', {})

@login_required
def executive(request):
    """ Create a form view for the Distribution of Effort """

    # get this user's Summary or else create a new one
    try:
        summaryData = Summary.objects.get(user=request.user)
    except Summary.DoesNotExist:
        summaryData = Summary(user=request.user)

    # get this user's DoEs or else create a new one
    try:
        doeData = DistributionOfEffort.objects.filter(user=request.user).order_by('year')
    except DistributionOfEffort.DoesNotExist:
        doeData = DistributionOfEffort(user=request.user)

    if request.method == 'POST':
        summaryFormset = ExecutiveSummaryForm(request.POST, request.FILES,
                instance=summaryData, prefix='summary')
        doeFormset = modelformset_factory(DistributionOfEffort,
                form=DoEForm, extra=0, can_delete=True, formset=FormsetMixin)(
                    request.POST, request.FILES, queryset=doeData,
                    prefix='doe', pk=request.user.id)

        if summaryFormset.is_valid() and doeFormset.is_valid():
            summaryFormset.save()
            doeFormset.save()

            return HttpResponseRedirect(reverse('cv-executive'))
    else:
        summaryFormset = ExecutiveSummaryForm(instance=summaryData, prefix='summary')
        doeFormset = modelformset_factory(DistributionOfEffort,
                form=DoEForm, extra=0, can_delete=True, formset=FormsetMixin)(
                        queryset=doeData, prefix='doe')

    return direct_to_template(request, 'executive.html',
            {'summaryFormset': summaryFormset, 'doeFormset': doeFormset})

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
def service_and_admin(request):
    return direct_to_template(request, 'service_and_administrative_contributions.html', {})

@login_required
def report_on_teaching(request):
    try:
        summary = Summary.objects.get(user=request.user)
    except Summary.DoesNotExist:
        summary = Summary(user=request.user)

    formsetInfo = { }
    formInfo = {
        'reportOnTeaching': (
            ReportOnTeachingForm,
            summary,
            'report',
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
                formset.save()

            return HttpResponseRedirect(reverse('cv-report-on-teaching'))
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'report_on_teaching.html', context)

@login_required
def research_consulting(request):
    try:
        summary = Summary.objects.get(user=request.user)
    except Summary.DoesNotExist:
        summary = Summary(user=request.user)

    formsetInfo = {}
    formInfo = {
        'consulting': (
            ConsultingResearchForm,
            summary,
            'consulting',
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

            return HttpResponseRedirect(reverse('cv-research-consulting'))
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'research_consulting.html', context)

@login_required
def counselling(request):
    try:
        summary = Summary.objects.get(user=request.user)
    except Summary.DoesNotExist:
        summary = Summary(user=request.user)

    formsetInfo = { }
    formInfo = {
        'counselling': (
            CounsellingForm,
            summary,
            'counselling',
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
                formset.save()

            return HttpResponseRedirect(reverse('cv-teaching-counselling'))
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'counselling.html', context)

@login_required
def research_patents(request):
    try:
        summary = Summary.objects.get(user=request.user)
    except Summary.DoesNotExist:
        summary = Summary(user=request.user)

    formsetInfo = { }
    formInfo = {
        'patents': (
            PatentsResearchForm,
            summary,
            'consulting',
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
                formset.save()

            return HttpResponseRedirect(reverse('cv-research-patents'))
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'research_patents.html', context)

@login_required
def research_other(request):
    try:
        summary = Summary.objects.get(user=request.user)
    except Summary.DoesNotExist:
        summary = Summary(user=request.user)

    formsetInfo = { }
    formInfo = {
        'other': (
            OtherResearchForm,
            summary,
            'other',
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
                formset.save()

            return HttpResponseRedirect(reverse('cv-research-other'))
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'research_other.html', context)

@login_required
def research_recognition(request):
    try:
        summary = Summary.objects.get(user=request.user)
    except Summary.DoesNotExist:
        summary = Summary(user=request.user)

    formsetInfo = { }
    formInfo = {
        'recognition': (
            RecognitionResearchForm,
            summary,
            'recognition',
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
                formset.save()

            return HttpResponseRedirect(reverse('cv-research-recognition'))
    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'research_recognition.html', context)

@login_required
def research_grants(request):
    formInfo = {}
    formsetInfo = {
        'grants': (
            modelformset_factory(Grant, form=GrantForm, extra=0, formset=GrantFormset, can_delete=True),
            Grant.objects.filter(user=request.user),
            'grant',
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
def courses(request):
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
        'courses': (
            modelformset_factory(Course, form=CourseForm, extra=0,
                formset=FormsetMixin, can_delete=True),
            Course.objects.all(),
            'courses',
            None
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
def service(request):
    formInfo = {}
    formsetInfo = {
        'department': (
            modelformset_factory(Service, form=ServiceForm,
                extra=0, formset=FormsetMixin, can_delete=True),
            Service.objects.filter(user=request.user).filter(level='d'),
            'dept',
            request.user.id
        ),
        'college': (
            modelformset_factory(Service, form=ServiceForm,
                extra=0, formset=FormsetMixin, can_delete=True),
            Service.objects.filter(user=request.user).filter(level='c'),
            'college',
            request.user.id
        ),
        'university': (
            modelformset_factory(Service, form=ServiceForm,
                extra=0, formset=FormsetMixin, can_delete=True),
            Service.objects.filter(user=request.user).filter(level='u'),
            'uni',
            request.user.id
        ),
        'external': (
            modelformset_factory(Service, form=ServiceForm,
                extra=0, formset=FormsetMixin, can_delete=True),
            Service.objects.filter(user=request.user).filter(level='e'),
            'ext',
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

            return HttpResponseRedirect(reverse('cv-service-contributions'))

    else:
        formsets, forms = createContext(formsetInfo, formInfo)
        context = dict([('forms', forms), ('formsets', formsets)])

    return direct_to_template(request, 'service.html', context)

@login_required
def research_activity(request):
    """ Create a form view for Research Activity """

    try:
        ResearchData = Summary.objects.get(user=request.user)
    except Summary.DoesNotExist:
        ResearchData = Summary(user=request.user)


    if request.method == 'POST':
        ResearchFormset =  ResearchActivityForm(request.POST, request.FILES,
                instance=ResearchData, prefix="Research")


        if ResearchFormset.is_valid():
            Research = ResearchFormset.save(commit=False)
            Research.user = request.user
            Research.save()
            ResearchFormset.save_m2m()

    else:
        ResearchFormset = ResearchActivityForm(instance=ResearchData, prefix="Research")

    return direct_to_template(request, 'research_activity.html',
            {'ResearchActivityForm': ResearchFormset})

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

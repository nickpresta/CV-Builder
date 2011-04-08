# -*- coding: utf-8 -*-
import datetime
import re

from django import forms
from django.forms import ModelForm, Form
from django.forms.models import BaseModelFormSet
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from django.forms.formsets import DELETION_FIELD_NAME

from cv.models import *

class FormMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(FormMixin, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        form = super(FormMixin, self).save(commit=False)

        if self.pk:
            form.setPK(self.pk)

        if commit:
            form.save()

        return form

class FormsetMixin(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(FormsetMixin, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        forms = super(FormsetMixin, self).save(commit=False)
        for form in forms:

            if self.pk:
                form.setPK(self.pk)
            if commit:
                form.save()
        return forms

class InlineFormsetMixin(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(InlineFormsetMixin, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        forms = super(InlineFormsetMixin, self).save(commit=False)
        for form in forms:

            if self.pk:
                form.setPK(self.pk)
            if commit:
                form.save()
        return forms

class DoEForm(FormMixin):
    """ This form is based on the DoE model and shows the
        year, research, teaching, and service """

    year = forms.DateField(initial=datetime.date.today,
            widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        fields = ('year', 'research', 'teaching', 'service')
        model = DistributionOfEffort

    def setPK(self, form):
        form.user_id = self.pk

    def clean(self):
        """ Clean the form according to our custom rules """
        cleaned_data = self.cleaned_data
        research = cleaned_data.get("research")
        teaching = cleaned_data.get("teaching")
        service = cleaned_data.get("service")

        # ensure that all 3 fields add up to 100
        if (research + teaching + service) != 100:
            msg = "Research, teaching and service must add up to 100"
            self._errors['research'] = self.error_class([msg])
            self._errors['teaching'] = self.error_class([msg])
            self._errors['service'] = self.error_class([msg])

            # These fields are no longer valid
            del cleaned_data['research']
            del cleaned_data['teaching']
            del cleaned_data['service']

        return cleaned_data

class FacultyNameDeptForm(FormMixin):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        fields = ('first_name', 'last_name')
        model = User

class AccredForm(FormMixin):
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = Accred
        fields = ('degree', 'discipline', 'institution', 'date')
        widgets = {
            'degree': forms.Textarea(attrs={'class': 'mceNoEditor'}),
            'discipline': forms.Textarea(attrs={'class': 'mceNoEditor'}),
            'institution': forms.Textarea(attrs={'class': 'mceNoEditor'}),
        }

class HonorForm(FormMixin):
    description = forms.CharField(label='Description',
            widget=forms.Textarea(attrs={'class': 'mceNoEditor'}))

    class Meta:
        model = Honor
        fields = ('description',)

class FacultyStartForm(FormMixin):
    faculty_start = forms.DateField(label="Faculty Start Date", initial=datetime.date.today,
            widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        fields = ('faculty_start',)
        model = UserProfile

class FacultyDepartmentsForm(FormMixin):
    class Meta:
        fields = ('departments',)
        model = UserProfile

class ExecutiveSummaryForm(FormMixin):
    class Meta:
        fields = ('executive',)
        model = Summary
        widgets = {
            'executive': forms.Textarea(attrs={'rows': '50', 'cols': '40',})
        }

class PositionHeldForm(FormMixin):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        fields = ('start_date', 'end_date', 'location', 'rank')
        model = PositionHeld

class PositionPriorForm(FormMixin):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        fields = ('start_date', 'end_date', 'location', 'position')
        model = PositionPrior

class PositionElsewhereForm(FormMixin):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        fields = ('start_date', 'end_date', 'location', 'position')
        model = PositionElsewhere

class OffCampusRecognitionForm(FormMixin):
    class Meta:
        fields = ('off_campus',)
        model = Summary

class ResearchActivityForm(FormMixin):
    class Meta:
        model = Summary
        fields = ('research',)
        widgets = {
            'research': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class ReportOnTeachingForm(FormMixin):
    class Meta:
        model = Summary
        fields = ('teaching',)
        widgets = {
            'teaching': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class ConsultingResearchForm(FormMixin):
    class Meta:
        model = Summary
        fields = ('research_professional_consulting',)
        widgets = {
            'research_professional_consulting': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class PatentsResearchForm(FormMixin):
    class Meta:
        model = Summary
        fields = ('research_patents',)
        widgets = {
            'research_patents': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class OtherResearchForm(FormMixin):
    class Meta:
        model = Summary
        fields = ('research_other_activities',)
        widgets = {
            'research_other_activities': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class RecognitionResearchForm(FormMixin):
    class Meta:
        model = Summary
        fields = ('research_recognition',)
        widgets = {
            'research_recognition': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class CounsellingForm(FormMixin):
    class Meta:
        model = Summary
        fields = ('teaching_counselling',)
        widgets = {
            'teaching_counselling': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class CourseJoinForm(FormMixin):
    class Meta:
        model = FacultyCourseJoin
        fields = ('course', 'year', 'semester', 'num_students')

class CourseForm(FormMixin):
    class Meta:
        model = Course
        fields = ('code', 'name', 'info')

class ServiceForm(FormMixin):
    class Meta:
        model = Service
        fields = ('level', 'start_semester', 'start_year', 'end_semester',
                'end_year', 'committee', 'role', 'chair', 'other')

class ServiceSelectForm(Form):
    pass

class GrantForm(FormMixin):
    class Meta:
        model = Grant
        fields = ('held', 'agency', 'support_type', 'project_title')

class InvestigatorForm(FormMixin):
    class Meta:
        model = Investigator
        fields = ('name', 'amount', 'role')

class AdvisorForm(FormMixin):
    class Meta:
        model = GradAdvisor
        fields = ('student_name', 'degree', 'start_date', 'end_date')

class AdvisorCommitteeForm(FormMixin):
    class Meta:
        model = GradAdvisor
        fields = ('student_name', 'degree', 'start_date', 'end_date')

class ExaminerForm(FormMixin):
    class Meta:
        model = GradAdvisor
        fields = ('student_name', 'degree', 'date')

class TeachingCourseDevelopmentForm(FormMixin):
    class Meta:
        model = Summary
        fields = ('teaching_course_development',)
        widgets = {
            'teaching_course_development': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class TeachingRecognitionForm(FormMixin):
    class Meta:
        model = Summary
        fields = ('teaching_recognition',)
        widgets = {
            'teaching_recognition': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }
        
class FreeFormatForm(FormMixin):
    def __init__(self, *args, **kwargs):
        field = kwargs.pop('field', None)
        super(FreeFormatForm, self).__init__(*args, **kwargs)

        self.fields = {
            field: forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '50', 'cols': '40'}))
        }
            
    class Meta:
        model = Summary

class GrantYearForm(FormMixin):
    start_year = forms.DateField(initial=datetime.date.today,
            widget=forms.TextInput(attrs={'class': 'datepicker'}))
    end_year = forms.DateField(initial=datetime.date.today,
            widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = GrantYear
        fields = ('title', 'amount', 'start_year', 'end_year')

class GrantSelectForm(Form):
    pass

InvestigatorFormset = inlineformset_factory(Grant, Investigator,
        form=InvestigatorForm, formset=InlineFormsetMixin, extra=0)
GrantYearFormset = inlineformset_factory(Grant, GrantYear,
        form=GrantYearForm, formset=InlineFormsetMixin, extra=0)

class GrantFormset(FormsetMixin):
    def _get_empty_form(self):
        return super(GrantFormset, self)._get_empty_form()

    def add_fields(self, form, index):
        super(GrantFormset, self).add_fields(form, index)

        try:
            instance = self.get_queryset()[index]
            prefix = re.sub(r'-(?!.*-)', '_', form.prefix)
        except IndexError:
            instance = None
            prefix = re.sub(r'-(?!.*-)', '_', form.prefix)
        except TypeError:
            instance = None
            prefix = re.sub(r'-__prefix__', '___nested_prefix__', form.prefix)

        form.nested = [
            InvestigatorFormset(data=self.data, instance=instance,
                prefix='%s_invest' % prefix, pk=instance),
            GrantYearFormset(data=self.data, instance=instance,
                prefix='%s_gyear' % prefix, pk=instance)
        ]

    def is_valid(self):
        result = super(GrantFormset, self).is_valid()

        for form in self.forms:
            if hasattr(form, 'nested'):
                for nestedForm in form.nested:
                    result = result and nestedForm.is_valid()
        return result

    def save_new(self, form, commit=True):
        instance = super(GrantFormset, self).save_new(form, commit=commit)

        form.instance = instance

        for nested in form.nested:
            nested.instance = instance

            for cdata in nested.cleaned_data:
                cdata[nested.fk.name] = instance

        return instance

    def should_delete(self, form):
        if self.can_delete:
            raw_delete_value = form._raw_value(DELETION_FIELD_NAME)
            should_delete = form.fields[DELETION_FIELD_NAME].clean(raw_delete_value)

            return should_delete
        return False

    def save_all(self, commit=True):
        objects = self.save(commit=False)

        if commit:
            for o in objects:
                o.save()

        if not commit:
            self.save_m2m()

        for form in set(self.initial_forms + self.saved_forms):
            if self.should_delete(form):
                continue

            for nested in form.nested:
                nested.save(commit=commit)

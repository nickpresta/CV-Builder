# -*- coding: utf-8 -*-
import datetime
import time
import re

from django import forms
from django.forms import ModelForm, Form
from django.forms.models import BaseModelFormSet
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from django.forms.formsets import DELETION_FIELD_NAME

from django.forms.extras.widgets import SelectDateWidget

from cv.models import *

DATE_FORMATS = [
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
    '%d/%m/%Y', '%d/%m/%y',             # '25/10/2006', '25/10/06'
    '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
    '%Y-%m', '%m/%Y', '%m/%y',          # '2006-10', '10/2006', '10/06'
    '%b %Y',                            # 'Oct 2006'
    '%B %Y',                            # 'October 2006'
    '%Y'                                # '2006'
]

class DateWidget(SelectDateWidget):
    """
    A Widget that splits date input into three <select> boxes.
    
    If any of the three date <select>s are left blank, the default 01 is used.
    """
    
    def value_from_datadict(self, data, files, name):
        """ Replace any blank date field with the default 01. """
        data = data.copy()

        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)

        if y == '0':
            data[self.year_field % name] = '0001'
        if m == '0':
            data[self.month_field % name] = '01'
        if d == '0':
            data[self.day_field % name] = '01'

        return super(DateWidget, self).value_from_datadict(data, files, name)

class FormMixin(ModelForm):
    """ Form mixin used to set foreign keys on new model instances. """
    # FIXME: pk should be renamed to fk
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
    """ FormSet mixin used to set foreign keys on new model instances and clean
    sets of forms. """
    # FIXME: pk should be renamed to fk
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

    def clean(self):
        """Clean formset, removing any forms to be deleted."""
        for form in self.forms:
            if self._should_delete_form(form):
                del form.cleaned_data
        # BaseModelFormSet.clean() preforms model uniqueness validation
        super(FormsetMixin, self).clean()

class InlineFormsetMixin(BaseInlineFormSet):
    """ InlineFormSet mixin used to set foreign keys on new model instances. """
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

    year = forms.DateField(input_formats=DATE_FORMATS,
            widget=forms.DateInput(format='%Y'))

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
        if research and teaching and service and (research + teaching + service) != 100:
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
        
class FacultyStartForm(FormMixin):
    faculty_start = forms.DateField(label="Faculty Start Date", required=False,
            widget=DateWidget(required=False, years=range(1940, datetime.date.today().year)))

    class Meta:
        fields = ('faculty_start',)
        model = UserProfile
        
    def clean(self):
        cleaned_data = self.cleaned_data
        start = cleaned_data.get('faculty_start')

        return cleaned_data

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
    start_date = forms.DateField(input_formats=DATE_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}))
    end_date = forms.DateField(input_formats=DATE_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}))

    class Meta:
        fields = ('start_date', 'end_date', 'location', 'rank')
        model = PositionHeld

class PositionPriorForm(FormMixin):
    start_date = forms.DateField(input_formats=DATE_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}))
    end_date = forms.DateField(input_formats=DATE_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}))

    class Meta:
        fields = ('start_date', 'end_date', 'location', 'position')
        model = PositionPrior

class PositionElsewhereForm(FormMixin):
    start_date = forms.DateField(input_formats=DATE_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}))
    end_date = forms.DateField(input_formats=DATE_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}))

    class Meta:
        fields = ('start_date', 'end_date', 'location', 'position')
        model = PositionElsewhere

class OffCampusRecognitionForm(FormMixin):
    class Meta:
        fields = ('off_campus',)
        model = Summary
        widgets = {
            'off_campus': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class CourseJoinForm(FormMixin):
    year = forms.DateField(input_formats=['%Y'], widget=forms.DateInput(format='%Y'))

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
    start_date = forms.DateField(initial=datetime.date.today,
            widget=forms.TextInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(initial=datetime.date.today,
            widget=forms.TextInput(attrs={'class': 'datepicker'}))
    class Meta:
        model = GradAdvisor
        fields = ('student_name', 'degree', 'start_date', 'end_date')

class AdvisorCommitteeForm(FormMixin):
    start_date = forms.DateField(initial=datetime.date.today,
            widget=forms.TextInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(initial=datetime.date.today,
            widget=forms.TextInput(attrs={'class': 'datepicker'}))
    class Meta:
        model = GradAdvisor
        fields = ('student_name', 'degree', 'start_date', 'end_date')

class ExaminerForm(FormMixin):
    date = forms.DateField(initial=datetime.date.today,
            widget=forms.TextInput(attrs={'class': 'datepicker'}))
    class Meta:
        model = GradAdvisor
        fields = ('student_name', 'degree', 'date')

class FreeFormatForm(FormMixin):
    """A form for single page, free format entries in the Summary table."""

    def __init__(self, *args, **kwargs):
        field = kwargs.pop('field', None)
        super(FreeFormatForm, self).__init__(*args, **kwargs)

        self.fields = {
            field: forms.CharField(required=False,
                widget=forms.Textarea(attrs={'rows': '50', 'cols': '40'}))
        }

    class Meta:
        model = Summary

class GrantYearForm(FormMixin):
    start_year = forms.DateField(input_formats=DATE_FORMATS,
        widget=forms.DateInput(format='%Y'))
    end_year = forms.DateField(input_formats=DATE_FORMATS,
        widget=forms.DateInput(format='%Y'))

    class Meta:
        model = GrantYear
        fields = ('title', 'amount', 'start_year', 'end_year')


    def clean(self):
        """ Clean the form according to our custom rules """

        cleaned_data = self.cleaned_data
        start_year = cleaned_data.get("start_year")
        end_year = cleaned_data.get("end_year")

        if start_year and end_year and end_year < start_year:
            msg = "End year must fall after start year."
            self._errors['end_year'] = self.error_class([msg])

            # These fields are no longer valid
            del cleaned_data['end_year']

        return cleaned_data

class GrantSelectForm(Form):
    pass

InvestigatorFormset = inlineformset_factory(Grant, Investigator,
        form=InvestigatorForm, formset=InlineFormsetMixin, extra=0)
GrantYearFormset = inlineformset_factory(Grant, GrantYear,
        form=GrantYearForm, formset=InlineFormsetMixin, extra=0)

class GrantFormset(FormsetMixin):
    """A formset for Grants, with two nested formsets for Investigators and
    GrantYears.
    
    Based on example from 
    http://yergler.net/blog/2009/09/27/nested-formsets-with-django/
    Form fields use the prefix: grants-__prefix__
    Nested form fields use the prefix: grants-__nested_prefix___PREFIX-__prefix__-
    eg: grants-0_gyear-0-id
    
    """
    
    def _get_empty_form(self):
        return super(GrantFormset, self)._get_empty_form()

    def add_fields(self, form, index):
        """Called when creating a new form in this formset, adding nested
        Investigator and GrantYear forms."""

        super(GrantFormset, self).add_fields(form, index)

        try:
            # retrieve Grant associated with this form
            instance = self.get_queryset()[index]
            prefix = re.sub(r'-(?!.*-)', '_', form.prefix)
        except IndexError:
            # form does not exist in formset (new form)
            instance = None
            prefix = re.sub(r'-(?!.*-)', '_', form.prefix)
        except TypeError:
            instance = None
            prefix = re.sub(r'-__prefix__', '___nested_prefix__', form.prefix)

        # create the nested forms
        form.nested = [
            InvestigatorFormset(data=self.data, instance=instance,
                prefix='%s_invest' % prefix, pk=instance),
            GrantYearFormset(data=self.data, instance=instance,
                prefix='%s_gyear' % prefix, pk=instance)
        ]

    def is_valid(self):
        """Validate all the forms in this formset, including their nested forms."""
        result = super(GrantFormset, self).is_valid()

        for form in self.forms:
            if hasattr(form, 'nested'):
                for nestedForm in form.nested:
                    result = result and nestedForm.is_valid()
        return result

    def save_new(self, form, commit=True):
        """Save a new Grant instance.
        
        New GrantYear and Investigator instances will be saved from nested forms.
        
        """
        instance = super(GrantFormset, self).save_new(form, commit=commit)

        form.instance = instance

        for nested in form.nested:
            nested.instance = instance

            for cdata in nested.cleaned_data:
                cdata[nested.fk.name] = instance

        return instance

    def should_delete(self, form):
        """Determine whether a form indicates deletion of a Grant instance.      

        Deltion is specified by the DELETE form field.

        """

        if self.can_delete:
            raw_delete_value = form._raw_value(DELETION_FIELD_NAME)
            should_delete = form.fields[DELETION_FIELD_NAME].clean(raw_delete_value)

            return should_delete
        return False

    def save_all(self, commit=True):
        """Save all forms in this formset, including nested forms.
        
        This should be used instead of the normal save() method.
        
        """
        objects = self.save(commit=False)

        if commit:
            for o in objects:
                o.save()

        if not commit:
            self.save_m2m()

        for form in set(self.initial_forms + self.saved_forms):
            # save forms for existing Grant instances(initial_forms) as well as
            # new Grant instances (saved_forms)

            if self.should_delete(form):
                continue

            for nested in form.nested:
                nested.save(commit=commit)

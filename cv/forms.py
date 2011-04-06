# -*- coding: utf-8 -*-
from django.forms import ModelForm
from cv.models import *
from django import forms
from django.forms.models import BaseModelFormSet
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from django.forms.formsets import DELETION_FIELD_NAME
import datetime

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
        
    Year = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    
    class Meta:
        fields = ('Year', 'Research', 'Teaching', 'Service')
        model = DoETable

    def setPK(self, form):
        form.Faculty_ID = self.pk

    def clean(self):
        """ Clean the form according to our custom rules """
        cleaned_data = self.cleaned_data
        research = cleaned_data.get("Research")
        teaching = cleaned_data.get("Teaching")
        service = cleaned_data.get("Service")

        # ensure that all 3 fields add up to 100
        if (research + teaching + service) != 100:
            msg = "Research, teaching and service must add up to 100"
            self._errors['Research'] = self.error_class([msg])
            self._errors['Teaching'] = self.error_class([msg])
            self._errors['Service'] = self.error_class([msg])

            # These fields are no longer valid
            del cleaned_data['Research']
            del cleaned_data['Teaching']
            del cleaned_data['Service']

        return cleaned_data
        
class FacultyNameDeptForm(FormMixin):
    Faculty_GName = forms.CharField(label='Given Name')
    Faculty_SName = forms.CharField(label='Surname')

    class Meta:
        fields = ('Faculty_GName', 'Faculty_SName', 'Department')
        model = FacultyTable
        
class AccredForm(FormMixin):
    Date = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = AccredTable
        fields = ('Degree', 'Discipline', 'Institution', 'Date')
        widgets = {
            'Degree': forms.Textarea(attrs={'class': 'mceNoEditor'}),
            'Discipline': forms.Textarea(attrs={'class': 'mceNoEditor'}),
            'Institution': forms.Textarea(attrs={'class': 'mceNoEditor'}),
        }

class HonorForm(FormMixin):
    Honor_desc = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'mceNoEditor'}))
    
    class Meta:
        model = HonorTable
        fields = ('Honor_desc',)
    
class FacultyStartForm(FormMixin):
    Faculty_Start = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    class Meta:
        fields = ('Faculty_Start',)
        model = FacultyTable

class ExecutiveSummaryForm(FormMixin):
    class Meta:
        fields = ('Executive',)
        model = SummaryTable
        widgets = {
            'Executive': forms.Textarea(attrs={'rows': '50', 'cols': '40',})
        }
        
class PositionHeldForm(FormMixin):
    StartDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    EndDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    
    class Meta:
        fields = ('StartDate', 'EndDate', 'Location', 'Rank')
        model = PositionHeldTable

class PositionPriorForm(FormMixin):
    StartDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    EndDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        fields = ('StartDate', 'EndDate', 'Location', 'Position')
        model = PositionPriorTable

class PositionElsewhereForm(FormMixin):
    StartDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    EndDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        fields = ('StartDate', 'EndDate', 'Location', 'Position')
        model = PositionElsewhereTable


class OffCampusRecognitionForm(FormMixin):
    class Meta:
        fields = ('OffCampus',)
        model = SummaryTable 

class ResearchActivityForm(FormMixin):
    class Meta:
        model = SummaryTable 
        fields = ('Research',)
        widgets = {
            'Research': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class ReportOnTeachingForm(FormMixin):
    class Meta:
        model = SummaryTable
        fields = ('Teaching',)
        widgets = {
            'Teaching': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class InvestigatorForm(FormMixin):
    class Meta:
        model = InvestigatorTable
        fields = ('Name', 'Amount', 'Role')

class GrantYearForm(FormMixin):
    class Meta:
        model = GrantYearTable
        fields = ('Title', 'Amount', 'StartYear', 'EndYear')

InvestigatorFormset = inlineformset_factory(GrantTable, InvestigatorTable, form=InvestigatorForm, formset=InlineFormsetMixin, extra=1)
GrantYearFormset = inlineformset_factory(GrantTable, GrantYearTable, form=GrantYearForm, formset=InlineFormsetMixin, extra=1)

#class GrantForm(FormMixin):

#    class Meta:
#        model = GrantTable
#        fields = ('Agency', 'SupportType', 'Held')

class GrantForm(FormMixin):
    choice = None
    class Meta:
        model = GrantTable
        fields = ('Held', 'Agency', 'SupportType', 'ProjectTitle')

class GrantFormset(FormsetMixin):
    def __init__(self, *args, **kwargs):
        super(GrantFormset, self).__init__(*args, **kwargs)

    def add_fields(self, form, index):
        super(GrantFormset, self).add_fields(form, index)
        
        try:
            instance = self.get_queryset()[index]
            pk_value = instance.pk
        except IndexError:
            instance = None
            pk_value = hash(form.prefix)
            
        form.nested = [
            InvestigatorFormset(data=self.data, instance=instance,
                prefix='invest_%s' % pk_value, pk=instance),                
            GrantYearFormset(data=self.data, instance=instance,
                prefix='gyear_%s' % pk_value, pk=instance)
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
                print self.pk
                if self.pk:
                    o.setPK(self.pk)
                o.save()
                
        if not commit:
            self.save_m2m()
            
        for form in set(self.initial_forms + self.saved_forms):
            if self.should_delete(form):
                continue
                
            for nested in form.nested:
                nested.save(commit=commit)

from django import forms

class DateForm(forms.Form):
    date_field = forms.DateField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}))

from django import forms

class ResultForm(forms.Form):
    result_link = forms.URLField(label='Result Link', required=True)
    college_code = forms.ChoiceField(label='College Code', choices=[('1604', 'MJCET'), ('1605', 'ISL'), ('1610', 'NSAKCET')], required=True)
    field_code = forms.ChoiceField(label='Field Code', choices=[('748','AIML'),('749','IOT'),('733','CSE')], required=True)
    
    # Changed from ChoiceField to CharField for year
    year = forms.ChoiceField(label='Year', choices=[('20', '4th year'), ('21', '3rd year'), ('22', '2nd year'), ('23', '1st year')], required=True)

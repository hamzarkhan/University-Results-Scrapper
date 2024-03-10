from django import forms

class ResultForm(forms.Form):
    result_link = forms.URLField(label='Result Link', required=True)
    college_code = forms.ChoiceField(label='College Code', choices=[('1604', 'MJCET'), ('1605', 'ISL'), ('1610', 'NSAKCET'),('2455','KMEC'),('2453','NGIT')], required=True)
    field_code = forms.ChoiceField(label='Field Code', choices=[('748','AIML'),('749','IOT'),('750','DS'),('736','MECH'),('733','CSE'),('732','CIVIL')], required=True)
    
    # Changed from ChoiceField to CharField for year
    year = forms.CharField(label='Year', widget=forms.TextInput(attrs={'placeholder': "Enter year of admission exmple if your hallticket is 1610'21'748031 then enter 21 ."}), required=True)

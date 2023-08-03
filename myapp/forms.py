from django import forms
from myapp.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserMentor(forms.ModelForm):
    AVAILABILITY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    availability = forms.MultipleChoiceField(choices=AVAILABILITY_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = CustomUser
        fields = ['major', 'preferred_language', 'availability']
        mentor_field = forms.CharField(max_length=255, required=False)
    def clean(self):
        cleaned_data = super().clean()
        if self.instance.is_mentee:
            raise forms.ValidationError("A user cannot be both a mentor and a mentee.")
        return cleaned_data

class UserMentee(forms.ModelForm):
    AVAILABILITY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    availability = forms.MultipleChoiceField(choices=AVAILABILITY_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = CustomUser
        fields = ['major', 'preferred_language', 'availability']
        mentee_field = forms.CharField(max_length=255, required=False)
    def clean(self):
        cleaned_data = super().clean()
        if self.instance.is_mentor:
            raise forms.ValidationError("A user cannot be both a mentor and a mentee.")
        return cleaned_data
    
# forms.py
MAJOR_CHOICES = [
    ('Accounting', 'Accounting'),
    ('Business Management', 'Business Management'),
    ('Computer Information Systems', 'Computer Information Systems'),
    ('Computer Network Technology', 'Computer Network Technology'),
    ('Health Information Technology', 'Health Information Technology'),
    ('Nursing', 'Nursing'),
    ('Paramedic', 'Paramedic'),
    ('Respiratory Therapy', 'Respiratory Therapy'),
    ('Small Business/Entrepreneurship', 'Small Business/Entrepreneurship'),
    ('Art Foundations: Art History', 'Art Foundations: Art History'),
    ('Bilingual Childhood Education', 'Bilingual Childhood Education'),
    ('Childhood Education', 'Childhood Education'),
    ('Children and Youth Studies', 'Children and Youth Studies'),
    ('Communication Studies', 'Communication Studies'),
    ('Criminal Justice', 'Criminal Justice'),
    ('Critical Thinking and Justice', 'Critical Thinking and Justice'),
    ('Economics', 'Economics'),
    ('Ethnic Studies', 'Ethnic Studies'),
    ('Gender and Women’s Studies', 'Gender and Women’s Studies'),
    ('History', 'History'),
    ('Liberal Arts*', 'Liberal Arts*'),
    ('Linguistics and Literacy', 'Linguistics and Literacy'),
    ('Modern Languages: French', 'Modern Languages: French'),
    ('Modern Languages: Italian', 'Modern Languages: Italian'),
    ('Modern Languages: Spanish', 'Modern Languages: Spanish'),
    ('Modern Languages: Spanish Translation and Interpretation', 'Modern Languages: Spanish Translation and Interpretation'),
    ('Political Science', 'Political Science'),
    ('Psychology', 'Psychology'),
    ('Secondary Education for Social Studies', 'Secondary Education for Social Studies'),
    ('Sociology', 'Sociology'),
    ('Urban Studies', 'Urban Studies'),
    ('Writing and Literature', 'Writing and Literature'),
    ('Accounting for Forensic Accounting', 'Accounting for Forensic Accounting'),
    ('Animation and Motion Graphics', 'Animation and Motion Graphics'),
    ('Art Foundations: Studio Art', 'Art Foundations: Studio Art'),
    ('Biotechnology Science', 'Biotechnology Science'),
    ('Business Administration', 'Business Administration'),
    ('Child Care/Early Childhood Education', 'Child Care/Early Childhood Education'),
    ('Community Health Education', 'Community Health Education'),
    ('Computer Science', 'Computer Science'),
    ('Data Science', 'Data Science'),
    ('Digital Marketing', 'Digital Marketing'),
    ('Engineering Science', 'Engineering Science'),
    ('Financial Management', 'Financial Management'),
    ('Geographic Information Science', 'Geographic Information Science'),
    ('Gerontology', 'Gerontology'),
    ('Human Services', 'Human Services'),
    ('Mathematics', 'Mathematics'),
    ('Mathematics and Sciences for Secondary Education', 'Mathematics and Sciences for Secondary Education'),
    ('Multimedia Programming and Design', 'Multimedia Programming and Design'),
    ('Music', 'Music'),
    ('Public and Nonprofit Administration', 'Public and Nonprofit Administration'),
    ('Public Health', 'Public Health'),
    ('School Health Education', 'School Health Education'),
    ('Science', 'Science'),
    ('Science for Forensics', 'Science for Forensics'),
    ('Science for Health', 'Science for Health'),
    ('Theatre', 'Theatre'),
    ('Video Arts and Technology', 'Video Arts and Technology'),
    ('Cybersecurity', 'Cybersecurity'),
    ('Accounting Certificate', 'Accounting Certificate'),
    ('Cybersecurity Certificate', 'Cybersecurity Certificate'),
    ('Health Informatics Certificate', 'Health Informatics Certificate'),
    ('Practical Nursing Certificate', 'Practical Nursing Certificate'),
    ('Spanish Translation for the Health, Legal and Business Professions Certificate', 'Spanish Translation for the Health, Legal and Business Professions Certificate'),
]

class UserEditForm(forms.ModelForm):
    is_mentor = forms.BooleanField(label="Mentor", required=False)
    is_mentee = forms.BooleanField(label="Mentee", required=False)
    major = forms.ChoiceField(choices=MAJOR_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'emplid', 'preferred_language', 'is_mentor', 'is_mentee', 'major']


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    major = forms.ChoiceField(choices=MAJOR_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'major']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


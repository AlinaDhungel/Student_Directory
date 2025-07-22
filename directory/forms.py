from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.html import format_html
import re
from django.contrib.auth.password_validation import validate_password
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'semester', 'faculty', 'section']  # Use your model fields here

class CustomRegisterForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=10,
        min_length=10,
        label="Phone Number",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 10-digit phone number',
            'pattern': '[0-9]{10}',
            'title': 'Please enter exactly 10 digits'
        }),
        help_text="Enter a 10-digit phone number without spaces or special characters."
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a strong password',
            'autocomplete': 'new-password'
        }),
        label="Password",
        help_text=format_html("""
            <ul class="password-requirements">
                <li>At least 8 characters</li>
                <li>Contains both letters and numbers</li>
                <li>Optional: special characters for extra security</li>
            </ul>
        """)
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'autocomplete': 'username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email address',
                'autocomplete': 'email'
            }),
        }
        help_texts = {
            'username': '',  # This line removes the default username help text
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Remove colon from labels

    def clean_username(self):
        username = self.cleaned_data.get('username').strip()
        if not username:
            raise ValidationError("Username is required.", code='username_required')
        if len(username) < 4:
            raise ValidationError("Username must be at least 4 characters long.", code='username_too_short')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if not email:
            raise ValidationError("Email is required for account verification and recovery.", code='email_required')
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError("Please enter a valid email address (e.g., example@domain.com).", code='invalid_email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use another or try to login.", code='email_exists')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone').strip()
        if not phone:
            raise ValidationError("Phone number is required for important notifications.", code='phone_required')
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits (0-9).", code='phone_non_digit')
        if len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits long.", code='phone_length')
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError("Password cannot be empty.", code='password_empty')
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(e.messages)
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.", code='password_too_short')
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one number.", code='password_no_number')
        if not any(char.isalpha() for char in password):
            raise ValidationError("Password must contain at least one letter.", code='password_no_letter')
        return password

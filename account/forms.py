from django import forms
from django.contrib.auth.models import User
from . import models

class AccountForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = '__all__'
        exclude = ('user',)

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Password',
    )

    password_confirmation = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Password Confirmation'
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 
                'password', 'password_confirmation', 'email')
    
    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_messages = {}
        
        user_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password_confirmation_data = cleaned.get('password_confirmation')

        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'This User already exists.'
        error_msg_email_exists = 'This Email already exists.'
        error_msg_password_match = 'The two passwords do not match.'
        error_msg_password_short = 'Your password needs at least 6 characters.'
        error_msg_required_field = 'This field is required.'

        if self.user:
            if user_db:
                if user_data != user_db.username:
                    validation_error_messages['username'] = error_msg_user_exists
            if email_db:
                if email_data != email_db.email:
                    validation_error_messages['email'] = error_msg_email_exists

            if password_data:
                if password_data != password_confirmation_data:
                    validation_error_messages['password'] = error_msg_password_match
                    validation_error_messages['password_confirmation'] = error_msg_password_match
                
                if len(password_data) < 6:
                    validation_error_messages['password'] = error_msg_password_short
        else:
            if user_db:
                validation_error_messages['username'] = error_msg_user_exists

            if email_db:
                validation_error_messages['email'] = error_msg_email_exists

            if not password_data:
                validation_error_messages['password'] = error_msg_required_field
            
            if not password_confirmation_data:
                validation_error_messages['password_confirmation'] = error_msg_required_field

            if password_data != password_confirmation_data:
                validation_error_messages['password'] = error_msg_password_match
                validation_error_messages['password_confirmation'] = error_msg_password_match
        
            if len(password_data) < 6:
                validation_error_messages['password'] = error_msg_password_short

        if validation_error_messages:
            raise(forms.ValidationError(validation_error_messages))
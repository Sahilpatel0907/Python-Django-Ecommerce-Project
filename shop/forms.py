from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import CustomerProfile


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your Email Address'}))
	first_name = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your First Name'}))
	last_name = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Enter Your User Name'
		self.fields['username'].label = 'UserName'
		self.fields['username'].help_text = None
		
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Enter Your Password'
		self.fields['password1'].label = 'Password'
		self.fields['password1'].help_text = None
		
		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Enter Your Confirm Password'
		self.fields['password2'].label = 'Confirm Password'
		self.fields['password2'].help_text = None

class UpdateUserForm(UserChangeForm):
    password = None
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email Address'}))
    first_name = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your First Name'}))
    last_name = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Your User Name'})
        self.fields['username'].label = 'User Name'
        self.fields['username'].help_text = None
        
class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Your Password'
        })
        self.fields['new_password1'].label = 'Password'
        self.fields['new_password1'].help_text = None

        # Update attributes for new_password2
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Your Confirm Password'
        })
        self.fields['new_password2'].label = 'Confirm Password'
        self.fields['new_password2'].help_text = None

class UserInfoForm(forms.ModelForm):
	phone = forms.CharField(label="Phone Number:", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), required=False)
	address1 = forms.CharField(label="Address1", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}), required=False)
	address2 = forms.CharField(label="Address2", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}), required=False)
	city = forms.CharField(label="City :", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=False)
	state = forms.CharField(label="State :", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
	zipcode = forms.CharField(label="Zipcode :", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=False)
	country = forms.CharField(label="Country :", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=False)

	class Meta:
		model = CustomerProfile
		fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', )
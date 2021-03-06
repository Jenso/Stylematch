#-*- coding:utf-8 -*-
from accounts.models import UserProfile
from braces.views import LoginRequiredMixin
from django import forms
from django.forms import ModelForm, ValidationError
from django.views.generic import UpdateView
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from registration.backends.default import DefaultBackend
from registration.forms import RegistrationForm

from accounts.views import (OpenHoursView,
                            ServicesView,
                            SaveProfileImageView,
                            get_unique_filename)

from index.models import BetaEmail

import logging
logger = logging.getLogger(__name__)


class SignupViewForm(ModelForm):
    """
    Form used in registration step 1, used to filter out wanted fields

    """
    salon_phone_number = forms.CharField(label='Telefonnummer för bokning',
                                         required=False)

    def __init__(self, *args, **kwargs):
        super(SignupViewForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields = ('salon_name',
                  'salon_adress',
                  'salon_city',
                  'salon_phone_number')


class SignupView(LoginRequiredMixin, UpdateView):
    """
    Step 1 in the user registration, after the main user registration.
    The user is asked to fill in some of the other fields.

    """
    template_name = "accounts/signup_step1.html"
    form_class = SignupViewForm

    def __init__(self, *args, **kwargs):
        super(SignupView, self).__init__(*args, **kwargs)
        self.success_url = reverse('signupstep2_page')

    def get_object(self, queryset=None):
        obj = UserProfile.objects.get(user__exact=self.request.user.id)
        return obj

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)

        context['progress_salon_info'] = "reached-progress"
        context['progress_width'] = "40.5%"

        context['no_menu'] = True

        # used to determine if it's a newly registered user
        # -> display more clearly where he should go on profile page
        self.request.session['extra_user_guidance'] = True
        return context


class SignupStep2View(SaveProfileImageView):
    template_name = "accounts/signup_step2.html"

    def __init__(self, *args, **kwargs):
        super(SignupStep2View, self).__init__(*args, **kwargs)
        # written here in init since it will give reverse url error
        # if just written in class definition. because urls.py isnt loaded
        # when this class is defined
        self.success_url = reverse('signupstep2_page')

    def get_context_data(self, **kwargs):
        context = super(SignupStep2View, self).get_context_data(**kwargs)

        context['progress_salon_info'] = "reached-progress"
        context['progress_salon_hours'] = "reached-progress"
        context['progress_salon_price'] = "reached-progress"
        context['progress_profile_pic'] = "reached-progress"
        context['progress_width'] = "66%"

        context['no_menu'] = True
        return context


def handle_invite_code(request, new_user):
    """
    Check if the user uses an invite code, if it's a valid invite cod,
    set the invite code as used by this user.
    
    ´new user´ is the user that was created with the invite code
    """
    if request.GET.get('kod'):
        supplied_invite_code = request.GET.get('kod')
        #try:
        #    pass
        #invite_code = InviteCode.objects.get(
        #            invite_code__iexact=supplied_invite_code,
        #            used=False,
        #            reciever=None)
        #except InviteCode.DoesNotExist:
        #    logger.debug('New user registered: Supplied invite code'
        #                 ' but it wasnt valid')
        #else:
        #    logger.info('New user registered: Used a valid invite code')
        #    invite_code.used = True
        #    invite_code.reciever = new_user
        #    invite_code.save()


class RegisterCustomBackend(DefaultBackend):
    """
    Extends django registration DefaultBackend, since we want
    to activate the user, save first_name and last_name.
    Followed this example:
    http://inka-labs.com/en-us/blog/2012/01/13/add-custom-backend-django-registration/

    TODO:
    Possible problem, the guide said you have to define a skeleton and
    call super, for the other functions to work. But I dont think you need to.
    """
    def register(self, request, **kwargs):
        user = super(RegisterCustomBackend, self).register(request, **kwargs)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        # login the newly registered user
        login(request, user)

        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']
        # set is_active = True, must be set and saved to DB after login
        # function is called.
        user.is_active = True

        user.save()

        #handle_invite_code(request, user)

        # update the used invitecode (if any)
        #invite_code = kwargs['invite_code']
        #if invite_code is not None:
        #    invite_code.reciever = user
        #    invite_code.save()

        return user


class UserRegistrationForm(RegistrationForm):
    """
    Custom user registration form. Used as the main registration form.
    """

    email = forms.CharField(required=False)
    first_name = forms.CharField(label="Förnamn")
    last_name = forms.CharField(label="Efternamn")
    #invite_code = forms.CharField(label="Inbjudningskod "
    #                                    "(just nu behövs en inbjudan "
    #                                    "för att gå med)")

    username = forms.EmailField(max_length=64, label="Emailadress")

    def clean_email(self):
        """
        Since its actually not the email field but the username
        presented on form we use username as email too.
        """
        email = ""
        try:
            email = self.cleaned_data['username']
        except:
            email = ""

        return email

    def UNUSED_clean_invite_code(self):
        """
        Validates that the user have supplied a valid invite code.
        And marks the code as used, if the other fields are correctly filled.

        NOTE: Match on invite code is case insensitive.

        """
        supplied_invite_code = self.cleaned_data['invite_code']
        try:
            invite_code = InviteCode.objects.get(
                        invite_code__iexact=supplied_invite_code,
                        used=False,
                        reciever=None)
        except InviteCode.DoesNotExist:
            # a permanent key which can be used by us
            if (supplied_invite_code == "permanent1" or
                supplied_invite_code == "gxc347"):
                return None

            raise forms.ValidationError(u'Din inbjudningskod (\'%s\') '
                                        u'var felaktig. Vänligen kontrollera '
                                        u'att du skrev rätt.'
                                        % supplied_invite_code)

        # only set the invite code to used=True if all other fields have
        # validated correctly
        # TODO:
        # this is run even if the passwords doesnt match in the clean()
        # method. since this function is run before clean()
        if self.is_valid():
            invite_code.used = True
            invite_code.save()
            return invite_code

        return None

    def clean(self):
        """
        Verifies that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        """
        if ('password1' in self.cleaned_data and
            'password2' in self.cleaned_data):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')


            if password1 != password2:
                error_msg = "Lösenorden stämmer ej överens"
                self._errors['password1'] = self.error_class([error_msg])
                raise ValidationError(error_msg)

            MIN_LENGTH = 5
            if len(password1) < MIN_LENGTH:
                error_msg = "Lösenordet är för kort, minst 5 tecken."
                self._errors['password1'] = self.error_class([error_msg])
                raise forms.ValidationError(error_msg)

        return self.cleaned_data

    class Meta:
        exclude = ('email',)

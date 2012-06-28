#!/usr/bin/python
#-*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.files.storage import default_storage
from registration.signals import user_registered

from tools import list_with_time_interval, format_minutes_to_pretty_format

weekdays_model = ['mon', 'tues', 'wed', 'thurs', 'fri', 'sat', 'sun']

# used on all fields that need to have a forced max_length
# django doesnt do this validation by itself
# the value given to MaxLengthValidator should be same as max_length variable
from django.core.validators import MaxLengthValidator

import uuid
import os
import re


def create_temporary_profile_url(sender, user, request, **kwargs):
    """
    Create a standard profile url at signup step using first name and
    last name. Add number if the url is already taken.

    John Nelson       -> /john-nelson
    John Nelson again -> /john-nelson2

    If, for some reason, first name isn't in POST data, bail out.
    """

    if 'first_name' not in request.POST:
        return
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    users = User.objects.filter(first_name=first_name,
                                last_name=last_name)
    names = (first_name +" "+ last_name).split(' ')
    tmp_url = "-".join(names)
    tmp_url = re.sub(r'\s', '', tmp_url)
    if len(users) > 1:
        tmp_url += "%d" % (len(users))
    userprofile = UserProfile.objects.get(user=user)
    userprofile.profile_url = tmp_url.lower()
    userprofile.save()
user_registered.connect(create_temporary_profile_url)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    When a a new user is created, create a corresponding UserProfile
    TODO:
    Create different profiles depending on if it's a stylist or a regular user
    """
    if created:
        UserProfile.objects.create(
                user=instance,
                temporary_profile_url=uuid.uuid4().hex,
                                   )
        OpenHours.objects.create(user=instance)


class Service(models.Model):
    buffer = list_with_time_interval(
                start=30,
                stop=6 * 60,
                interval=30,
                format_function=format_minutes_to_pretty_format)
    TIME_CHOICES = tuple(buffer)

    length = models.IntegerField("Tidsåtgång *",
                                 choices=TIME_CHOICES,
                                 max_length=3)
    name = models.CharField("Namn (ex. Klippning kort hår) *",
                            max_length=20)
    price = models.IntegerField("Pris i kronor *", max_length=6)

    # TODO: längd på desc?
    description = models.CharField("Beskrivning (ex. Inklusive styling)",
                                   max_length=200,
                                   validators=[MaxLengthValidator(200)],
                                   blank=True)
    display_on_profile = models.BooleanField("Visa på profil", blank=True)

    # user that has this service
    user = models.ForeignKey(User, editable=False)
    order = models.PositiveIntegerField(blank=True, editable=True, null=True)

    class Meta:
        # deliver the services sorted on the order field
        # needs to be here, or the services admin ui will break
        ordering = ['order']


class OpenHours(models.Model):
    """
    TODO: Fix model description
    """

    # Do not change if you dont know what you're doing!!
    closed_value = -1

    time_list = list_with_time_interval(
                start=60 * 6,
                stop=60 * 24,
                interval=15)
    time_list.insert(0, (closed_value, 'Stängt'))

    # Since Python tuples are immutable we need to use a list as
    # a temporary buffer
    time_tuple = tuple(time_list)

    user = models.ForeignKey(User, editable=False)

    # 8:00 AM
    default_open_time = 480
    # 17:00 PM
    default_close_time = 1020

    # For time being, default lunches to always be closed.
    default_lunch_open = closed_value
    default_lunch_close = closed_value

    # Store days who should be defaulted as closed in a list for easier
    # configuration in future.
    default_closed_days = ['sun']

    # Instead of having duplicate code we generate the code dynamically and
    # execute it. FIXME: This MIGHT be unsafe, so if any problem occurs in
    # this model this is probably why.
    for day in weekdays_model:
        if day in default_closed_days:
            default_open_time = closed_value
            default_close_time = closed_value

        code = (day + ' = models.IntegerField('
                                    '"",'
                                    'choices=time_tuple,'
                                    'default=' + str(default_open_time) + ')')
        exec(code)

        code = (day + '_closed = models.IntegerField('
                                    '"",'
                                    'choices=time_tuple,'
                                    'default=' + str(default_close_time) + ')')
        exec(code)


# client side url to images, without image filename
# used in the view that edit the images on the profile
def get_image_url(filename):
    return os.path.join(settings.MEDIA_URL,
                        settings.PATH_USER_IMGS,
                        filename)


class BaseImage(models.Model):
    # server-side, full path to upload image including filename
    def get_image_path(instance, filename):
        return os.path.join(settings.UPLOAD_PATH_USER_IMGS, instance.filename)

    def get_image_url(self):
        return get_image_url(self.filename)

    def __unicode__(self):
        return self.filename

    file = models.ImageField(upload_to=get_image_path,
                             blank=True)
    filename = models.CharField(max_length=50,
                                blank=True)
    user = models.ForeignKey(User,
                             editable=False)
    upload_date = models.DateTimeField(auto_now_add=True,
                                       editable=False)

    class Meta:
        abstract = True


class ProfileImage(BaseImage):
    cropped = models.BooleanField(default=False)


class GalleryImage(BaseImage):
    comment = models.CharField(max_length=100,
                               blank=True)
    order = models.PositiveIntegerField(blank=True,
                                        editable=True,
                                        null=True)
    display_on_profile = models.BooleanField("Visa på profil",
                                             blank=True,
                                             default=True)

    class Meta:
        # deliver the images sorted on the order field
        # needs to be here, or the edit_images ui will break
        ordering = ['order']


class UserProfile(models.Model):
    """
    TODO:
    fixa så email från huvudprofilen visas här
    fixa så twitter och facebook profil visas här, se styleseat
    fixa description till denna modell
    """
    user = models.ForeignKey(User, unique=True, editable=False)

    visible = models.BooleanField(
        "Visa i sökresultat och visa användarens bilder", default=False)

    # max_length? less?
    profile_text = models.CharField("Om mig", max_length=500, blank=True)

    profile_url = models.CharField("http://stylematch.se/",
                                   max_length=40,
                                   blank=True)
    # used to reach profile if no profile_url set
    temporary_profile_url = models.CharField(editable=False,
                                             unique=True,
                                             max_length=36)

    # select phone number to display on profile
    DISPLAY_NUMBER_CHOICES = (
        (True, 'Personligt telefonnummer'),
        (False, 'Salongens telefonnummer'),
        )
    number_on_profile = models.BooleanField(
        "Vilket telefonnummer ska visas på profilen?",
        max_length=1,
        default=False,
        choices=DISPLAY_NUMBER_CHOICES)
    
    personal_phone_number = models.CharField("Personligt telefonnummer",
                                             max_length=30,
                                             blank=True,
                                             null=True)

    # salong
    salon_phone_number = models.CharField("Salongens telefonnummer",
                                          max_length=30,
                                          blank=True,
                                          null=True)
    salon_name = models.CharField("Salongens namn",
                                  max_length=30,
                                  blank=True)
    salon_city = models.CharField("Stad",
                                  max_length=30,
                                  blank=True)
    salon_url = models.URLField("Salongens hemsida",
                                blank=True)
    salon_adress = models.CharField("Salongens adress",
                                    max_length=30,
                                    blank=True)

    zip_adress = models.CharField("Postnummer",
                                  max_length=20,
                                  blank=True,
                                  null=True)

    url_online_booking = models.URLField("Adress till online bokningssystem",
                                         blank=True)
    show_booking_url = models.BooleanField("Min salong har online-bokning",
                                           blank=True)

    # on_delete=models.SET_NULL, since we dont want to delete UserProfile
    # when profile_image is deleted
    profile_image_cropped = models.ForeignKey(ProfileImage,
                                              unique=True,
                                              editable=False,
                                              null=True,
                                              blank=True,
                                              on_delete=models.SET_NULL,
                                              related_name='profile_image_cropped')
    profile_image_uncropped = models.ForeignKey(ProfileImage,
                                                unique=True,
                                                editable=False,
                                                null=True,
                                                blank=True,
                                                on_delete=models.SET_NULL,
                                                related_name='profile_image_uncropped')

    def save(self, *args, **kwargs):
        # remove accidental whitespaces from city
        self.salon_city = self.salon_city.strip()

        return super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s, %s' % (self.user, self.salon_city)


# Signals handler for deleting files after object record deleted
# In Django 1.3, delete a record not remove the associated files
def delete_filefield(sender, **kwargs):
    """Automatically deleted files when records removed.

    On Django 1.3, removing records will not followed by deleting files.
    Should manually delete PDF using signals post_delete.

    This function can be done more generic

    https://github.com/h3/django-webcore/blob/master/webcore/utils/storage.py#L8
    Explanation in comment 1 -
    http://obroll.com/automatically-delete-file-in-filefield-django-1-3-when-object-record-deleted/
    """
    instance = kwargs.get('instance')

    """
    The most natural way to get name of file would be instance.file.path
    but since we're using amazon S3 for storage, the file object does not
    have a path() method, which is called when trying to get attribute .path
    of a file object. -> using attribute .name which we save in the
    model.
    -> This will probably be a problem if we move to filebased storage.
    """
    default_storage.delete(instance.file.name)
post_delete.connect(delete_filefield, ProfileImage)
post_delete.connect(delete_filefield, GalleryImage)


class InviteCode(models.Model):
    used = models.BooleanField("Have the invite code been used?",
                               default=False)
    invite_code = models.CharField("The string to use as invite code",
                                   max_length=30)
    comment = models.CharField("To who was the invitecode given? And so on..",
                               max_length=500)

    def __unicode__(self):
        return u'Invitecode: %s Used: %s' % (self.invite_code, self.used)


class Featured(models.Model):
    user = models.ForeignKey(UserProfile, null=False, blank=False)
    city = models.CharField("City", max_length=30, null=False, blank=False)

    def __unicode__(self):
        return "%s in %s" % (self.user.user.username, self.city)

    class Meta:
        unique_together = ('user', 'city')
        verbose_name_plural = "Featured profiles"

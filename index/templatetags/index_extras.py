"""
Global filters needed in all templates
"""

from django.conf import settings
from django import template
register = template.Library()


# Now, inside a template you can do {{ template_var|pdb }} and enter a pdb session
@register.filter 
def pdb(element):
    import ipdb; ipdb.set_trace()
    return element

@register.simple_tag
def current_url(request):
   from django.core.urlresolvers import resolve
   current_url = resolve(request.get_full_path()).url_name
   return current_url

@register.simple_tag
def active(request, pattern):
    #import pdb;pdb.set_trace()
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''

@register.simple_tag
def google_analytics():
    if settings.PRODUCTION:
        return '<script src="%sjs/google_analytics.js" type="text/javascript"></script>' % settings.STATIC_URL

    return ""

@register.simple_tag
def intercom_analytics():
    if settings.PRODUCTION:
        return '<script src="%sjs/intercom_analytics.js" type="text/javascript"></script>' % settings.STATIC_URL

    return ""

@register.simple_tag
def facebook():
        return '<script src="%sjs/facebook.js" type="text/javascript"></script>' % settings.STATIC_URL

@register.filter
def get_userprofile(user):
    return user.get_profile()

@register.filter
def profile_image(userprofile):
    try:
        # display cropped profile image if there's any
        if userprofile.profile_image_cropped:
            profile_image = userprofile.profile_image_cropped
        else:
            profile_image = userprofile.profile_image_uncropped

        profile_image = profile_image.get_image_url()
    except:
        profile_image = os.path.join(
                            settings.STATIC_URL,
                            'img/default_image_profile_not_logged_in.jpg')
    return profile_image

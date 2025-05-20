from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group

# import lesgv.settings.secrets.lesecret

from .settings import *
# from .websites import *

STATIC_ROOT = "/var/www/wagtail/static/"
STATIC_URL = "/static/"

MEDIA_ROOT = "/var/www/wagtail/medias/"
MEDIA_URL = "/medias/"

@receiver(user_signed_up)
def user_signed_up_callback(sender, request, user, **kargs):
    dashboard_user_group = Group.objects.get(name="dashboard")
    if dashboard_user_group:
      user.groups.add(dashboard_user_group)

# https://www.grandv.org/accounts/oidc/key-lesgrandsvoisins-com/login/?process=wagtailadmin/login/
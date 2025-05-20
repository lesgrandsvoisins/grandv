from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group


@receiver(user_signed_up)
def user_signed_up_callback(sender, request, user, **kargs):
    dashboard_user_group = Group.objects.get(name="dashboard")
    if dashboard_user_group:
      user.groups.add(dashboard_user_group)

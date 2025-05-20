from django.apps import AppConfig


def user_signed_up_callback(sender, request, user, **kargs):
    from django.contrib.auth.models import Group

    dashboard_user_group = Group.objects.get(name="dashboard")
    if dashboard_user_group:
        user.groups.add(dashboard_user_group)


class LesgrandsvoisinsAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lesgrandsvoisins.admin'
    label = 'lesgrandsvoisins_admin'

    # def ready(self):
    #     from allauth.account.signals import user_signed_up
    #     user_signed_up.connect(user_signed_up_callback)

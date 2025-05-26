from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from wagtail.models import Page, PageViewRestriction
from wagtail.permission_policies.pages import PagePermissionPolicy

@login_required
def list_accessible_pages(request):
    # Get all live pages
    all_pages = Page.objects.live().specific().filter(depth__gt=1)
    
    # Get Wagtail's page permission policy
    permission_policy = PagePermissionPolicy()
    
    accessible_pages = []
    
    for page in all_pages:
        # Check if the page has any view restrictions
        restrictions = PageViewRestriction.objects.filter(page=page)
        
        if restrictions.exists():
            # If there are restrictions, check if user has access
            has_access = any(
                restriction.accept_request(request)
                for restriction in restrictions
            )
            if has_access:
                accessible_pages.append(page)
        else:
            # If no restrictions, check standard permissions
            if permission_policy.user_has_permission(request.user, 'view'):
                accessible_pages.append(page)
    
    # Sort pages by title (or any other field you prefer)
    accessible_pages.sort(key=lambda x: x.title)
    
    context = {
        'pages': accessible_pages,
        'user': request.user,
    }

    return render(request, 'lesgrandsvoisins/annuaire/list_edit_pages.html', context)


@login_required
def list_modifiable_pages(request):
    # Get all live pages
    all_pages = Page.objects.live().specific().filter(depth__gt=1)
    
    # Get Wagtail's page permission policy
    permission_policy = PagePermissionPolicy()
    
    modifiable_pages = []
    
    for page in all_pages:
        # Check if user has edit permission for this page
        if permission_policy.user_has_permission_for_instance(
            request.user, 'edit', page
        ):
            modifiable_pages.append(page)
    
    # Sort pages by title
    modifiable_pages.sort(key=lambda x: x.title)
    
    context = {
        'pages': modifiable_pages,
        'user': request.user,
    }
    
    return render(request, 'lesgrandsvoisins/annuaire/list_pages.html', context)
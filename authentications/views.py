from django.shortcuts import render
from django.core.exceptions import PermissionDenied


######## Restrict the vendor from accessing the customer page ########
def check_role_company(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


######### Restrict the customer from accessing the vendor page ########
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
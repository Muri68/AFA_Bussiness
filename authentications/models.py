from django.db import models
from django.contrib.auth.models import AbstractBaseUser,    BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

######## Saving Files of each User on his Directory ########
def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (instance.user.id, filename)
    return "user_{0}/{1}".format(instance.user.id, filename)



########## User Model ##########

class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    BUSINESS = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (BUSINESS, 'Business'),
        (CUSTOMER, 'Customer'),
    )
    
    email = models.EmailField(max_length=254, unique=True)
    website = models.CharField(max_length=254)
    company_name = models.CharField(max_length=254)
    mobile_number = models.CharField(max_length=254)
    job_title = models.CharField(max_length=254)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, default=BUSINESS, blank=True, null=True)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_role(self):
        if self.role == 1:
            user_role = 'Business'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)


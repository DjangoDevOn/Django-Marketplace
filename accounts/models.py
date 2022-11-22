import uuid
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
# Auth/User
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin



class Selling(models.Model):
    SELLING_CHOICES =(
    ("Electronics", "Electronics"),
    ("Camping", "Camping"),
    ("Property", "Property"),
    ("Sporting", "Sporting"),
    ("Vehicles", "Vehicles"),
    ("Gardening", "Gardening"),
    ("Tools", "Tools"),
    ("Household", "Household"),
    )
    selling = models.CharField(max_length=50, blank=True, choices=SELLING_CHOICES)

    def __str__(self):
        return self.selling


################################### CUSTOM USER MODEL ###################################
class CustomUserManager(BaseUserManager):
    
    def create_user(self, selling, useralias, email, first_name, last_name, company_name, business_street_address, business_street_address2, city, state, zip_code, company_phone_number, profile_photo, password=None,):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            useralias=useralias,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            business_street_address=business_street_address,
            business_street_address2=business_street_address2,
            city=city,
            state=state,
            zip_code=zip_code,
            company_phone_number=company_phone_number,
            profile_photo=profile_photo,
            buyer_account=models.BooleanField(default=False),
            selling=selling,
        )

        user.set_password(password)
        # Toggle if: superuser create broke from this stuff
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        # endToggle if: superuser broke
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    
class User(AbstractUser, PermissionsMixin):
    STATE_CHOICES =(
    ("Alabama", "Alabama"),
    ("Alaska", "Alaska"),
    ("Arizona", "Arizona"),
    ("Arkansas", "Arkansas"),
    ("California", "California"),
    ("Colorado", "Colorado"),
    ("Connecticut", "Connecticut"),
    ("Delaware", "Delaware"),
    ("Florida", "Florida"),
    ("Georgia", "Georgia"),
    ("Hawaii", "Hawaii"),
    ("Idaho", "Idaho"),
    ("Illinois", "Illinois"),
    ("Indiana", "Indiana"),
    ("Iowa", "Iowa"),
    ("Kansas", "Kansas"),
    ("Kentucky", "Kentucky"),
    ("Louisiana", "Louisiana"),
    ("Maine", "Maine"),
    ("Maryland", "Maryland"),
    ("Massachusetts", "Massachusetts"),
    ("Michigan", "Michigan"),
    ("Minnesota", "Minnesota"),
    ("Mississippi", "Mississippi"),
    ("Missouri", "Missouri"),
    ("Montana", "Montana"),
    ("Nebraska", "Nebraska"),
    ("Nevada", "Nevada"),
    ("New", "New"),
    ("New", "New"),
    ("New", "New"),
    ("New", "New"),
    ("North", "North"),
    ("North", "North"),
    ("Ohio", "Ohio"),
    ("Oklahoma", "Oklahoma"),
    ("Oregon", "Oregon"),
    ("Pennsylvania", "Pennsylvania"),
    ("Rhode", "Rhode"),
    ("South", "South"),
    ("South", "South"),
    ("Tennessee", "Tennessee"),
    ("Texas", "Texas"),
    ("Utah", "Utah"),
    ("Vermont", "Vermont"),
    ("Virginia", "Virginia"),
    ("Washington", "Washington"),
    ("West", "West"),
    ("Wisconsin", "Wisconsin"),
    ("Wyoming", "Wyoming"),
    )
    useralias = models.CharField(max_length=50, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    profile_photo = models.ImageField(default='avatar1.jpg')
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    company_name = models.CharField(max_length=250, blank=True)
    business_street_address = models.CharField(max_length=100, blank=True)
    business_street_address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True, choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=100, blank=True)
    company_phone_number = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=200)
    buyer_account = models.BooleanField(default=False)
    selling = models.ManyToManyField(Selling, blank=True)


    @property
    def imageURL(self):
        try:
            url = self.profile_photo.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.user.username
    
    
    username = None
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    
    objects = CustomUserManager()
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# extends the profile
class UserNotificationSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="notification_user", on_delete=models.CASCADE)
    notify_support = models.BooleanField(default=True)
    notify_marketing = models.BooleanField(default=True)
    notify_activity = models.BooleanField(default=True)
    notify_messages = models.BooleanField(default=True)
    notify_referral = models.BooleanField(default=True)

    def __str__(self):
        return self.user.useralias



################################### FAQ ###################################
class FaqCat(models.Model):
    cat_title = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.cat_title


class Faq(models.Model):
    category = models.ForeignKey(FaqCat, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    answer = RichTextField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question






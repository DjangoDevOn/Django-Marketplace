from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *
# from website.models import *
from .models import *
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from marketplace.models import BuyerRequest, ChatMessage, SellerQuote
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect, render
from django.views.generic import UpdateView, View
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
# from django.core.mail import send_mail


################################### AJAX VIEWS ###################################
 
def quoteAcceptedRejectedCount(request):
    accepted_and_rejected_quotes = SellerQuote.objects.filter(author_notified=True) # when this is false it means they haven't been notified yet about being accepted/denied
    accepted_and_rejected_quotes = accepted_and_rejected_quotes.filter(author=request.user)

    quote_notification_count = accepted_and_rejected_quotes.count()

    return JsonResponse({'quote_notification_count':quote_notification_count})


def requestGotQuoteCount(request):
    user_profile = User.objects.get(id=request.user.id)
    user_requests = BuyerRequest.objects.filter(author=user_profile) # get all of this users requests

    quote_list = []
    # get all the quotes, loop through loop through requests, 
    # then see if quote points to the request, if so add it to list
    # then filter the list to see if request_author_notified=False
    
    # FOR NOW JUST SHOW BUYERS WHEN THEY GOT QUOTES
    quotes = SellerQuote.objects.all()
    for quote in quotes:
        for req in user_requests:
            if quote.request == req:
                if quote.buyer_notified == False:
                    quote_list.append(quote) 

    request_got_a_quote_count = len(quote_list)
    return JsonResponse({'request_got_a_quote_count':request_got_a_quote_count})


def inboxCount(request):
    inbox = ChatMessage.objects.filter(reciever=request.user)
    unread_general_inbox = inbox.filter(user_read=False)
    # dont show ones that are quote messages
    unread_general_inbox = unread_general_inbox.filter(quote_regarding__isnull=True)

    inbox_count = unread_general_inbox.count()
    return JsonResponse({'inbox_count':inbox_count})


def quotesInboxCount(request):
    inbox = ChatMessage.objects.filter(reciever=request.user)
    unread_general_inbox = inbox.filter(user_read=False)
    # do show ones that are quote messages
    unread_general_inbox = unread_general_inbox.filter(quote_regarding__isnull=False)

    quote_inbox_count = unread_general_inbox.count()
    return JsonResponse({'quote_inbox_count':quote_inbox_count})
 

 # Ajax grabs the general inbox messages
def unreadGeneralInbox(request):
    # general messages
    inbox = ChatMessage.objects.filter(reciever=request.user)
    my_general_inbox = inbox.filter(user_read=False).order_by('-id')
    print(my_general_inbox)
    
    unread_inbox = [] #list
    for obj in my_general_inbox:
        # get profile photo
        user = User.objects.get(id=obj.sender.id)
        created_at = str(obj.created_at)
        created_at = created_at[:10]
        item = {
            'id': obj.id,
            'sender': user.useralias,
            'created_at': obj.created_at,
            'photo': str(user.profile_photo),
        }
        unread_inbox.append(item) # append dictionary to the list
    return JsonResponse({'unread_inbox':unread_inbox})


# Ajax grabs the sidebar profile photo
def profilePhoto(request):
    profile = User.objects.get(id=request.user.id)
    profile_photo = str(profile.profile_photo)
    profile_photo = '/media/' + profile_photo
    return JsonResponse({'profile_photo':profile_photo})


# Ajax grabs the profile type
def profileType(request):
    profile = User.objects.get(id=request.user.id)
    profile_type = profile.buyer_account
    return JsonResponse({'profile_type':profile_type})

 
 
################################### PROFILE ###################################

def my_profile(request):
    profile = User.objects.get(id=request.user.id)
    selling = profile.selling.all()
    context = {
        'selling':selling,
        'profile':profile,
    }
    return render(request, 'config/my-profile.html', context)


class UserAccountUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'config/edit-profile.html'
    fields = (
    'profile_photo',
    'first_name',
    'last_name',
    'company_name',
    'business_street_address',
    'city',
    'state',
    'zip_code',
    'company_phone_number',
    )
    success_message = 'Your Profile has been updated!'
    success_url = reverse_lazy('my-profile')
 
class UserEmailUpdate(LoginRequiredMixin, SuccessMessageMixin,UpdateView):
    model = User
    template_name = 'config/edit-profile.html'
    fields = (
    'email',
    )
    success_message = 'Your Email has been updated!'
    success_url = reverse_lazy('my-profile')
 

class UserAccountSellingUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'config/edit-selling.html'
    fields = (
    'selling',
    )
    success_message = 'Your selling options have been updated!'
    success_url = reverse_lazy('my-profile')
 

def support_faq(request):
    categories = FaqCat.objects.all()
    faqs = Faq.objects.all()
    context = {
        'categories':categories,
        'faqs':faqs,
    }
    return render(request, 'support/support-faq.html', context)


# the page with the buttons that caches their account type in local storage
def signup_landing(request):
    return render(request, 'registration/signup.html', {})


# Sign Up View
class SignUpBuyerView(View):
    form_class = SignUpBuyerForm
    template_name = 'registration/signup-buyer.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            # try setting buyer_account here:
            user.buyer_account = True
            user.is_active = True
            user.save()
            selling = request.POST.getlist('selling')
            for s in selling:
                user.selling.add(s)
            user.save()

            messages.success(request, ('Welcome to Django Marketplace!'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})


# Sign Up View
class SignUpSellerView(View):
    form_class = SignUpSellerForm
    template_name = 'registration/signup-seller.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = True
            user.save()

            messages.success(request, ('Welcome to Django Marketplace!'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request,"Username or Password is not correct.")
    return render(request, 'registration/login.html',{})

def login_filter_user(request): 
    # called by the global_settings.py & settings.py LOGIN_REDIRECT_URL
    user = User.objects.get(id=request.user.id)

    if user.buyer_account:
        return redirect('requests')
    else:
        return redirect('posts')


def signout(request):
    logout(request)
    return redirect('login')
    
################################### NOTIFICATIONS ###################################
def user_notification_settings(request):
    settings = UserNotificationSettings.objects.get(user=request.user)
    context = {
        'settings':settings,
    }
    return render(request, 'config/notification-settings.html', context)


def toggle_activity_notifications(request):
    settings = UserNotificationSettings.objects.get(user=request.user)
    if settings.notify_activity == True:
        settings.notify_activity = False
        settings.save()
    else:
        settings.notify_activity = True
        settings.save()
    return redirect('notification-settings')


def toggle_support_notifications(request):
    settings = UserNotificationSettings.objects.get(user=request.user)
    if settings.notify_support == True:
        settings.notify_support = False
        settings.save()
    else:
        settings.notify_support = True
        settings.save()
    return redirect('notification-settings')


def toggle_marketing_notifications(request):
    settings = UserNotificationSettings.objects.get(user=request.user)
    if settings.notify_marketing == True:
        settings.notify_marketing = False
        settings.save()
    else:
        settings.notify_marketing = True
        settings.save()
    return redirect('notification-settings')


def toggle_messages_notifications(request):
    settings = UserNotificationSettings.objects.get(user=request.user)
    if settings.notify_messages == True:
        settings.notify_messages = False
        settings.save()
    else:
        settings.notify_messages = True
        settings.save()
    return redirect('notification-settings')
 
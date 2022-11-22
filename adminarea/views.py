from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from adminarea.models import ProspectEmail
from marketplace.models import BuyerRequest, SellerQuote
from website.models import *
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from accounts.models import Faq, FaqCat, UserNotificationSettings
from django.http import JsonResponse
# from django.core.mail import send_mail


################################### AJAX NOTIFICATIONS ###################################

# Ajax grabs the count for notifications
# def referralCount(request):
#     referral_count = 0
#     users = get_user_model().objects.all()
#     # check all users for referrals then count them
#     for user in users:
#         try:
#             profile = get_user_model().objects.get(user=user)
#         except:
#             pass
#         my_recs = profile.get_recommened_profiles()
#         recs_len = len(my_recs)
#         # limit to only show users with referrals
#         if recs_len > 0:
#             # check ReferralPayoutReceipts for the user, count them, check for incongruency of referral count
#             ref_payout_receipts = ReferralPayoutReceipt.objects.filter(user=user)
#             ref_payout_receipts_len = len(ref_payout_receipts)
#             if recs_len > ref_payout_receipts_len:
#                 # append to the list and display in the template
#                 difference = recs_len - ref_payout_receipts_len
#                 referral_count = referral_count + difference
#     return JsonResponse({'referral_count':referral_count})


# def inboxCount(request):
#     unread_support_inbox = SupportTicket.objects.filter(admin_read=False)

#     # inbox2 = SupportTicketResponse.objects.filter(reciever=request.user) # doesnt work
#     # unread_general_inbox = inbox2.filter(user_read=False)
#     unread_support_inbox = SupportTicket.objects.filter(admin_read=False)

#     inbox_count = unread_support_inbox.count() + unread_general_inbox.count()
#     return JsonResponse({'inbox_count':inbox_count})


# # Ajax grabs the support inbox messages
# def unreadTicketInbox(request):
#     inbox = SupportTicket.objects.filter(reciever=request.user)
#     my_support_inbox = inbox.filter(user_read=False).order_by('-id')
#     print(my_support_inbox)

#     unread_inbox = [] #list
#     for obj in my_support_inbox:
#         # get profile photo
#         # profile = get_user_model().objects.get(user=obj.sender)
#         created_at = str(obj.created_at)
#         created_at = created_at[:10]
        
#         # truncate message
#         # obj.msg_content = obj.msg_content[-10]
#         item = {
#             'id': obj.id,
#             'ticket_id': obj.ticket.id,
#             'msg_content': obj.msg_content,
#             'created_at': created_at,
#         }
#         unread_inbox.append(item) # append dictionary to the list

#     return JsonResponse({'unread_inbox':unread_inbox})


#  # Ajax grabs the general inbox messages
# def unreadResponseInbox(request):
#     # ticket responses
#     inbox = SupportTicketResponse.objects.filter(reciever=request.user)
#     my_general_inbox = inbox.filter(user_read=False).order_by('-id')
    
#     unread_inbox = [] #list
#     for obj in my_general_inbox:
#         # get profile photo
#         profile = get_user_model().objects.get(user=obj.sender)
#         created_at = str(obj.created_at)
#         created_at = created_at[:10]
#         item = {
#             'id': obj.id,
#             'sender': obj.sender.username,
#             'created_at': obj.created_at,
#             'photo': str(profile.profile_photo),
#         }
#         unread_inbox.append(item) # append dictionary to the list
#     return JsonResponse({'unread_inbox':unread_inbox})



 

################################### DASHBOARD ###################################
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request): 
   
    user_count = get_user_model().objects.all().count()
    seller_count = get_user_model().objects.filter(buyer_account=False).count()
    buyer_count = get_user_model().objects.filter(buyer_account=True).count()

    # referrals to payout count
    referral_count = 0
    users = get_user_model().objects.all() 

    context = {
        'seller_count':seller_count,
        'buyer_count':buyer_count,
        'user_count':user_count,
    }
    return render(request, 'adminarea/admin-dash.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_account_settings(request):
    profile = get_user_model().objects.get(id=request.get_user_model().id)
    context = {
        'profile':profile
    }
    return render(request, 'adminarea/admin-account-settings.html', context)
 

################################### FAQ ###################################
@user_passes_test(lambda u: u.is_superuser)
def admin_faq_posts(request):
    categories = FaqCat.objects.all()
    faqs = Faq.objects.all()
    faq_insights = Faq.objects.filter(category=1)
    faq_betting = Faq.objects.filter(category=2)
    faq_legal = Faq.objects.filter(category=3)
    context = {
        'faqs':faqs,
        'categories':categories,
        'faq_betting':faq_betting,
        'faq_insights':faq_insights,
        'faq_legal':faq_legal,
    }
    return render(request, 'adminarea/faq/admin-faq-posts.html',context)

class AdminNewFaqPost(LoginRequiredMixin, CreateView):
    model = Faq
    fields = '__all__'
    template_name = 'adminarea/faq/admin-new-faq-post.html'
    success_url = reverse_lazy('admin-faq-posts')

class EditFaqView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Faq
    template_name = 'adminarea/faq/admin-edit-faq-post.html'
    fields = '__all__'
    success_message = 'The FAQ has been updated!'
    success_url = reverse_lazy('admin-faq-posts')

class AdminNewFaqCat(LoginRequiredMixin, CreateView):
    model = FaqCat
    fields = '__all__'
    template_name = 'adminarea/faq/admin-new-faq-cat.html'
    success_url = reverse_lazy('admin-faq-posts')


################################### USERS ###################################

@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    users = get_user_model().objects.all().order_by('-id')
    context = {
        'users':users,
    }
    return render(request, 'adminarea/user/admin-users.html', context)

class EditUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'adminarea/user/admin-edit-get_user_model().html'
    fields = '__all__'
    success_message = 'The User has been updated!'
    success_url = reverse_lazy('admin-users')

@user_passes_test(lambda u: u.is_superuser)
def admin_view_user(request, pk):
    profile = get_user_model().objects.get(id=pk)
    return render(request, 'adminarea/user/admin-view-user.html', {'profile':profile})


################################### MARKETING ###################################
@user_passes_test(lambda u: u.is_superuser)
def admin_leads(request):
    if request.method == "POST":
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        link = request.POST['link']

        new_message = ProspectEmail.objects.create(
            email=email,
            subject=subject,
            message=message,
            link=link,
        )

        # html_message = loader.render_to_string(
        #             'adminarea/emails/lead-gen-email.html',
        #             {
        #                 'message': new_message.message, 
        #                 'link': new_message.link,
        #             }
        #         )

        # send_mail(
        #     new_message.subject,
        #     '',
        #     'support@Marketplace.io', # from_email
        #     [new_message.email], # to_list
        #     fail_silently=False,
        #     html_message=html_message
        # )
        
        # message_sent = True

        # show all sent emails
        sent_emails = ProspectEmail.objects.all()
        return render(request, 'adminarea/admin-leads.html',{'sent_emails':sent_emails,'message_sent':message_sent})
    
    message_sent = False
    # show all sent emails
    sent_emails = ProspectEmail.objects.all()
    return render(request, 'adminarea/admin-leads.html',{'sent_emails':sent_emails,'message_sent':message_sent})
 

################################### REQUESTS ###################################
@user_passes_test(lambda u: u.is_superuser)
def request_list(request):
    buyer_requests = BuyerRequest.objects.all()
    context = {
        'buyer_requests':buyer_requests,
    }
    return render(request, 'adminarea/requests/requests.html',context)

@user_passes_test(lambda u: u.is_superuser)
def request_detail(request,pk):
    buyer_request = BuyerRequest.objects.get(pk=pk)
    quotes = SellerQuote.objects.filter(request=buyer_request)
    context = {
        'quotes':quotes,
        'buyer_request':buyer_request,
    }
    return render(request, 'adminarea/requests/request.html',context)

class DeleteRequestView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = BuyerRequest
    template_name = 'adminarea/requests/delete-request.html'
    success_message = 'The Request has been deleted!'
    success_url = reverse_lazy('admin-requests')


@user_passes_test(lambda u: u.is_superuser)
def request_update(request,pk):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        need_by_date = request.POST["need_by_date"]
        maximum_quotes_desired = request.POST["maximum_quotes_desired"]

        request_to_update = BuyerRequest.objects.get(id=pk)
        request_to_update.description = description
        request_to_update.title = title
        request_to_update.need_by_date = need_by_date
        request_to_update.maximum_quotes_desired = maximum_quotes_desired
        request_to_update.save()

        return redirect('admin-requests')
    
    request_to_update = BuyerRequest.objects.get(id=pk)
    return render(request, 'adminarea/requests/update-request.html', {'request_to_update':request_to_update,})
    

    
################################### QUOTES ###################################
@user_passes_test(lambda u: u.is_superuser)
def quote_list(request):
    quotes = SellerQuote.objects.all()
    context = {
        'quotes':quotes,
    }
    return render(request, 'adminarea/quotes/quotes.html',context)


@user_passes_test(lambda u: u.is_superuser)
def quote_detail(request,pk):
    quote = SellerQuote.objects.get(pk=pk)
    context = {
        'quote':quote,
    }
    return render(request, 'adminarea/quotes/quote.html',context)


class DeleteQuoteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SellerQuote
    template_name = 'adminarea/quotes/delete-quote.html'
    success_message = 'The Quote has been deleted!'
    success_url = reverse_lazy('admin-quotes')


@user_passes_test(lambda u: u.is_superuser)
def quote_update(request,pk):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        expiry_date = request.POST["expiry_date"]

        quote_to_update = SellerQuote.objects.get(id=pk)
        quote_to_update.description = description
        quote_to_update.title = title
        quote_to_update.expiry_date = expiry_date
        quote_to_update.price = price
        quote_to_update.save()

        return redirect('admin-quotes')
    
    quote_to_update = SellerQuote.objects.get(id=pk)
    return render(request, 'adminarea/quotes/update-quote.html', {'quote_to_update':quote_to_update,})


@user_passes_test(lambda u: u.is_superuser)
def admin_search(request):
    query = request.POST["q"]
    profiles = get_user_model().objects.filter(Q(company_name__contains=query) | Q(first_name__contains=query))
    requests = BuyerRequest.objects.filter(Q(title__contains=query) | Q(description__contains=query))
    quotes = SellerQuote.objects.filter(Q(title__contains=query) | Q(description__contains=query))

    context = {
        'profiles':profiles,
        'requests':requests,
        'quotes':quotes,
    }
    return render(request, 'adminarea/admin-search-results.html', context)

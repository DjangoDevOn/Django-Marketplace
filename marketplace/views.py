from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse_lazy
# from django.core.mail import send_mail
from django.template import loader
from django.views.generic import UpdateView, DeleteView
from accounts.models import UserNotificationSettings
from django.contrib.messages.views import SuccessMessageMixin

################################### NOTIFICATIONS ###################################
def dismiss_new_quote_notif(request, pk):
    quote = SellerQuote.objects.get(id=pk)
    quote.buyer_notified = True
    quote.save()
    return redirect('request-details', quote.request.id)


################################### FILTERS ###################################

def most_recent_filter(request):
    most_recent = True
    return render(request, 'marketplace/feed.html', {'most_recent':most_recent})

def quoted_request_filter(request):
    quoted_request = True
    return render(request, 'marketplace/feed.html', {'quoted_request':quoted_request})

def best_matches_filter(request):
    best_matches = True
    return render(request, 'marketplace/feed.html', {'best_matches':best_matches})

def saved_requests_filter(request):
    saved_requests = True
    return render(request, 'marketplace/feed.html', {'saved_requests':saved_requests})

################################### POSTS FEED ###################################
def load_more_posts_most_recent(request, num_posts):  # get num_posts we should display as kwarg from the URL/path
    if request.is_ajax():
        visible = 3 # initially display 3 posts
        upper = num_posts # the number we should show   ex: 9
        lower = upper - visible # lower boundary is upper minus 3 (visible)   ex: 6
        # size = BuyerRequest.objects.all().count()  - option 2: display all BuyerRequests even if under contract
        size = BuyerRequest.objects.filter(in_contract=False).count()

        # for checking if user quoted
        quotes = SellerQuote.objects.all()

        qs = BuyerRequest.objects.filter(in_contract=False)
        data = [] #list
        for obj in qs:
            # see if logged in user already sent a quote, and also check status of quote cap due to template limitation of no "elseif"
            limit_message = ''
            for quote in quotes:
                if quote.request == obj:
                    if quote.request.quote_cap_reached:
                        limit_message = 'Quote Capped'
                if quote.request == obj:
                    if quote.author == request.user:
                        limit_message = 'You Quoted'
                

            item = {
                'id': obj.id,
                'title': obj.title,
                'description': obj.description,
                'author': obj.author.useralias,
                'photo': str(obj.author.profile_photo),
                # Check if the user liked a request or not
                'liked': True if request.user in obj.liked.all() else False,
                'count': obj.like_count,
                'need_by_date': obj.need_by_date,
                'maximum_quotes_desired': obj.maximum_quotes_desired,
                'limit_message':limit_message,

            } #dictionary
            data.append(item)
            # slice the data based on the lower/upper variables
            # include size so you can see: X out of "size"
        return JsonResponse({'data':data[lower:upper], 'size': size})


def load_more_posts_quoted_requests(request, num_posts):  # get num_posts we should display as kwarg from the URL/path
    if request.is_ajax():
        visible = 3 # initially display 3 posts
        upper = num_posts # the number we should show   ex: 9
        lower = upper - visible # lower boundary is upper minus 3 (visible)   ex: 6
        # size = BuyerRequest.objects.all().count()  - option 2: display all BuyerRequests even if under contract
        size = BuyerRequest.objects.filter(author=request.user).count()

        # for checking if user quoted
        quotes = SellerQuote.objects.all()

        qs = BuyerRequest.objects.filter(author=request.user)
        profile = User.objects.get(id=request.user.id)
        data = [] #list
        for obj in qs:
            if obj.quote_cap_reached:
                limit_message = 'Quote Capped'
            # see if logged in user already sent a quote, and also check status of quote cap due to template limitation of no "elseif"
            limit_message = ''
            for quote in quotes:
                # if quote.request == obj:
                if quote.author == request.user:
                    limit_message = 'You Quoted'
                    # add object to the list of Requests this user has quoted
                    item = {
                        'id': obj.id,
                        'title': obj.title,
                        'description': obj.description,
                        'author': obj.author.useralias,
                        'photo': str(obj.author.profile_photo),
                        # Check if the user liked a request or not
                        'liked': True if request.user in obj.liked.all() else False,
                        'count': obj.like_count,
                        'need_by_date': obj.need_by_date,
                        'maximum_quotes_desired': obj.maximum_quotes_desired,
                        'limit_message':limit_message,

                    } #dictionary
                    data.append(item)
                    # slice the data based on the lower/upper variables
                    # include size so you can see: X out of "size"

            
        return JsonResponse({'data':data[lower:upper], 'size': size})
            


def load_more_posts_saved_requests(request, num_posts):  # get num_posts we should display as kwarg from the URL/path
    if request.is_ajax():
        visible = 3 # initially display 3 posts
        upper = num_posts # the number we should show   ex: 9
        lower = upper - visible # lower boundary is upper minus 3 (visible)   ex: 6

         # for checking if user quoted
        quotes = SellerQuote.objects.all()

        qs = BuyerRequest.objects.filter(in_contract=False)
        data = [] #list
        size = 0
        for obj in qs:
             # see if logged in user already sent a quote, and also check status of quote cap due to template limitation of no "elseif"
            limit_message = ''
            for quote in quotes:
                if quote.request == obj:
                    limit_message = 'You Quoted'
            if obj.quote_cap_reached:
                limit_message = 'Quote Capped'
            if request.user in obj.liked.all():
                size +=1
                item = {
                    'id': obj.id,
                    'title': obj.title,
                    'description': obj.description,
                    'author': obj.author.useralias,
                    'photo': str(obj.author.profile_photo),
                    # Check if the user liked a request or not
                    'liked': True if request.user in obj.liked.all() else False,
                    'count': obj.like_count,
                    'need_by_date': obj.need_by_date,
                    'maximum_quotes_desired': obj.maximum_quotes_desired,
                    'limit_message':limit_message,

                } #dictionary
                data.append(item)
            # else:
                # item = {
                #     'none': 'No Requests to display',
                # } #dictionary
                # data.append(item)
                 # add not found variable / alert
            # slice the data based on the lower/upper variables
            # include size so you can see: X out of "size"
        return JsonResponse({'data':data[lower:upper], 'size': size})



def like_unlike_post(request):
    if request.is_ajax():
        pk = request.POST.get('pk') # get the pk/clickedId sent from the ajax call
        obj = BuyerRequest.objects.get(id=pk) # get the post object using the pk
        if request.user in obj.liked.all():
            # if the user is in the list, we should remove the user, because if they clicked again that means they want to "Unlike" the post
            liked = False
            obj.liked.remove(request.user)
        else:
            # they are not on the liked list
            liked = True # because the user must be added to like list of a post
            obj.liked.add(request.user)
        return JsonResponse({'liked':liked, 'count': obj.like_count})


################################### REQUESTS ###################################
def open_requests_filter(request):
    # permissions: only request author can see these
    profile = User.objects.get(id=request.user.id)
    requests = BuyerRequest.objects.filter(author=profile).order_by('-id')
    closed_requests = requests.filter(in_contract=True)
    closed_count = len(closed_requests)
    requests = requests.filter(in_contract=False)
    open = True
    open_count = len(requests)
    # new quote indicator
    new_quotes = SellerQuote.objects.filter(buyer_notified=False)
    # filter the list so it just shows one notification per new quote on the request card
    quotes_list = [] # what the template is getting
    for req in requests:
        counter = 0
        for quote in new_quotes:
            if quote.request == req:
                counter += 1
                if counter < 2:
                    quotes_list.append(quote)
    # new quote message indicator
    inbox = ChatMessage.objects.filter(reciever=request.user)
    unread_general_inbox = inbox.filter(user_read=False)
    # do show ones that are quote messages
    unread_general_inbox = unread_general_inbox.filter(quote_regarding__isnull=False)
    new_messages = []
    all_requests = BuyerRequest.objects.filter(author=profile)
    # filter the list so it just shows one notification per new quote on the request card
    for req in all_requests:
        counter = 0
        for message in unread_general_inbox:
            if message.quote_regarding.request == req:
                counter += 1
                if counter < 2:
                    new_messages.append(message)
    return render(request, 'marketplace/requests.html', {'new_messages':new_messages,'quotes_list':quotes_list,'open_count':open_count,'closed_count':closed_count,'open':open, 'requests':requests,})

def closed_requests_filter(request):
    # permissions: only request author can see these
    profile = User.objects.get(id=request.user.id)
    requests = BuyerRequest.objects.filter(author=profile).order_by('-id')
    open_requests = requests.filter(in_contract=False)
    open_count = len(open_requests)
    requests = requests.filter(in_contract=True)
    closed = True
    closed_count = len(requests)
    # new quote indicator
    new_quotes = SellerQuote.objects.filter(buyer_notified=False)
    # filter the list so it just shows one notification per new quote on the request card
    quotes_list = [] # what the template is getting
    for req in requests:
        counter = 0
        for quote in new_quotes:
            if quote.request == req:
                counter += 1
                if counter < 2:
                    quotes_list.append(quote)
    # new quote message indicator
    inbox = ChatMessage.objects.filter(reciever=request.user)
    unread_general_inbox = inbox.filter(user_read=False)
    # do show ones that are quote messages
    unread_general_inbox = unread_general_inbox.filter(quote_regarding__isnull=False)
    new_messages = []
    # filter the list so it just shows one notification per new quote on the request card
    all_quotes = SellerQuote.objects.filter(author=request.user)
    for quote in all_quotes:
        counter = 0
        for message in unread_general_inbox:
            if message.quote_regarding == quote:
                counter += 1
                if counter < 2:
                    new_messages.append(message)
    return render(request, 'marketplace/requests.html', {'new_messages':new_messages,'quotes_list':quotes_list,'open_count':open_count,'closed_count':closed_count,'closed':closed, 'requests':requests,})


def new_request(request):
    # check if user is a buyer and if not - redirect
    current_user = User.objects.get(id=request.user.id)
    if current_user.buyer_account == False:
        return redirect('quotes')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        need_by_date = request.POST.get('need_by_date')
        maximum_quotes_desired = request.POST.get('maximum_quotes_desired')
        attachments = request.FILES.getlist('attachments')

        # "Expiry date cannot be in the past" validator
        alert = ''
        from datetime import datetime, date
        need_by_date = datetime.strptime(need_by_date, '%Y-%m-%d')
        if need_by_date < datetime.today():
            alert = 'Your Request\'s "Need By Date" cannot be in the past!'
            return render(request, 'marketplace/new-request.html',{'alert':alert,})

        # "Quote Cap" cannot be a zero or negative number validator
        alert = ''
        if int(maximum_quotes_desired) < 1:
            alert = 'Your Request\'s "Quote Cap" cannot be a zero or negative number !'
            return render(request, 'marketplace/new-request.html',{'alert':alert,})

        user_profile = User.objects.get(id=request.user.id)

        new_request = BuyerRequest.objects.create(
            title=title,
            description=description,
            need_by_date=need_by_date,
            maximum_quotes_desired=maximum_quotes_desired,
            author=user_profile,
        )

        for attachment in attachments:
            new_attachment = RequestAttachment.objects.create(
                buyer_request=new_request,
                attachment=attachment,
            )
        alert = 'You successfully created a new Request!'
        return render(request, 'marketplace/new-request.html',{'alert':alert})
    
    return render(request, 'marketplace/new-request.html',{})
 


def edit_request(request, pk):
    if request.method == 'POST':
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

        return redirect('requests')
        
    editing_request = BuyerRequest.objects.get(id=pk)
    return render(request, 'marketplace/edit-request.html', {'editing_request':editing_request})

# hides the quote on the req details page for the author of the request
def hide_quote(request, pk):
    quote = SellerQuote.objects.get(id=pk)
    quote.buyer_hidden = True
    quote.buyer_notified = True # also remove notification
    quote.save()
    return redirect('request-details', quote.request.id)

# show all hidden quotes
def hidden_quotes(request):
    quotes = SellerQuote.objects.filter(buyer_hidden=True)
    req = quotes[0].request
    return render(request, 'marketplace/hidden-quotes.html', {'req':req,'quotes':quotes,})


def request_details(request, pk):
    # permissions: only request's quote recipient author can view
    if request.method == 'POST':
        respond_to_user = request.POST["user"]
        respond_to_user = get_user_model().objects.get(useralias=respond_to_user)
        request_regarding = BuyerRequest.objects.get(id=pk)
        return render(request, 'marketplace/message-respond.html', {'respond_to_user':respond_to_user, 'request_regarding':request_regarding})

    # Permissions DONE IN TEMPLATE INSTEAD
    request_details = BuyerRequest.objects.get(id=pk)
    # my_profile = User.objects.get(id=request.user.id)
    # if request_details.author != my_profile:
    #     return redirect('requests')
     
    quotes = SellerQuote.objects.filter(request=request_details)
    # if theres multiple message with the same sender in the queryset then pass
    # otherwise add it to "messages", this shows just one message icon if theres a thread 
    # about this quote
    all_msg = ChatMessage.objects.all()
    messages = []
    for quote in quotes:
        counter = 0
        for message in all_msg:
            # count num of messages with that quote regarding
            if message.quote_regarding == quote:
                counter += 1
                if counter < 2:
                    messages.append(message)
        
    quote_accepted = ''
    for quote in quotes:
        if quote.accepted:
            quote_accepted = quote

    # get the attachments for the request
    attachments = RequestAttachment.objects.filter(buyer_request=request_details)
    # get all profiles for the profile info 
    profiles = User.objects.all()
    return render(request, 'marketplace/request-details.html', {'messages':messages,'profiles':profiles,'attachments':attachments,'quote_accepted':quote_accepted, 'messages':messages,'quotes':quotes, 'request_details':request_details})


################################### QUOTES ###################################



class EditQuoteView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SellerQuote
    template_name = 'marketplace/edit-quote.html'
    fields = (
            'title', 
            'description', 
            'price', 
            )
    success_message = 'Your Quote has been updated!'
    success_url = reverse_lazy('quotes')


def accepted_quotes_filter(request):
    # permissions: only quote user can see these
    quotes = SellerQuote.objects.filter(author=request.user).order_by('-id')
    quotes = quotes.filter(accepted=True)
    accepted = True
    accepted_count = len(quotes)
    # new quote message indicator
    inbox = ChatMessage.objects.filter(reciever=request.user)
    unread_general_inbox = inbox.filter(user_read=False)
    # do show ones that are quote messages
    unread_general_inbox = unread_general_inbox.filter(quote_regarding__isnull=False)
    new_messages = []
    # filter the list so it just shows one notification per new quote on the request card
    all_quotes = SellerQuote.objects.filter(author=request.user)
    for quote in all_quotes:
        counter = 0
        for message in unread_general_inbox:
            if message.quote_regarding == quote:
                counter += 1
                if counter < 2:
                    new_messages.append(message)
    return render(request, 'marketplace/quotes.html', {'new_messages':new_messages,'accepted_count':accepted_count,'accepted':accepted, 'quotes':quotes,})

def rejected_quotes_filter(request):
    # permissions: only quote user can see these
    quotes = SellerQuote.objects.filter(author=request.user).order_by('-id')
    quotes = quotes.filter(rejected=True)
    rejected = True
    rejected_count = len(quotes)
    # new quote message indicator
    inbox = ChatMessage.objects.filter(reciever=request.user)
    unread_general_inbox = inbox.filter(user_read=False)
    # do show ones that are quote messages
    unread_general_inbox = unread_general_inbox.filter(quote_regarding__isnull=False)
    new_messages = []
    # filter the list so it just shows one notification per new quote on the request card
    all_quotes = SellerQuote.objects.filter(author=request.user)
    for quote in all_quotes:
        counter = 0
        for message in unread_general_inbox:
            if message.quote_regarding == quote:
                counter += 1
                if counter < 2:
                    new_messages.append(message)
    return render(request, 'marketplace/quotes.html', {'new_messages':new_messages,'rejected_count':rejected_count,'rejected':rejected, 'quotes':quotes,})

def open_quotes_filter(request):
    # permissions: only quote user can see these
    quotes = SellerQuote.objects.filter(author=request.user).order_by('-id')
    quotes = quotes.filter(rejected=False)
    open = True
    open_count = len(quotes)
    # new quote message indicator
    inbox = ChatMessage.objects.filter(reciever=request.user)
    unread_general_inbox = inbox.filter(user_read=False)
    # do show ones that are quote messages
    unread_general_inbox = unread_general_inbox.filter(quote_regarding__isnull=False)
    new_messages = []
    # filter the list so it just shows one notification per new quote on the request card
    all_quotes = SellerQuote.objects.filter(author=request.user)
    for quote in all_quotes:
        counter = 0
        for message in unread_general_inbox:
            if message.quote_regarding == quote:
                counter += 1
                if counter < 2:
                    new_messages.append(message)
    return render(request, 'marketplace/quotes.html', {'new_messages':new_messages,'open_count':open_count,'open':open, 'quotes':quotes,})


def new_quote(request, pk):
    # check if user is a buyer and if so - redirect
    current_user = User.objects.get(id=request.user.id)
    if current_user.buyer_account == True:
        return redirect('requests')
    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        expiry_date = request.POST.get('expiry_date')
        attachments = request.FILES.getlist('attachments')
        buyer_request = BuyerRequest.objects.get(id=pk)

        # "Expiry date cannot be in the past" validator
        alert = ''
        from datetime import datetime, date
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')
        if expiry_date < datetime.today():
            # raise forms.ValidationError("The date cannot be in the past!")
            alert = 'Your Quote\'s "Expiry Date" cannot be in the past!'
            # return redirect('new-quote', pk)
            return render(request, 'marketplace/new-quote.html',{'alert':alert,'buyer_request':buyer_request})

        # before making the new quote, check if seller already has
        alert = ''
        quotes_list = SellerQuote.objects.filter(request=buyer_request)
        for quote in quotes_list:
            if quote.author == request.user:
                alert = 'You already sent a quote to this Request!'
                return render(request, 'marketplace/new-quote.html',{'alert':alert,'buyer_request':buyer_request})
        
        # Last step before making the new quote, check if the request has the max quotes 
        # Make the quote 
        # Toggle quote_cap_reached if so
        quotes = SellerQuote.objects.all()
        requests = BuyerRequest.objects.all()
        alert = ''
        if buyer_request.quote_cap_reached:
            alert = 'Sorry but the quote cap has been reached for this request!'
            return render(request, 'marketplace/new-quote.html',{'alert':alert,'buyer_request':buyer_request})
        
        new_quote = SellerQuote.objects.create(
            author=request.user,
            title=title,
            description=description,
            price=price,
            expiry_date=expiry_date,
            request=buyer_request,
            # attachment=attachment,
        )

        for request in requests:
            count = 0 # for each request we count the quotes pointing to it
            for quote in quotes:
                if quote.request == buyer_request: # if the quotes request points to this one we're trying to make a quote referencing then:
                    count += 1
                    if count == buyer_request.maximum_quotes_desired: # if the count is more than the max quotes desired at any point then toggle the field in the request
                        buyer_request.quote_cap_reached = True
                        buyer_request.save()

        author = User.objects.get(id=buyer_request.author.id)
        # check notification settings and send email if True
        # gets the settings for the author of the Request we're quoting
        # try:
        #     user_settings = UserNotificationSettings.objects.get(user=author)
        #     if user_settings.notify_activity == True:
        #         html_message = loader.render_to_string(
        #                     'marketplace/emails/request-activity-email.html',
        #                     {
        #                         'message': 'Quote: ' + new_quote.title + ' Request: ' + buyer_request.title, 
        #                         'quote_id': new_quote.id,
        #                     }
        #                 )
                
        #         send_mail(
        #             'Your Request recieved a Quote on Marketplace!',
        #             '',
        #             'support@Marketplace.io', # from_email
        #             [author.email], # to_list
        #             fail_silently=False,
        #             html_message=html_message
        #         )
        # except:
        #     pass

        for attachment in attachments:
            new_attachment = QuoteAttachment.objects.create(
                seller_quote=new_quote,
                attachment=attachment,
            )

        # check quote cap
        if len(quotes_list) >= int(buyer_request.maximum_quotes_desired):
            buyer_request.quote_cap_reached = True
            buyer_request.save()
            
        new_quote.save()

        alert = 'You successfully created a new Quote!'
        # return render(request, 'marketplace/new-quote.html',{'alert':alert,'buyer_request':buyer_request})
        return redirect('quotes')
    buyer_request = BuyerRequest.objects.get(id=pk)
    return render(request, 'marketplace/new-quote.html',{'buyer_request':buyer_request})



def accept_quote(request):
    quote_id = request.POST["quote_id"]
    quote = SellerQuote.objects.get(id=quote_id)
    quote.accepted = True
    quote.save()

    # check notification settings and send email if True
    # try:
    #     user_settings = UserNotificationSettings.objects.get(user=quote.author)
    #     if user_settings.notify_activity == True:
    #         html_message = loader.render_to_string(
    #                     'marketplace/emails/quote-activity-email.html',
    #                     {
    #                         'message': 'Quote: ' + quote.title, 
    #                         'quote_id': quote.id
    #                     }
    #                 )
            
    #         send_mail(
    #             'Your Quote was accepted on Marketplace!',
    #             '',
    #             'support@Marketplace.io', # from_email
    #             [quote.author.email], # to_list
    #             fail_silently=False,
    #             html_message=html_message
    #         )
    # except:
    #     pass


    # update the BuyerRequest object
    buyer_request = BuyerRequest.objects.get(id=quote.request.id)
    buyer_request.in_contract = True
    buyer_request.save()

    # add rejected = True to all quotes for this request
    quotes = SellerQuote.objects.all()
    for quote in quotes:
        if quote.request == buyer_request:
            # exclude the accepted one
            if quote.accepted:
                pass
            else:
                quote.rejected = True
                quote.save()
                # now notify all users that were rejected
                new_notification = QuoteRejectedNotification.objects.create(
                    user=quote.author,
                    seller_quote=quote,
                )

    return redirect("my-closed-requests-filter")


def reject_quote(request):
    quote_id = request.POST["quote_id"]
    quote = SellerQuote.objects.get(id=quote_id)
    quote.accepted = False
    quote.rejected = True
    quote.save()

    # check notification settings and send email if True
    # user_settings = UserNotificationSettings.objects.get(user=quote.author)
    # if user_settings.notify_activity == True:
    #     html_message = loader.render_to_string(
    #                 'marketplace/emails/quote-activity-email.html',
    #                 {
    #                     'message': 'Quote: ' + quote.title, 
    #                     'quote_id': quote.id
    #                 }
    #             )
        
    #     send_mail(
    #         'Your Quote was rejected on Marketplace!',
    #         '',
    #         'support@Marketplace.io', # from_email
    #         [quote.author.email], # to_list
    #         fail_silently=False,
    #         html_message=html_message
    #     )

    return redirect("requests")



# convert this to ajax later to avoid page reload
def remove_quote_notification(request, pk):
    quote_notification = QuoteRejectedNotification.objects.get(id=pk)
    quote_notification.recieved = True
    quote_notification.save()
    return redirect("quotes")



 
def quote_details(request, pk):
    # permissions: only quote user or recipient of quote to a request can view, (two steps)
    if request.method == 'POST':
        quote = SellerQuote.objects.get(id=pk)
        msg = request.POST["message"]

        # mark all messages from this thread as read if they are sent to this user
        quote_details = SellerQuote.objects.get(id=pk)
        messages = ChatMessage.objects.filter(quote_regarding=quote_details) # message about this quote
        messages = messages.filter(reciever=request.user) # for this user
        messages = messages.filter(user_read=False) # that are "unread"
        for message in messages: # mark all of these as "read"
            message.user_read = True
            message.save()


        if request.user != quote.author: 
            new_msg = ChatMessage.objects.create(
                            sender=request.user,
                            reciever=quote.author, #if i'm not the author of the quote
                            msg_content=msg,
                            quote_regarding=quote,
                        )
        else: 
            new_msg = ChatMessage.objects.create(
                            sender=request.user,
                            reciever=quote.request.author, # otherwise the request author's user is the respond to user
                            msg_content=msg,
                            quote_regarding=quote,
                        )
            
    # Permissions (two steps
    # is current user the author
    quote_details = SellerQuote.objects.get(id=pk)
    author_profile = User.objects.get(id=quote_details.request.author.id) #profile of user who wrote original request
    if quote_details.author != request.user:
        if quote_details.request.author != author_profile:
            return redirect('posts')
     
    
    quotes = SellerQuote.objects.filter(request=quote_details.request)
    messages = ChatMessage.objects.filter(quote_regarding=quote_details)
    
    current_user_profile = User.objects.get(id=request.user.id)
    user_is_buyer = current_user_profile.buyer_account
    
    buyer_request = BuyerRequest.objects.get(id=quote_details.request.id)
    quote_accepted = buyer_request.in_contract

    # get the attachments for the quote
    attachments = QuoteAttachment.objects.filter(seller_quote=quote_details)
    # get all profiles for the profile info 
    profile = User.objects.get(id=quote_details.author.id)
    
    # remove notification of new quote for your request if request author is opening request details
    quote_details.buyer_notified = True
    quote_details.save()
    return render(request, 'marketplace/quote-details.html', {'profile':profile,'attachments':attachments,'quote_accepted':quote_accepted, 'user_is_buyer':user_is_buyer,'messages':messages,'quotes':quotes, 'quote_details':quote_details})



################################### MESSAGES ###################################
def message_search(request):
    query = request.POST["q"]

    queryset = ChatMessage.objects.filter(Q(msg_content__contains=query)) # .distinct()

    context = {
        'queryset':queryset,
        'query':query,
    }
    return render(request, 'marketplace/message-search-results.html', context)



def messages(request):
    if request.method == 'POST':
        msg = request.POST["message"]
        respond_to_user_id = request.POST["respond_to_user"]
        respond_to_user = get_user_model().objects.get(id=respond_to_user_id)
            
        new_msg = ChatMessage.objects.create(
                            sender=request.user,
                            reciever=respond_to_user,
                            msg_content=msg,
                        )

    all_messages = ChatMessage.objects.all()
    user_list = []
    for message in all_messages:
        if message.sender == request.user:
            user_list.append(message.reciever) # if i sent it, show the recievers username
        if message.reciever == request.user:
            user_list.append(message.sender)# if i recieved it, show the senders username

    # make the user_list unique
    res = []
    for i in user_list:
        if i not in res:
            res.append(i)
    user_list = res
    # future option, try: user_list = {c.sender for c in ChatMessage.objects.exclude(sender=request.user).select_related('sender')}

    try:
        focused_user = list(user_list)[0]
    except:
        focused_user = ''

    # unread message count for each sidebar of messages
    unread_message_dict = []
    inbox = ChatMessage.objects.filter(reciever=request.user)
    unread_inbox = inbox.filter(user_read=False)
    users = get_user_model().objects.all()
    for user in users:
        count = 0
        for message in unread_inbox:
            # for each sender we should count and add that to the count
            if message.sender == user:
                count += 1
        unread_message_dict.append(
            {
            'count' : count, # how many messages does user have
            'user' : user, # for this sender/user
            }
        )

    return render(request, 'marketplace/messages.html', {'unread_message_dict':unread_message_dict,'focused_user':focused_user, 'user_list':user_list,'all_messages':all_messages, 'request_details':request_details})


# almost the exact same as the above view
def message_filter(request, pk):
    if request.method == 'POST':
        msg = request.POST["message"]
        respond_to_user_id = request.POST["respond_to_user"]
        respond_to_user = get_user_model().objects.get(id=respond_to_user_id)
            
        new_msg = ChatMessage.objects.create(
                            sender=request.user,
                            reciever=respond_to_user,
                            msg_content=msg,
                        )

    all_messages = ChatMessage.objects.all()
    user_list = []
    for message in all_messages:
        if message.sender == request.user:
            user_list.append(message.reciever) # if i sent it, show the recievers username
        if message.reciever == request.user:
            user_list.append(message.sender)# if i recieved it, show the senders username

    # make the user_list unique
    res = []
    for i in user_list:
        if i not in res:
            res.append(i)
    user_list = res
    # future option, try: user_list = {c.sender for c in ChatMessage.objects.exclude(sender=request.user).select_related('sender')}
    
    focused_user = get_user_model().objects.get(id=pk)

    # toggle user_read to True on all messges
    messages_to_toggle = ChatMessage.objects.filter(reciever=request.user)
    messages_to_toggle = messages_to_toggle.filter(sender=focused_user)
    for message in messages_to_toggle:
        message.user_read = True
        message.save()

     # unread message count for each sidebar of messages
    unread_message_dict = []
    inbox = ChatMessage.objects.filter(reciever=request.user)
    unread_inbox = inbox.filter(user_read=False)
    users = get_user_model().objects.all()
    for user in users:
        count = 0
        for message in unread_inbox:
            # for each sender we should count and add that to the count
            if message.sender == user:
                count += 1
        unread_message_dict.append(
            {
            'count' : count, # how many messages does user have
            'user' : user, # for this sender/user
            }
        )
    return render(request, 'marketplace/messages.html', {'unread_message_dict':unread_message_dict,'focused_user':focused_user, 'user_list':user_list,'all_messages':all_messages, 'request_details':request_details})



class EditMessageView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ChatMessage
    template_name = 'marketplace/edit-message.html'
    fields = (
            'msg_content', 
            )
    success_message = 'Your Message has been updated!'
    success_url = reverse_lazy('messages')


class DeleteMessageView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ChatMessage
    template_name = 'marketplace/delete-message.html'
    success_message = 'Your Message has been deleted!'
    success_url = reverse_lazy('messages')


def message_detail(request, pk):
    message = ChatMessage.objects.get(id = pk)
    profile = User.objects.get(user=message.sender)

    user_object = get_user_model().objects.get(useralias=request.user.useralias)
    user_profile = User.objects.get(user=user_object)
    return render(request, 'marketplace/message-detail.html', {'user_profile': user_profile, 'profile':profile,'message':message})


  
def new_message(request, pk):
    if request.method == 'POST':

        msg = request.POST["message"]
        
        original_request = BuyerRequest.objects.get(id=pk)
        reciever = original_request.author

        # try catch in case sender is reciever
        try:
            new_msg = ChatMessage.objects.create(
                            sender=request.user,
                            reciever=reciever,
                            msg_content=msg,
                            request_regarding=original_request,
                        )
        except:
            return redirect('posts')

        # try:
        #     user_settings = UserNotificationSettings.objects.get(user=reciever)
        #     if user_settings.notify_messages == True:
        #         created_at = str(new_msg.created_at)
        #         created_at = created_at[:10]
        #         html_message = loader.render_to_string(
        #                     'marketplace/emails/messages-activity-email.html',
        #                     {
        #                         'message': 'Message Content: ' + new_msg.msg_content + ' Sent: ' + created_at + ' From: ' + new_msg.reciever.useralias, 
        #                         'message_id': new_msg.id,
        #                     }
        #                 )
                
        #         send_mail(
        #             'You got a message on Marketplace!',
        #             '',
        #             'support@Marketplace.io', # from_email
        #             [reciever.email], # to_list
        #             fail_silently=False,
        #             html_message=html_message
        #         )
        # except:
        #     pass
            
        return redirect('messages')
    og_request = pk
    return render(request, 'marketplace/new-message.html', {'og_request':og_request})

    
def respond_message(request):
    msg = request.POST["message"]
    id = request.POST["message_id"]
    request_regarding_id = request.POST["request_regarding"]
    request_regarding = BuyerRequest.objects.get(id=request_regarding_id)

    # get the message that's being responded to and find reciever
    og_message = ChatMessage.objects.get(id=id)

    new_msg = ChatMessage.objects.create(
                        sender=request.user,
                        reciever=og_message.sender,
                        msg_content=msg,
                        request_regarding=request_regarding,
                    )

    # try:
    #     user_settings = UserNotificationSettings.objects.get(user=og_message.sender)
    #     if user_settings.notify_messages == True:
    #         created_at = str(new_msg.created_at)
    #         created_at = created_at[:10]
    #         html_message = loader.render_to_string(
    #                     'marketplace/emails/messages-activity-email.html',
    #                     {
    #                         'message': 'Message Content: ' + new_msg.msg_content + ' Sent: ' + created_at, 
    #                         'message_id': new_msg.id,
    #                     }
    #                 )
            
    #         send_mail(
    #             'Your got a message on Marketplace!',
    #             '',
    #             'support@Marketplace.io', # from_email
    #             [og_message.sender.email], # to_list
    #             fail_silently=False,
    #             html_message=html_message
    #         )
    # except:
    #     pass
        
    return redirect('messages')
    

def message_user(request):
    quote_id = request.POST["quote_id"]
    quote_request_author_id = request.POST["quote_request_author_id"]
    quote = SellerQuote.objects.get(id=quote_id)
    quote_request = quote.request
    request_details = BuyerRequest.objects.get(id=quote_request.id)
    # get the attachments for the request
    attachments = RequestAttachment.objects.filter(buyer_request=request_details)
    return render(request, "marketplace/new-message-to-user.html", {'attachments':attachments,'request_details':request_details,'quote_id':quote_id,'quote_request_author_id':quote_request_author_id})


def send_message_user(request):
    quote_id = request.POST["quote_id"]
    quote_request_author_id = request.POST["quote_request_author_id"]
    msg = request.POST["message"]
    
    quote = SellerQuote.objects.get(id=quote_id)
    quote_request_author_id = int(quote_request_author_id)
    reciever = get_user_model().objects.get(id=quote_request_author_id)
    
    new_msg = ChatMessage.objects.create(
                        sender = request.user,
                        reciever = reciever,
                        msg_content=msg,
                        quote_regarding=quote,
                    )
    
    # try:
    #     user_settings = UserNotificationSettings.objects.get(user=reciever)
    #     if user_settings.notify_messages == True:
    #         created_at = str(new_msg.created_at)
    #         created_at = created_at[:10]
    #         html_message = loader.render_to_string(
    #                     'marketplace/emails/messages-activity-email.html',
    #                     {
    #                         'message': 'Message Content: ' + new_msg.msg_content + ' Sent: ' + created_at, 
    #                         'message_id': new_msg.id,
    #                     }
    #                 )
            
    #         send_mail(
    #             'Your got a Quote related message on Marketplace!',
    #             '',
    #             'support@Marketplace.io', # from_email
    #             [reciever.email], # to_list
    #             fail_silently=False,
    #             html_message=html_message
    #         )
    # except:
    #     pass

    return redirect("requests")



def respond_request_msg(request):
    msg = request.POST["message"]
    respond_to_user_id = request.POST["respond_to_user"]
    respond_to_user = get_user_model().objects.get(id=respond_to_user_id)

    request_regarding_id = request.POST["request_regarding"]
    request_regarding = BuyerRequest.objects.get(id=request_regarding_id)

    new_msg = ChatMessage.objects.create(
                        sender=request.user,
                        reciever=respond_to_user,
                        msg_content=msg,
                        request_regarding=request_regarding,
                    )

    # try:
    #     user_settings = UserNotificationSettings.objects.get(user=respond_to_user)
    #     if user_settings.notify_messages == True:
    #         created_at = str(new_msg.created_at)
    #         created_at = created_at[:10]
    #         html_message = loader.render_to_string(
    #                     'marketplace/emails/messages-activity-email.html',
    #                     {
    #                         'message': 'Message Content: ' + new_msg.msg_content + ' Sent: ' + created_at, 
    #                         'message_id': new_msg.id,
    #                     }
    #                 )
            
    #         send_mail(
    #             'Your got a message on Marketplace!',
    #             '',
    #             'support@Marketplace.io', # from_email
    #             [respond_to_user.email], # to_list
    #             fail_silently=False,
    #             html_message=html_message
    #         )
    # except:
    #     pass

    return redirect('requests')

 

################################### SEARCH ###################################
def general_search_requests(request):
    query = request.POST["q"]

    requests = BuyerRequest.objects.filter(Q(title__contains=query) | Q(description__contains=query)) # .distinct()

    context = {
        'requests':requests,
        'query':query,
    }
    return render(request, 'marketplace/request-search-results.html', context)


def general_search_quotes(request):
    query = request.POST["q"]

    quotes = []
    all_quotes = SellerQuote.objects.filter(Q(title__contains=query) | Q(description__contains=query)) # .distinct()
    # filter quotes to only show quotes for your requests
    profile = User.objects.get(id=request.user.id)
    all_requests = BuyerRequest.objects.filter(author=profile) # get user requests

    for req in all_requests:
        for quo in all_quotes:
            if quo.request == req:
                quotes.append(quo)

    context = {
        'quotes':quotes,
        'query':query,
    }
    return render(request, 'marketplace/quote-search-results.html', context)


################################### NOTIFICATIONS ###################################
def message_read(request, pk): 
    message = ChatMessage.objects.get(id=pk)
    message.user_read = True
    message.save()
    return redirect('messages')

# def ticket_read(request, pk):
#     ticket = SupportTicketResponse.objects.get(id=pk)
#     ticket.user_read = True
#     ticket.save()
#     return redirect('messages')
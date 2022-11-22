from django.core.mail import send_mail
from django.shortcuts import render
from marketplace.models import BuyerRequest
from .models import *
 
################################### WEBSITE ###################################
def index(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        new_msg = ContactForm.objects.create(
            name=name,
            email=email,
            message=message,
        )

        # send_mail(
        #         'You got a Contact Form Submission on Marketplace!',
        #         'From: ' + name + ' Email: ' + email + ' Message: ' + message,
        #         'support@Marketplace.io', # from_email
        #         ['network.connect@protonmail.com'], # to_list
        #         fail_silently=False
        #     )
        requests = BuyerRequest.objects.all()[:8]
        alert = 'Your message has been sent to our team!'
        return render(request, 'website/index.html', {'alert':alert,'requests':requests})
    
    
    # posts = Post.objects.all()[:3]
    requests = BuyerRequest.objects.all()[:8]
    return render(request, 'website/index.html', {'requests':requests})
 
 
################################### ERROR PAGES ###################################
def custom_error_404(request, exception):
    return render(request, 'website/404.html', {})

def custom_error_500(request):
    return render(request, 'website/500.html', {})

def custom_error_403(request, exception):
    return render(request, 'website/403.html', {})

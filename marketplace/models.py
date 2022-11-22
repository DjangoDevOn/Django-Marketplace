from django.db import models
from django.urls import NoReverseMatch
from datetime import datetime
from django.conf import settings

################################### REQUEST ###################################
class BuyerRequest(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="request_author", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    need_by_date = models.DateField(auto_now_add=False)
    maximum_quotes_desired = models.IntegerField()
    quote_cap_reached = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL)
    updated = models.DateTimeField(auto_now=True)
    in_contract = models.BooleanField(default=False)
    author_notified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    @property
    def like_count(self):
        return self.liked.all().count()

    @property
    def quotes_recieved(self):
        return self.sellerquote_set.all().count()

    # Order posts class method - works automatically
    class Meta:
        ordering = ("-created",)


class RequestAttachment(models.Model):
    buyer_request = models.ForeignKey(BuyerRequest, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to ='buyer_request_attachments/')
    
    def __str__(self):
        return str(self.attachment)
 

################################### QUOTE ###################################
class SellerQuote(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="seller_quote_user", on_delete=models.CASCADE)
    request = models.ForeignKey(BuyerRequest, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    expiry_date =models.DateField(auto_now_add=True)
    created =models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    author_notified = models.BooleanField(default=False) # used for reject/accept
    buyer_notified = models.BooleanField(default=False) # used to let buyer/request author know they got a quote
    buyer_hidden = models.BooleanField(default=False) # used to let buyer/request author hide forever

    def __str__(self):
        return self.title

class QuoteAttachment(models.Model):
    seller_quote = models.ForeignKey(SellerQuote, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to ='seller_quote_attachments/')
    
    def __str__(self):
        return str(self.attachment)


class QuoteRejectedNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="quoterejectednotification", on_delete=models.CASCADE)
    seller_quote = models.ForeignKey(SellerQuote, on_delete=models.CASCADE)
    recieved = models.BooleanField(default=False)    

    def __str__(self):
        return str(self.seller_quote.title)


################################### MESSAGE ###################################
class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sender", on_delete=models.CASCADE)
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reciever", on_delete=models.CASCADE)
    msg_content = models.CharField(max_length=5000)
    created_at = models.DateTimeField(default=datetime.now)
    request_regarding = models.ForeignKey(BuyerRequest, on_delete=models.CASCADE, null=True, blank=True)
    quote_regarding = models.ForeignKey(SellerQuote, on_delete=models.CASCADE, null=True, blank=True)
    user_read = models.BooleanField(default=False)

    def __str__(self):
        return self.msg_content

    def save(self, *args, **kwargs):
        if self.sender == self.reciever:
            raise NoReverseMatch()
        super().save(*args, **kwargs)




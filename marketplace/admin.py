from django.contrib import admin
from .models import *

admin.site.register(BuyerRequest)
admin.site.register(SellerQuote)
admin.site.register(ChatMessage) 

admin.site.register(RequestAttachment)
admin.site.register(QuoteAttachment)

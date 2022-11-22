from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin-dash/', admin_dashboard, name='admin-dash'),
    path('admin-search/', admin_search, name='admin-search'),
    path("admin-account/", admin_account_settings, name="admin-account"),
    path("admin-leads/", admin_leads, name="admin-leads"),
    # dynamic faq
    path("admin-new-faq-post/", AdminNewFaqPost.as_view(), name="admin-new-faq-post"),
    path("admin-edit-faq-post/edit/<int:pk>/", EditFaqView.as_view(), name="admin-edit-faq-post"),
    path("admin-faq-posts/", admin_faq_posts, name="admin-faq-posts"),
    path("admin-new-faq-cat/", AdminNewFaqCat.as_view(), name="admin-new-faq-cat"),
    # crud / verify users
    path("admin-users/", admin_users, name="admin-users"),
    path("admin-edit-user/edit/<int:pk>/", EditUserView.as_view(), name="admin-edit-user"),
    path("admin-view-user/<int:pk>/", admin_view_user, name="admin-view-user"),
    # requests
    path('admin-requests/', request_list, name="admin-requests"),
    path("admin-request/<int:pk>/", request_detail, name="admin-request"),
    path('admin-request-delete/<int:pk>/', DeleteRequestView.as_view(), name="admin-request-delete"),
    path('admin-request-update/<int:pk>/', request_update, name="admin-request-update"),
    # quotes
    path("admin-quotes/", quote_list, name="admin-quotes"),
    path("admin-quote/<int:pk>/", quote_detail, name="admin-quote"),
    path("admin-quote-delete/<int:pk>/", DeleteQuoteView.as_view(), name="admin-quote-delete"),
    path("admin-quote-update/<int:pk>/", quote_update, name="admin-quote-update"),
]

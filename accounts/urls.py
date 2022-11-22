from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views # For reset password


urlpatterns = [
    # form to reset email
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password/forgot-password.html"), name="reset_password"),
    # email link success message
    path('reset_password-sent/', auth_views.PasswordResetDoneView.as_view(template_name="password/password-reset-sent.html"), name="password_reset_done"),
    # link to reset password form in email
    path('password_change/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password-reset-form.html"), name="password_reset_confirm"),
    # password successfully changed message
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password/password-reset-done.html"), name="password_reset_complete"),
    # signup / referral stuff
    path('signup/', signup_landing, name='signup'),
    path('buyer-signup/', SignUpBuyerView.as_view(), name='buyer-signup'),
    path('seller-signup/', SignUpSellerView.as_view(), name='seller-signup'), # use both url names to gather the info using JS cookie
    path("login/", signin, name="login"),
    path("signin-filter-user/", login_filter_user, name="signin-filter-user"),
    path("signout/", signout, name="signout"),
    # ajax sidebar grab profile photo
    path('profile-photo/', profilePhoto, name="profile-photo"),
    # ajax grab profile type
    path('profile-type/', profileType, name="profile-type"),
    # ajax nav message inbox
    path('unread-general-inbox/', unreadGeneralInbox, name="unread-general-inbox"),
    path('quote-accepted-rejected-count/', quoteAcceptedRejectedCount, name="quote-accepted-rejected-count"),
    path('request-got-quote-count/', requestGotQuoteCount, name="request-got-quote-count"),
    # ajax counters
    path('inbox-count/', inboxCount, name="inbox-count"),
    path('quote-inbox-count/', quotesInboxCount, name="quote-inbox-count"),
    # config
    path('notification-settings/', login_required(user_notification_settings), name="notification-settings"),
    # toggle activity notifications
    path('toggle-activity-notifications/', login_required(toggle_activity_notifications), name="toggle-activity-notifications"),
    # toggle support notifications
    path('toggle-support-notifications/', login_required(toggle_support_notifications), name="toggle-support-notifications"),
    # toggle marketing notifications
    path('toggle-marketing-notifications/', login_required(toggle_marketing_notifications), name="toggle-marketing-notifications"),
    # toggle messages notifications
    path('toggle-messages-notifications/', login_required(toggle_messages_notifications), name="toggle-messages-notifications"),
    # account settings
    path("edit-profile/<int:pk>", login_required(UserAccountUpdate.as_view()), name="edit-profile"),
    path("edit-email/<int:pk>", login_required(UserEmailUpdate.as_view()), name="edit-email"),
    path("my-profile", login_required(my_profile), name="my-profile"),
    path('edit-selling/<int:pk>', login_required(UserAccountSellingUpdate.as_view()), name="edit-selling"),
    # support faq
    path("support-faq/", login_required(support_faq), name="support-faq"),
]


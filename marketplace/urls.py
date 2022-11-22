from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import *


urlpatterns = [
    # Chat
    path('posts/', most_recent_filter, name="posts"),
    path('new-request/', login_required(new_request), name="new-request"),
    path('new-quote/<int:pk>', login_required(new_quote), name="new-quote"),
    path('edit-quote/<int:pk>/', EditQuoteView.as_view(), name='edit-quote'), 
    path('quote-details/<int:pk>', login_required(quote_details), name="quote-details"),
    path('most-recent-data/<int:num_posts>/', load_more_posts_most_recent, name="most-recent-data"),
    path('quoted-request-data/<int:num_posts>/', login_required(load_more_posts_quoted_requests), name="quoted-request-data"),
    path('saved-requests-data/<int:num_posts>/', login_required(load_more_posts_saved_requests), name="saved-requests-data"),
    path('like-unlike/', login_required(like_unlike_post), name="like-unlike"),
    path('messages', login_required(messages), name='messages'),
    path('new-message/<int:pk>', login_required(new_message), name='new-message'),
    path('respond-message', login_required(respond_message), name='respond-message'),
    path('message-user', login_required(message_user), name='message-user'),
    path('send-msg-to-user', login_required(send_message_user), name='send-msg-to-user'),
    path('message-detail/<int:pk>', login_required(message_detail), name="message-detail"),
    path('search-requests/', login_required(general_search_requests), name='search-requests'),
    path('search-quotes/', login_required(general_search_quotes), name='search-quotes'),
    path('request-details/<int:pk>/', login_required(request_details), name='request-details'),
    path('edit-request/<int:pk>/', login_required(edit_request), name='edit-request'), 
    path('edit-message/<int:pk>/', EditMessageView.as_view(), name='edit-message'), 
    path('delete-message/<int:pk>/', DeleteMessageView.as_view(), name='delete-message'), 
    path('respond-message-about-specific-request', login_required(respond_request_msg), name='respond-message-about-specific-request'),
    # path('respond-message-general', respond_msg_general, name='respond-message-general'),
    path('reject-quote', login_required(reject_quote), name='reject-quote'), 
    path('accept-quote', login_required(accept_quote), name='accept-quote'), 
    # feed filters (most-recent-filter = index page)
    path('quoted-request-filter', login_required(quoted_request_filter), name='quoted-request-filter'), 
    path('best-matches-filter', login_required(best_matches_filter), name='best-matches-filter'), 
    path('saved-requests-filter', login_required(saved_requests_filter), name='saved-requests-filter'), 
    # message filter
    path('message-filter/<int:pk>/', login_required(message_filter), name='message-filter'),
    path('message-search/', login_required(message_search), name='message-search'), 
    path('message-read/<int:pk>/', login_required(message_read), name='message-read'),
    # path('ticket-read/<int:pk>/', login_required(ticket_read), name='ticket-read'),
    # quote filter
    path('quotes/', login_required(open_quotes_filter), name="quotes"), #default page
    path('my-accepted-quotes-filter/', login_required(accepted_quotes_filter), name='my-accepted-quotes-filter'),
    path('my-rejected-quotes-filter/', login_required(rejected_quotes_filter), name='my-rejected-quotes-filter'),
    path('my-open-quotes-filter/', login_required(open_quotes_filter), name='my-open-quotes-filter'),
    # request filter
    path('requests/', login_required(open_requests_filter), name="requests"), #default page
    path('my-open-requests-filter/', login_required(open_requests_filter), name='my-open-requests-filter'),
    path('my-closed-requests-filter/', login_required(closed_requests_filter), name='my-closed-requests-filter'),
    # dismiss notification 
    path('dismiss-new-quote-notif/<int:pk>/', login_required(dismiss_new_quote_notif), name='dismiss-new-quote-notif'),
    # hides the quote on the req details page for the author of the request
    path('hide-quote/<int:pk>/', login_required(hide_quote), name='hide-quote'),
    # see all hidden quotes
    path('hidden-quotes', login_required(hidden_quotes), name='hidden-quotes'),
]
    
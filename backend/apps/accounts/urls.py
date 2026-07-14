from django.urls import path
from . import views

urlpatterns = [
    # Auth & Tokens
    path('csrf-token/', views.CSRFTokenView.as_view(), name='csrf_token'),
    path('user_login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('google_login/', views.GoogleLoginView.as_view(), name='google_login'),

    # User Profile Data
    path('user/', views.UserView.as_view(), name='user'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('update_profile/', views.ProfileView.as_view(), name='update_profile'),
    path('update_location/', views.UpdateLocationView.as_view(), name='update_location'),
    path('become_verified/', views.BecomeVerifiedView.as_view(), name='become_verified'),

    # Profile Pictures
    path('upload_profile_picture/', views.ProfilePictureView.as_view(), name='upload_profile_picture'),
    path('delete_profile_picture/', views.ProfilePictureView.as_view(), name='delete_profile_picture'),

    # --- UNIFIED PULSE SYSTEM ---
    path('add_pulse/', views.AddPulseAPIView.as_view(), name='add_pulse'),
    path("list-all-pulses/", views.PulseList.as_view(), name="list_all_pulses"),
    path("update_pulse/<int:pulse_id>/", views.PulseDetailView.as_view(), name="update_pulse"),
    path('remove_pulse/<int:pulse_id>/', views.PulseDetailView.as_view(), name='remove_pulse'),
    path("get_nearest_pulses/", views.NearestPulses.as_view(), name="get_nearest_pulses"),
    path('pulse/<int:pulse_id>/', views.PulseDetailRetrieve.as_view(), name='get_pulse_by_id'),
    path('pulse/comments/<int:pulse_id>/', views.PulseCommentsAPIView.as_view(), name='get_pulse_comments'),
    path('pulse/ratings/<int:pulse_id>/', views.PulseRatingAPIView.as_view(), name='add_pulse_rating'),
    path("create_pulse_rental/", views.CreatePulseRentalAPIView.as_view(), name="create_pulse_rental"),
    path("pulse_rentals/", views.UserRentalsAPIView.as_view(), name="get_user_rental"),
    path("pulse_rentals/<int:rental_id>/", views.ModifyRentalStatusAPIView.as_view(), name="modify_rental_status"),
    path("signal_pulse_rental/", views.SignalPulseRentalAPIView.as_view(), name="signal_pulse_rental"),
    path("pulse_rental_feedback/<int:rental_id>/", views.PulseRentalFeedbackAPIView.as_view(), name="pulse_rental_feedback"),
    path("pulse_own_proposals/", views.RentalProposalsAPIView.as_view(), name="get_rental_proposals"),
    path('favorites/', views.FavoritePulses.as_view(), name="get_favorite_pulses"),
    path('add_to_favorites/<int:pulse_id>/', views. AddPulseToFavoritesAPIView.as_view(), name='add_to_favorites'),
    path('delete_from_favorites/<int:pulse_id>/', views.DeletePulseFromFavoritesAPIView.as_view(), name='delete_from_favorites'),

    # Search & Social
    path("search-users/", views.SearchUsersAPIView.as_view(), name="search-users"),
    path("follow/<int:user_id>/", views.FollowUserAPIView.as_view()),
    path("follow-requests/accept/<int:request_id>/", views.AcceptFollowRequestAPIView.as_view()),
    path("follow-requests/reject/<int:request_id>/", views.RejectFollowRequestAPIView.as_view()),
    path("unfollow/<int:user_id>/", views.UnfollowUserAPIView.as_view(), name="unfollow-user"),
    path("follow-requests/", views.FollowRequestsAPIView.as_view()),
    path("direct_conversations/create/<int:user2_id>/", views.CreateDirectConversationAPIView.as_view(), name="create_conversation"),
    path("user_profile/<int:user_id>/", views.UserProfileAPIView.as_view(), name="user_profile"),
    path('message_keys/upload/', views.upload_public_key, name='upload_public_key'),
    path('message_keys/get/<int:user_id>/', views.get_public_key, name='get_public_key'),
    path('message_keys/get/me/', views.get_my_public_key, name='get_my_public_key'),
    path("messages/history/<str:chat_type>/<int:conversation_id>/", views.MessageHistoryAPIView.as_view(), name="chat_history"),
    path("my-conversations/", views.my_conversations, name="my_conversations"),
    path("notifications/", views.get_notifications, name="get_notifications"),
    path("notifications/mark-read/", views.mark_notifications_read, name="mark_notifications_read"),
    path("delete_notification/<int:notif_id>/", views.delete_notification, name="delete_notification"),

    # Warnings and shit
    path("alerts/", views.list_alerts, name="list_alerts"),
    path("alerts/create/", views.create_alert, name="create_alert"),
    path("alerts/<int:alert_id>/", views.alert_details, name="alert_details"),
    path("alerts/<int:alert_id>/confirm/", views.confirm_alert, name="confirm_alert"),
    path("alerts/<int:alert_id>/unconfirm/", views.unconfirm_alert, name="unconfirm_alert"),
    path("alerts/<int:alert_id>/report/", views.report_alert, name="report_alert"),
    path('alerts/comments/<int:alert_id>/', views.get_alert_comments, name='get_alert_comments'),
    path("alerts/weather/", views.get_current_weather, name="get_current_weather"),
    #Urgent requests
    path('urgent-requests/create/', views.create_urgent_request, name='create_urgent_request'),
    path('remove_request/<int:request_id>/', views.remove_request, name='remove_request'),
    path("update_request/<int:request_id>/", views.update_request, name="update_request"),
    path("urgent-requests/", views.urgent_requests_list, name="urgent_requests_list"),
    path("urgent-request/<int:request_id>/", views.get_request_by_id, name="urgent_request_detail"),
    path('urgent-requests/comments/<int:request_id>/', views.get_request_comments, name='get_request_comments'),
    path("list-all-requests/", views.list_all_requests, name="list_all_requests"),
    path("create_request_offer/", views.create_request_offer, name="create_request_offer"),
    path('request-offers/received/', views.get_user_request_offers, name='get_user_request_offers'),
    path('request-offers/<int:offer_id>/', views.modify_offer_status, name='modify_offer_status'),
    path('own-request-offers/', views.get_my_offers, name='own-request-offers'),
    path("request_rental_feedback/<int:rental_id>/", views.RequestRentalFeedbackAPIView.as_view(), name="request_rental_feedback"),

    #Admin urls
    path('admin_alert_reports/', views.admin_alert_reports, name='admin_reports'),
    path('ban-user/<int:user_id>/', views.ban_user, name='ban_user'),
    path('unban-user/<int:user_id>/', views.unban_user, name='unban_user'),
    path('flagged_posts/', views.flagged_posts, name='flagged_posts'),
    path('feedbacks/', views.admin_feedbacks, name='feedbacks'),
    path('delete_report/<int:report_id>/', views.delete_report, name='delete_report'),
    path('delete-pulse/<int:id>/', views.delete_pulse, name='delete_pulse'),
    path('delete-alert/<int:id>/', views.delete_alert, name='delete_alert'),
    path('delete-urgent-request/<int:id>/', views.delete_urgent_request, name='delete_urgent_request'),
    path("delete-rental-signal/<int:id>/", views.delete_rental_signal, name='delete_rental_signal'),
    path("delete-rental-feedback/<int:id>/", views.delete_rental_feedback, name='delete_rental_feedback'),
    path("delete-user-contact/<int:id>/", views.delete_user_contact, name='delete_user_contact'),
    path("contact/create/", views.create_contact_post, name='create_contact_post'),
    path("resolve-rental-signal/<int:id>/", views.resolve_rental_signal, name='resolve_rental_signal'),

    path("ai_chat/", views.ai_chat, name="ai_chat"),
]

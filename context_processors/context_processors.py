from video.models import Category, UserNotification, AdminNotification


def video(request):
    """
    To have categories, notifications and site announcements
    """
    categories = Category.objects.all()
    context = {"categories": categories}

    # Save user's notification in context if user is authenticated
    if request.user.is_authenticated:
        user_notif = UserNotification.objects.filter(receiver=request.user)
        admin_notif = AdminNotification.objects.filter(receiver=request.user)
        # Calculates total number of notifications
        total_notifs = user_notif.count() + admin_notif.count()

        context.update({"user_notif": user_notif,
                        "admin_notif": admin_notif,
                        "total_notifs": total_notifs})

    return context

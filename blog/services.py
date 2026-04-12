from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from .models import AffiliateClick


def get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def register_affiliate_click(request, post):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    ip_address = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    cutoff = timezone.now() - timedelta(hours=24)
    is_duplicate = AffiliateClick.objects.filter(
        post=post,
        clicked_at__gte=cutoff,
    ).filter(
        Q(session_key=session_key) | Q(ip_address=ip_address)
    ).exists()
    if not is_duplicate:
        AffiliateClick.objects.create(
            post=post,
            ip_address=ip_address,
            user_agent=user_agent,
            session_key=session_key,
        )

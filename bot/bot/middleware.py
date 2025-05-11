from datetime import date

from django.http import JsonResponse

from subscriptions.models import UserSubscription


class SubscriptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith('/api/order'):
            if not request.user.is_authenticated:
                return JsonResponse({'detail': 'Authentication required.'}, status=401)
            try:
                subscription = UserSubscription.objects.get(user=request.user)
                if subscription.end_date < date.today():
                    return JsonResponse({'detail': 'Your subscription has expired.'}, status=403)
            except UserSubscription.DoesNotExist:
                return JsonResponse({'detail': 'No active subscription found.'}, status=403)
        return self.get_response(request)
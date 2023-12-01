from django.http import JsonResponse
from django.views import View
import json


def verify_signature(request):
    """
    Get the actor's public key and verify that the incoming HTTP signature is valid
    """
    pass


def sign_activity(activity):
    """
    Sign outgoing activities using the keys stored in `[BASE_DIR] / data/keys/public.pem`
    and `[BASE_DIR] / data/keys/private.pem`
    """
    pass


def send_activity(activity, to_inbox):
    """
    Send the signed outgoing activity to the appropriate inboxes
    """
    pass


def handle_follow(activity, request):
    pass


def handle_create(activity):
    pass


def handle_update(activity):
    pass


def handle_delete(activity):
    pass


def handle_like(activity):
    pass


def handle_announce(activity):
    pass


def handle_undo(activity):
    pass


def handle_accept(activity):
    pass


def handle_reject(activity):
    pass


def handle_block(activity):
    pass


def handle_mention(activity):
    pass


def handle_move(activity):
    pass


class Inbox(View):
    def post(self, request, *args, **kwargs):
        activity = json.loads(request.body)

        if not verify_signature(request):
            return JsonResponse({"error": "Invalid signature"}, status=401)

        activity_type = activity.get("type")

        if activity_type == "Follow":
            handle_follow(activity, request)
        elif activity_type == "Create":
            handle_create(activity, request)
        elif activity_type == "Update":
            handle_update(activity, request)
        elif activity_type == "Delete":
            handle_delete(activity, request)
        elif activity_type == "Like":
            handle_like(activity, request)
        elif activity_type == "Announce":
            handle_announce(activity, request)
        elif activity_type == "Undo":
            handle_undo(activity, request)
        elif activity_type == "Accept":
            handle_accept(activity, request)
        elif activity_type == "Reject":
            handle_reject(activity, request)
        elif activity_type == "Block":
            handle_block(activity, request)
        elif activity_type == "Mention":
            handle_mention(activity, request)
        elif activity_type == "Move":
            handle_move(activity, request)
        else:
            return JsonResponse({"status": "Unknown activity type"}, status=400)

        return JsonResponse({"status": "Handled"})

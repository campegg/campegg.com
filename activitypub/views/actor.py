from django.http import JsonResponse
from django.views import View
from pathlib import Path
from django.conf import settings


class Actor(View):
    def get(self, request, *args, **kwargs):
        public_key_path = Path(settings.BASE_DIR) / "data/keys/public.pem"
        public_key_content = public_key_path.read_text().strip()

        base_url = request.build_absolute_uri("/")[:-1]

        actor_json = {
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1",
            ],
            "id": "https://campegg.com",
            "type": "Person",
            "preferredUsername": "cam",
            "name": "Cam Pegg",
            "summary": "I like coffee. I don't like celery.",
            "inbox": f"{base_url}/inbox",
            "outbox": f"{base_url}/outbox",
            "followers": f"{base_url}/followers",
            "following": f"{base_url}/following",
            "publicKey": {
                "id": "https://campegg.com/#key",
                "owner": "https://campegg.com",
                "publicKeyPem": public_key_content,
            },
            "icon": {
                "url": "https://campegg.com/assets/img/favicon-256x256.png",
                "type": "Image",
                "mediaType": "image/jpeg",
            },
            "attachment": [
                {
                    "type": "PropertyValue",
                    "name": "Website",
                    "value": '\u003ca href="https://campegg.com"\u003ecampegg.com\u003c/a\u003e',
                },
                {
                    "type": "PropertyValue",
                    "name": "GitHub",
                    "value": '\u003ca href="https://github.com/campegg"\u003egithub.com/campegg\u003c/a\u003e',
                },
                {
                    "type": "PropertyValue",
                    "name": "Micro.blog",
                    "value": '\u003ca href="https://campegg.micro.blog"\u003ecampegg.micro.blog\u003c/a\u003e',
                },
            ],
        }

        response = JsonResponse(actor_json)
        response["Content-Type"] = "application/activity+json"
        return response

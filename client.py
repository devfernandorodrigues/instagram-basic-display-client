import urllib


class InstagramBasicDisplayClient:
    API_ENDPOINT = "https://api.instagram.com"

    def __init__(
        self,
        client_id,
        client_secret,
        redirect_uri,
        scope="user_profile,user_media",
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.client_secret = client_secret

    def authorize(self):
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "response_type": "code",
        }

        url = (
            f"{self.API_ENDPOINT}/oauth/authorize?"
            f"{urllib.parse.urlencode(params)}"
        )

        return url

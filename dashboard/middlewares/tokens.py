from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import User
from rest_framework_simplejwt.exceptions import TokenError



class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # print("Something hit me")
        # print(scope.get("query_string", b"").decode())
        parts = scope.get("query_string", b"").decode().split("token=")
        if len(parts) != 2:
            print("Forbidden in the split")
            scope["ws_forbidden"] = True
            return await super().__call__(scope, receive, send)
        raw_token = parts[1]
        # print(f"Raw token is {raw_token}")
        try: 
            token = AccessToken(raw_token) # type: ignore
            user = await User.objects.aget(pk=token["user_id"])
            if not user:
                print("Forbidden in the user")
                scope["ws_forbidden"] = True
            return await super().__call__(scope, receive, send)
        except TokenError:
            print("Forbidden in the token error")
            scope["ws_forbidden"] = True
            return await super().__call__(scope, receive, send)
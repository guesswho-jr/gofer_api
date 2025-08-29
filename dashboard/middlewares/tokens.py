from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import User
from rest_framework_simplejwt.exceptions import TokenError



class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers: dict[bytes, bytes] = dict(scope["headers"])
        if not headers:
            scope["ws_forbidden"] = True
            return await super().__call__(scope, receive, send)
        raw_token: str = (headers.get(b"authorization")).decode() # type: ignore
        parts = raw_token.split(' ')
        if len(parts) != 2:
            scope["ws_forbidden"] = True
            return await super().__call__(scope, receive, send)
            # raise Http
        raw_token = parts[1] 
        try: 
            token = AccessToken(raw_token) # type: ignore
            user = await User.objects.aget(pk=token["user_id"])
            if not user:
                scope["ws_forbidden"] = True
                return await super().__call__(scope, receive, send)
            return await super().__call__(scope, receive, send)
        except TokenError:
            scope["ws_forbidden"] = True
            return await super().__call__(scope, receive, send)
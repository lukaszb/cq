from accounts.cqrs import app
from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
import re


TOKEN_RE = re.compile(r'^Token (\w+)$')


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        header = get_authorization_header(request)
        if not header:
            return (None, None)
        try:
            header = header.decode()
        except UnicodeError:
            raise AuthenticationFailed('Authorization header contains bad characters')
        finds = TOKEN_RE.findall(header)
        if not finds:
            raise AuthenticationFailed('Authorization header should be in format: "Token TOKEN"')
        token = finds[0]
        return self.authenticate_token(token)

    def authenticate_token(self, token):
        user = app.get_user_by_token(token)
        if user is None:
            raise AuthenticationFailed('Invalid token')
        elif not user.is_active:
            raise AuthenticationFailed('User inactive or deleted')
        return user, token

    def authenticate_header(self, request):
        return 'Token'

from rest_framework_simplejwt.tokens import RefreshToken

class Auth:
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
from rest_framework_simplejwt.views import TokenRefreshView


class TokenRefreshViewCustom(TokenRefreshView):
    def get_serializer_class(self):
        return TokenRefreshSerializer


class TokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh_token = data['refresh']
        user = self.get_token(refresh_token)

        return data

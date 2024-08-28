from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUser
from employers.serializers.role_serializers import RoleCreateSerializer


class RoleListView(APIView):
    def get(self, request, *args, **kwargs):
        roles = [role for role in CustomUser.ROLE_CHOICES if role[0] != CustomUser.EMPLOYER]

        return Response({
            "roles": roles
        }, status=status.HTTP_200_OK)


class RoleCreateView(APIView):
    serializer_class = RoleCreateSerializer

    def post(self, request):
        serializer = RoleCreateSerializer(data=request.data, context={'employer': request.user.employer_profile})

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Пользователь успешно создан",
                "user_id": user.id,
                "role": user.role},
                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

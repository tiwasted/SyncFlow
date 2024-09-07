from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from ..serializers.create_employee_serializers import EmployeeCreateSerializer
from users.models import CustomUser

User = get_user_model()


class EmployeeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'employer':
            return Response({"error": "Только Employer может создавать Employee."},
                            status=status.HTTP_403_FORBIDDEN)

        if not hasattr(request.user, 'employer_profile'):
            return Response({"error": "Этот пользователь не связан с профилем работодателя."},
                            status=status.HTTP_400_BAD_REQUEST)

        employer = request.user.employer_profile
        print("Работодатель из профиля пользователя:", employer)
        serializer = EmployeeCreateSerializer(data=request.data, context={'employer': employer})
        if serializer.is_valid():
            user = serializer.save(employer=employer)
            return Response({"message": "Employee создан успешно"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

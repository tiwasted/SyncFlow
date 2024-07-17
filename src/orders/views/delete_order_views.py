# from rest_framework import generics, permissions
# from users.models import CustomUser
# from employers.models import Employer
# from orders.models import Order
#
#
# class OrderDeleteView(generics.DestroyAPIView):
#     queryset = Order.objects.all()
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         # Получаем текущего пользователя
#         user = self.request.user
#
#         # Получаем объект Employer, связанный с текущим пользователем
#         try:
#             employer = user.employer_profile
#             return Order.objects.filter(employer=employer)
#         except Employer.DoesNotExist:
#             # Если объект Employer не найден, возвращаем пустой  QuerySet (список объектов Order)
#             return Order.objects.none()

# from rest_framework import generics, permissions
# from users.models import CustomUser
# from employers.models import Employer
# from orders.models import Order
# from orders.serializers.edit_order_serilalizers import OrderEditSerializer
#
#
# class OrderEditView(generics.UpdateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderEditSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         # получаем текущего пользователя
#         user = self.request.user
#
#         # Получаем объект Employer, связанный с текущим пользователем
#         try:
#             employer = user.employer_profile
#             return Order.objects.filter(employer=employer)
#         except Employer.DoesNotExist:
#             return Order.objects.none()

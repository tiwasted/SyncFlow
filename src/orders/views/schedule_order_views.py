from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from users.models import CustomUser
from b2b_client_orders.models import B2BOrder
from b2c_client_orders.models import B2COrder
from orders.serializers.order_serializers import B2BOrderSerializer, B2COrderSerializer
from orders.permissions import CanViewOrder
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404


class OrderScheduleViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, CanViewOrder]

    def list(self, request):
        date = request.query_params.get('date')
        user_id = request.query_params.get('user_id')

        print(f"Received date: {date}, user_id: {user_id}")

        if date and user_id:
            try:
                date = parse_date(date)
                if not date:
                    raise ValueError("Некорректная дата")

                # Получаем employer_id по user_id
                user = CustomUser.objects.get(id=user_id)
                try:
                    employer = user.employer_profile  # Используем связь
                    employer_id = employer.id
                except Employer.DoesNotExist:
                    raise ValueError("Employer не найден для данного пользователя")

                print(f"Employer ID: {employer_id}")

                b2b_orders = B2BOrder.objects.filter(order_date=date, status='in waiting', employer=employer_id)
                b2c_orders = B2COrder.objects.filter(order_date=date, status='in waiting', employer=employer_id)

                b2b_serializer = B2BOrderSerializer(b2b_orders, many=True)
                b2c_serializer = B2COrderSerializer(b2c_orders, many=True)

                data = b2b_serializer.data + b2c_serializer.data
                print(f"Returning data: {data}")

                return Response(data)
            except Exception as e:
                print(f"Unexpected error: {e}")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Дата или user_id не указаны"}, status=status.HTTP_400_BAD_REQUEST)


    # def list(self, request):
    #     date = request.query_params.get('date')
    #     user_id = request.query_params.get('user_id')
    #
    #     if not date or not user_id:
    #         return Response({"error": "Дата или user_id не указаны"}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     try:
    #         date = parse_date(date)
    #         if not date:
    #             raise ValueError("Некорректная дата")
    #     except ValueError as e:
    #         print(f"Date parsing error: {e}")
    #         return Response({"error": "Некорректная дата"}, status=status.HTTP_400_BAD_REQUEST)
    #
    #         # Получаем employer_id по user_id
    #         user = CustomUser.objects.get(id=user_id)
    #         employer_id = user.employer.id
    #
    #     try:
    #         user = get_object_or_404(CustomUser, id=user_id)
    #
    #         # Проверьте, что у пользователя есть связанный объект Employer
    #         if user.role == CustomUser.EMPLOYER:
    #             employer_id = user.id  # Предположим, что в этом случае user.id является employer_id
    #         else:
    #             # Используйте связь для получения employer_id
    #             employer_id = user.employer_profile.id
    #
    #         print(f"Employer ID for user {user_id}: {employer_id}")
    #
    #         b2b_orders = B2BOrder.objects.filter(order_date=date, status='in waiting', employer=employer_id)
    #         b2c_orders = B2COrder.objects.filter(order_date=date, status='in waiting', employer=employer_id)
    #
    #         b2b_serializer = B2BOrderSerializer(b2b_orders, many=True)
    #         b2c_serializer = B2COrderSerializer(b2c_orders, many=True)
    #
    #         return Response(b2b_serializer.data + b2c_serializer.data)
    #     except CustomUser.DoesNotExist:
    #         print(f"User with ID {user_id} does not exist.")
    #         return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         print(f"Unexpected error: {e}")
    #         return Response({"error": "Произошла ошибка на сервере"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class OrderScheduleViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated, CanViewOrder]
#
#     def list(self, request):
#         date = request.query_params.get('date')
#         user_id = request.query_params.get('user_id')
#         print(f"Received date: {date}, user_id: {user_id}")  # Логирование параметров
#
#         if not date or not user_id:
#             return Response({"error": "Дата или user_id не указаны"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             date = parse_date(date)
#             if not date:
#                 raise ValueError("Некорректная дата")
#             print(f"Дата на сервере: {date}")
#         except ValueError as e:
#             print(f"Date parsing error: {e}")
#             return Response({"error": "Некорректная дата"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             user = User.objects.get(id=user_id)
#             employer_id = user.employer.id
#             print(f"Employer ID for user {user_id}: {employer_id}")
#
#             b2b_orders = B2BOrder.objects.filter(order_date=date, status='in waiting', employer=employer_id)
#             b2c_orders = B2COrder.objects.filter(order_date=date, status='in waiting', employer=employer_id)
#
#             b2b_serializer = B2BOrderSerializer(b2b_orders, many=True)
#             b2c_serializer = B2COrderSerializer(b2c_orders, many=True)
#
#             return Response(b2b_serializer.data + b2c_serializer.data)
#         except User.DoesNotExist:
#             print(f"User with ID {user_id} does not exist.")
#             return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
#         except ValueError as e:
#             print(f"ValueError: {e}")
#             return Response({"error": "Некорректная дата"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             print(f"Unexpected error: {e}")
#             return Response({"error": "Произошла ошибка на сервере"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def list(self, request):
    #     date = request.query_params.get('date')
    #     user_id = request.query_params.get('user_id')
    #
    #     try:
    #         date = parse_date(date)
    #         print(f"Parsed date: {date}")
    #         if not date:
    #             raise ValueError("Некорректная дата")
    #     except Exception as e:
    #         print(f"Date parsing error: {e}")
    #         raise
    #
    #     if date and user_id:
    #         try:
    #             date = parse_date(date)
    #             if not date:
    #                 raise ValueError("Некорректная дата")
    #
    #             # Получаем employer_id по user_id
    #             user = User.objects.get(id=user_id)
    #             employer_id = user.employer.id
    #
    #             b2b_orders = B2BOrder.objects.filter(order_date=date, status='in waiting', employer=employer_id)
    #             b2c_orders = B2COrder.objects.filter(order_date=date, status='in waiting', employer=employer_id)
    #
    #             b2b_serializer = B2BOrderSerializer(b2b_orders, many=True)
    #             b2c_seroalizer = B2COrderSerializer(b2c_orders, many=True)
    #             return Response(b2b_serializer.data + b2c_seroalizer.data)
    #         except ValueError:
    #             return Response({"error": "Некорректная дата"}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response({"error": "Дата не указана"}, status=status.HTTP_400_BAD_REQUEST)

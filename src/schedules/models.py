# from django.db import models
# from orders.models import Order
# from employees.models import Employee
#
#
# class Schedule(models.Model):
#     order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='schedule')
#     assigned_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"{self.order.order_name} - {self.assigned_employee.user.phone}"
#

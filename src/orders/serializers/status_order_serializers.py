from rest_framework import serializers


class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['status']

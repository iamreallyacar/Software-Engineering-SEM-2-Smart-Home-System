from rest_framework import serializers
from api.models.log_models import (
    DeviceLog1Min, DeviceLogDaily, DeviceLogMonthly,
    RoomLog1Min, RoomLogDaily, RoomLogMonthly,
    EnergyGeneration1Min, EnergyGenerationDaily, EnergyGenerationMonthly
)


# Device Log Serializers
class DeviceLog1MinSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLog1Min
        fields = '__all__'


class DeviceLogDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLogDaily
        fields = '__all__'


class DeviceLogMonthlySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLogMonthly
        fields = '__all__'


# Room Log Serializers
class RoomLog1MinSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomLog1Min
        fields = '__all__'


class RoomLogDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomLogDaily
        fields = '__all__'


class RoomLogMonthlySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomLogMonthly
        fields = '__all__'


# Energy Generation Serializers
class EnergyGeneration1MinSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyGeneration1Min
        fields = '__all__'


class EnergyGenerationDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyGenerationDaily
        fields = '__all__'


class EnergyGenerationMonthlySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyGenerationMonthly
        fields = '__all__'

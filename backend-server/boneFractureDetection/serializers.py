from rest_framework import serializers
from .models import predictions


class BoneFractureDetectionSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = predictions
        fields = ['image']

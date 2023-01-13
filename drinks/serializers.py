from rest_framework import serializers
from .models import Drink

class DrinkSerializer(serializers.ModelSerializer):

  # inner class to describe the metadata of the model
  class Meta:
    model = Drink
    fields = ['id', 'name', 'description']
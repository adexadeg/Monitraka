from rest_framework import serializers
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = ['title', 'category', 'amount', 'the_currency', 'the_duration', 'start_date', 'end_date']
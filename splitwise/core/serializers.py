from rest_framework import serializers

from .models import User, Group, Expense, Settlement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def __str__(self):
        return self.name
    

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = all

    def __str__(self):
        return self.name
    

    
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = all
        
    def __str__(self, *args, **kwds):
        return f"{self.name} - {self.amount}"
    

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = all

    def __str__(self):
        return f"Settlement of {self.amount} from {self.paid_by} to {self.paid_to}"
   
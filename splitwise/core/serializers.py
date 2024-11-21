from rest_framework import serializers

from .models import User, Group, Expense, Settlement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, instance, validated_data):
      
        user = User(
            name=validated_data['name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user
    
    
        userisPresnent = User.objects.get(email=validated_data['email'])
        if(userisPresnent):
            User.objects.filter(email=validated_data['email']).update(name=validated_data['name']) 
            User.objects.filter(email=validated_data['email']).update(password=validated_data['password'])
            return "Updated User information"
        
        return "User not fount"

    

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'users' , 'id']

    def __str__(self):
        return self.name
    

    
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'paid_by', 'group' , 'created_at' , 'id']
        
    def __str__(self, *args, **kwds):
        return f"{self.name} - {self.amount}"
    

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = ['amount', 'paid_by', 'paid_to', 'group' , 'created_at'  , 'notes' , 'id']

    def __str__(self):
        return f"Settlement of {self.amount} from {self.paid_by} to {self.paid_to}"
   
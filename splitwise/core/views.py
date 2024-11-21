from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer,GroupSerializer,ExpenseSerializer
from .models import User, Group,Expense






# ----------------------------user views -----------------------
@api_view(['POST'])
def user_login(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])  
        user.save()
        
        return Response({
            "message": "User created successfully",
            "data": serializer.data  
        }, status=201)
    
    return Response({
        "error": serializer.errors
    }, status=400)



@api_view(['PUT'])
def update_userinfo(request,id):
   
    print(id)

    persentUser = User.objects.get(id=id)
    if(persentUser):
        persentUser.name = request.data.get('name')
        persentUser.email = request.data.get('email')
        updateduser =  persentUser.save()
        return Response({
            "message": "User updated successfully",
            "data": updateduser
        }, status=201)
    
    return Response({
        "error": "User not found"
    }, status=400)


@api_view(['GET'])
def getuser_Info(request,id):
    persentUser = User.objects.get(id=id)
    serializer = UserSerializer(persentUser)

    if(persentUser):
        return Response({
            "message": "User found successfully",
            "data": serializer.data
        }, status=201)
    
    return Response({
        "error": "User not found"
    }, status=400)
   


@api_view(['DELETE'])
def deleteuser_Info(request,id):
    persentUser = User.objects.get(id=id)
    seraliser  = UserSerializer(persentUser)
    if(persentUser):
        persentUser.delete()
        return Response({
            "message": "User deleted successfully",
            "data": seraliser.data
        }, status=201)
    
    return Response({
        "error": "User not found"
    }, status=400)
    



#---------------- Group Views ----------------
@api_view(['POST'])
def create_group(request):
    groupname = request.data.get('groupName')
    createduserdata = request.data.get('created_by')

    group = Group.objects.create(name=groupname)
    seraliser = GroupSerializer(group)
    group.users.add(createduserdata)

    return Response({
        "message": "Group created successfully",
        "data": seraliser.data
    }, status=201)


@api_view(['GET'])
def get_groups(request):
    groups = Group.objects.all()
    if not groups:
        return Response({
            "error": "Groups not found"
        }, status=400)
    seraliser = GroupSerializer(groups, many=True)

    return Response({
        "message": "Groups found successfully",
        "data": seraliser.data
    }, status=201)
    

@api_view(['GET'])
def get_group_user_present(request,id):
    group = Group.objects.get(id=id)
    if not group:
        return Response({
            "error": "Group not found"
        }, status=400)
    seraliser = GroupSerializer(group)

    return Response({
        "message": "Group found successfully",
        "data": seraliser.data    
    }, status=201)




@api_view(['PUT'])
def add_user_to_group(request,id):
    group = Group.objects.get(id=id)
    user_info = request.data.get('user_info')

   
    if not group:
        return Response({
            "error": "Group not found"
        }, status=400)
    group.users.add(user_info)
    seraliser = GroupSerializer(group)

    return Response({
        "message": "Group found successfully",
        "data": seraliser.data    
    }, status=201)




@api_view(['DELETE'])
def delete_group(request,id):
    group = Group.objects.get(id=id)
    if not group:
        return Response({
            "error": "Group not found"
        }, status=400)
    group.delete()
    return Response({
        "message": "Group deleted successfully"
    }, status=201)



#--------------------------------expenses view ---------------------

@api_view(['POST'])
def create_expense(request):

    #we need group and user info who will add edxpense

    group_id = request.data.get('group_id')
    expense_name = request.data.get('expense_name')
    expense_amount = request.data.get('expense_amount')
    expense_paid_by = request.data.get('expense_paid_by')

    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=expense_paid_by)

    expense = Expense.objects.create(name=expense_name, amount=expense_amount, paid_by=user, group=group)
    seraliser = ExpenseSerializer(expense)

    return Response({
        "message": "Expense created successfully",
        "data": seraliser.data    
    }, status=201)

@api_view(['PUT'])
def add_users_to_expense(request,id):
    expense = Expense.objects.get(id=id)
    user_info = request.data.get('user_info')

   
    if not expense:
        return Response({
            "error": "Expense not found"
        }, status=400)
    expense.users.add(user_info)
    seraliser = ExpenseSerializer(expense)

    return Response({
        "message": "Expense found successfully",
        "data": seraliser.data    
    }, status=201)


@api_view(['GET'])
def get_expense_info(request,id):
    expense = Expense.objects.get(id=id)
    if not expense:
        return Response({
            "error": "Expense not found"
        }, status=400)
    seraliser = ExpenseSerializer(expense)

    return Response({
        "message": "Expense found successfully",
        "data": seraliser.data    
    }, status=201)

@api_view(['GET'])
def get_expense_for_perticular_user(request,id):
    expense = Expense.objects.filter(paid_by=id)
    if not expense:
        return Response({
            "error": "Expense not found"
        }, status=400)
    seraliser = ExpenseSerializer(expense, many=True)

    return Response({
        "message": "Expense found successfully",
        "data": seraliser.data    
    }, status=201)


@api_view(['PUT'])
def update_expense(request,id):
    expense = Expense.objects.get(id=id)
    expense_name = request.data.get('expense_name')
    expense_amount = request.data.get('expense_amount')

    if not expense:
        return Response({
            "error": "Expense not found"
        }, status=400)
    expense.name = expense_name
    expense.amount = expense_amount
    expense.save()
    seraliser = ExpenseSerializer(expense)

    return Response({
        "message": "Expense found successfully",
        "data": seraliser.data    
    }, status=201)


@api_view(['DELETE'])
def delete_expense(request,id):
    expense = Expense.objects.get(id=id)
    if not expense:
        return Response({
            "error": "Expense not found"
        }, status=400)
    expense.delete()
    return Response({
        "message": "Expense deleted successfully"
    }, status=201)


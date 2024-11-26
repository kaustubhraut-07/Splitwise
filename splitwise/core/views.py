from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer,GroupSerializer,ExpenseSerializer, SettlementSerializer
from .models import User, Group,Expense,Settlement
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.mail import send_mail

# ----------------------------user views -----------------------
@api_view(['POST'])
def user_registeration(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()  
        
        return Response({
            "message": "User created successfully",
            "data": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            } 
        }, status=201)
    
    return Response({
        "error": serializer.errors
    }, status=400)

@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        send_welcome_email()
        return Response({'message': 'User logged in successfully' , "data": UserSerializer(user).data})
    else:
        
        return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['PUT'])
def update_userinfo(request, id):
    try:
      
        persentUser = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({
            "error": "User not found"
        }, status=404)

   
    name = request.data.get('name', persentUser.name)  
    email = request.data.get('email', persentUser.email)  
    password = request.data.get('password')


    persentUser.name = name
    persentUser.email = email
    if password:
        persentUser.set_password(password) 

    persentUser.save()

    return Response({
        "message": "User updated successfully",
        "data": {
            "id": persentUser.id,
            "name": persentUser.name,
            "email": persentUser.email
        }
    }, status=200)

    # persentUser = User.objects.get(id=id)
    # if(persentUser):
    #     persentUser.name = request.data.get('name')
    #     persentUser.email = request.data.get('email')
    #     updateduser =  persentUser.save()
    #     return Response({
    #         "message": "User updated successfully",
    #         "data": updateduser
    #     }, status=201)
    
    # return Response({
    #     "error": "User not found"
    # }, status=400)


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


@api_view(['GET'])
def get_all_users_in_group(request,id):
    useringroup = Group.objects.filter(id=id)
    if not useringroup:
        return Response({
            "error": "Group not found"
        }, status=400)
    seraliser = GroupSerializer(useringroup, many=True)

    return Response({
        "message": "Group found successfully",
        "data": seraliser.data[0]   
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

@api_view(['GET'])
def get_all_expenses_in_group(request , id):
    expense = Expense.objects.filter(group=id)
    if not expense:
        return Response({
            "error": "Expense not found"
        }, status=400)
    seraliser = ExpenseSerializer(expense, many=True)

    return Response({
        "message": "Expense found successfully",
        "data": seraliser.data    
    }, status=201)

# ----------- Settlement apis ----------------

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Expense, Settlement, User
from .serializers import ExpenseSerializer

@api_view(['POST'])
def user_settlement_with_other_user(request, id):
    try:
       
        expense = Expense.objects.get(id=id)
    except Expense.DoesNotExist:
        return Response({"error": "Expense not found"}, status=404)

    user_paid_to_id = request.data.get('user_paid_to')
    user_paid_by_id = request.data.get('user_paid_by')
    amount = request.data.get('amount')
    notes = request.data.get('notes')

    
    if not user_paid_to_id or not user_paid_by_id or not amount:
        return Response({"error": "All fields are required"}, status=400)

    try:
        
        user_paid_to = User.objects.get(id=user_paid_to_id)
        user_paid_by = User.objects.get(id=user_paid_by_id)
    except User.DoesNotExist:
        return Response({"error": "Invalid user ID(s) provided"}, status=400)

    
    settlement = Settlement.objects.create(
        paid_by=user_paid_by,
        paid_to=user_paid_to,
        amount=amount,
        notes=notes,
        group=expense.group
    )

    
    serializer = ExpenseSerializer(expense)

    update_amount_in_expense = expense.amount - amount
    expense.amount = update_amount_in_expense
    expense.save()

    return Response({
        "message": "Settlement created successfully",
        "data": serializer.data
    }, status=201)



@api_view(['POST'])
def add_settlement_to_group(request, id):
    expene = Expense.objects.get(id=id)
    expensed_added_person_id = request.data.get('expensed_added_person_id')

    if not expene:  
        return Response({
            "error": "Expense not found"
        }, status=400)
    print(expene.group)
    group_id= expene.group.id
    # expense should be equaly divied to the number of user present in a group
    # we will get all users id in the group if weget the group etails

    group = Group.objects.get(id=group_id)
    users = group.users.all()
    amount = expene.amount

    for user in users:
        user_paid_to = User.objects.get(id=expensed_added_person_id) 
        user_paid_by = user
        amount = expene.amount / len(users)
        Settlement.objects.create(
            paid_by=user_paid_by,
            paid_to=user_paid_to,
            amount=amount,
            group=group

        )

    return Response({
        "message": "Settlement created successfully"
    }, status=201)



@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_all_settlements_in_group(request , id):
    settlement = Settlement.objects.filter(group=id)
    if not settlement:
        return Response({
            "error": "Settlement not found"
        }, status=400)
    seraliser = SettlementSerializer(settlement, many=True)

    return Response({
        "message": "Settlement found successfully",
        "data": seraliser.data    
    }, status=201)








#-------------- Email Configurations --------------
def send_welcome_email():
    subject = 'Welcome to Our Service'
    message = 'Thank you for signing up!'
    from_email = 'kaustubhraut135@gmail.com'
    recipient_list = ['kaustubhraut135@gmail.com']

    send_mail(subject, message, from_email, recipient_list)
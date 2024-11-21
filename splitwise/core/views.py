from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer,GroupSerializer
from .models import User, Group






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
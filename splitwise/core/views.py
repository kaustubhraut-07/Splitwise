from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer

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

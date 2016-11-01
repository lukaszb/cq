from .cqrs import app
from .serializers import AccountActivationSerializer
from .serializers import CredentialsSerializer
from .serializers import RegisterSerializer
from .serializers import UserProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    event = app.register(
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password'],
    )
    return Response({'user_id': event.entity_id})


@api_view(['POST'])
@permission_classes([AllowAny])
def activate(request, user_id):
    serializer = AccountActivationSerializer(user_id, data=request.data)
    serializer.is_valid(raise_exception=True)
    token = serializer.validated_data['token']
    app.activate_with_token(user_id, token)
    return Response({})


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_auth_token(request):
    serializer = CredentialsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = app.get_by_email(serializer.validated_data['email'])
    event = app.obtain_auth_token(user.id)
    return Response({
        'id': user.id,
        'token': event.data['auth_token'],
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)

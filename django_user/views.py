
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication, exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django_user.models import BlackList
from django_user.serializer import UserSignupSerializer

class CustomAuthentication(BaseAuthentication):

    def authenticate(self, request):
        if 'HTTP_AUTHORIZATION' in request.META: 
            token = request.META['HTTP_AUTHORIZATION'][4:]
            try:
                BlackList.objects.get(token=token)                
                raise exceptions.AuthenticationFailed('Unauthorized user')
            except BlackList.DoesNotExist:
                pass

class UserSignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        "View for user signup"  
        signup_serializer = UserSignupSerializer(data=request.data)
        signup_serializer.is_valid(raise_exception=True)
        user = signup_serializer.save()
        
        user.set_password(request.data.get("password"))
        user.save()
        return Response("User signup successfully")

class UserSigInView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        "View for user signin"
        try:
            user = User.objects.get(username=request.data.get("username"))
        except User.DoesNotExist:
            raise exceptions.ValidationError('Username or password is incorrect')

        if not user.check_password(request.data.get("password")):
            raise exceptions.ValidationError('Username or password is incorrect')

        # Do your stuffs here

        # Generating JWT authentication
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        
        return Response({
            "auth-token" : token
        })

class UserLogoutView(APIView):
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)

    def post(self, request):
        "View for user logout"
        # Get token from the header
        token = request.META['HTTP_AUTHORIZATION'][4:]

        # save token to the blacklist
        BlackList(token=token).save()
        return Response("User logged out")
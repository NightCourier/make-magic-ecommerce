from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView


# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User


class HealthView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        return Response({"message": "It works!"}, status=status.HTTP_200_OK)


class Authentication(ObtainAuthToken):

    def post(self, request, *args, **kwargs):

        # username = request.data.get('username')
        # password = request.data.get('password')
        #
        # if not User.objects.filter(username=username).exists():
        #     return Response(
        #         {'error': 'The user doesn\'t exist'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        #
        # user = authenticate(username=username, password=password)
        # if not user:
        #     return Response(
        #         {'error': 'The password is incorrect'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        serializer = self.serializer_class(data=request.data, context={"request": request})

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response({"error": "The authentication is failed"}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)

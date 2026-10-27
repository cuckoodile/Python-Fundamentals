from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BaseUser, Contact, ContactType
from .serializers import (
    BaseUserSerializer,
    ContactSerializer,
    ContactTypeSerializer,
    LoginSerializer,
)


# ---------- Auth ----------

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # a stale token in the header must not block login

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': BaseUserSerializer(user, context={'request': request}).data,
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()  # request.auth is the Token object
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = BaseUserSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---------- BaseUser ----------

class BaseUserListCreateAPIView(APIView):
    def get(self, request):
        users = BaseUser.objects.filter(is_active=True).prefetch_related('contacts__type')
        serializer = BaseUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BaseUserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BaseUserRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(
            BaseUser.objects.filter(is_active=True).prefetch_related('contacts__type'), pk=pk
        )

    def get(self, request, pk):
        serializer = BaseUserSerializer(self.get_object(pk), context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        serializer = BaseUserSerializer(
            self.get_object(pk), data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        serializer = BaseUserSerializer(
            self.get_object(pk), data=request.data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        # Soft delete, matching the is_active=True filter used above
        user = self.get_object(pk)
        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- ContactType ----------

class ContactTypeListCreateAPIView(APIView):
    def get(self, request):
        serializer = ContactTypeSerializer(ContactType.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContactTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContactTypeRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(ContactType, pk=pk)

    def get(self, request, pk):
        serializer = ContactTypeSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        serializer = ContactTypeSerializer(self.get_object(pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        serializer = ContactTypeSerializer(self.get_object(pk), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- Contact ----------

class ContactListCreateAPIView(APIView):
    def get(self, request):
        contacts = Contact.objects.select_related('type', 'owner')
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContactRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Contact.objects.select_related('type', 'owner'), pk=pk)

    def get(self, request, pk):
        serializer = ContactSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        serializer = ContactSerializer(self.get_object(pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        serializer = ContactSerializer(self.get_object(pk), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.shortcuts import render
from .serializer import UserSerializer
from .models import User
from rest_framework.views import Response, APIView
from rest_framework import status, generics

# Create your views here.

class UserListCreateAPI(APIView):
    def get(self, request):
        model = User.objects.all()
        serializer = UserSerializer(model, many=True, context={'request': request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        seralizer = UserSerializer(data=request.data, context={'request': request})
        if seralizer.is_valid():
            seralizer.save()
            return Response(data=seralizer.data, status=status.HTTP_201_CREATED)

        return Response(data=seralizer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRetrieveAPI(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(data={"detail": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

        seralizer = UserSerializer(user,  context={'request': request})
        return Response(data=seralizer.data, status=status.HTTP_200_OK)
        

# class UserListCreateAPI(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
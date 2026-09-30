from django.shortcuts import render
from rest_framework.views import status, APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import UserSerializer
from .models import User

# Create your views here.

# POST
# GET
# PATCH
# PUT
# DELETE / DESTROY


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# {Model}{[Methods]}APIView
# class UserListCreateAPIView(APIView):
#     def get(self, request):
#         # List = Get All
#         model = User.objects.all()
#         serializer = UserSerializer(model, many=True)

#         return Response(data=serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():   # serializer.is_valid() is a method that return bool
#             serializer.save()   # save calls either SQL QUERY: INSERT or UPDATE
#             # INSERT INTO users VALUE(...)
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserRetrieveUpdateDeleteAPIView(APIView):
    # filter_classes
    # sort...
    # permission_classes

    # Retrieve (1) vs List (All or Many) | Quantity of display
    # Update (PATCH)
    # Delete (DESTROY)
    def get(self, request, pk):
        # Check if the given pk is valid
        try:
            # pk = Primary Key (DB id) | Comes from the request URL
            user = User.objects.get(id=pk)  # Get the User model using the id or pk
        except User.DoesNotExist:
            return Response(
                data={'detail': 'User not found!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # SELECT {fields} FROM {model} WHERE {condition}

        #  user = User.objects.get(id=pk)       ORM
        # SELECT * FROM users WHERE id=1        SQL Query

        print("Request user ID: ", request.user.id)
        print("Model ID: ", user.id)
        # request.user.id == Logged in user (Current user)
        # user.id == Selected user to GET or PATCH (given pk)
        if request.user.id != user.id:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'detail': 'You are not authorized to do this!'},
            )

        serializer = UserSerializer(user)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    # PATCH = Partial (specific update)
    # vs
    # PUT = Full Data (All data)
    def patch(self, request, pk):
        # Check if the given pk is valid
        try:
            # pk = Primary Key (DB id) | Comes from the request URL
            user = User.objects.get(id=pk)  # Get the User model using the id or pk
        except User.DoesNotExist:
            return Response(
                data={'detail': 'User not found!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate if the request user to update is him/herself
        if request.user.id != user.id:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'detail': 'You are not authorized to do this!'},
            )

        # At this point, we are sure that the given pk is valid and existing

        # UserSerializer(user)  GET (List or Retrieve)
        # UserSerializer(data=request.data) POST
        # UserSerializer(user, data=request.data) PATCH
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():   # is_valid() return True if there is no validation error i.e. len(username) <= 150, False if there is an error.
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        # Check if the given pk is valid
        try:
            # pk = Primary Key (DB id) | Comes from the request URL
            user = User.objects.get(id=pk)  # Get the User model using the id or pk
        except User.DoesNotExist:
            return Response(
                data={'detail': 'User not found!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate if the request user to update is him/herself
        if request.user.id != user.id:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'detail': 'You are not authorized to do this!'},
            )
        
        user.delete()   # Method to deleted the selected user
        return Response(
            data={'detail': f"User {user.username} is deleted successfully!"},
            status=status.HTTP_200_OK,
        )
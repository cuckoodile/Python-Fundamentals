from django.shortcuts import render
from .serializer import UserSerializer
from .models import User
from rest_framework.views import Response, APIView
from rest_framework import status

# Create your views here.

# class UserListCreateAPI(APIView):
#     def get(self, request):
#         model = User.objects.all().filter(is_active=True)
#         serializer = UserSerializer(model, many=True, context={'request': request})

#         return Response(data=serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         seralizer = UserSerializer(data=request.data, context={'request': request})
#         if seralizer.is_valid():
#             seralizer.save()
#             return Response(data=seralizer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(data=seralizer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserRetrieveUpdateDeleteAPI(APIView):
#     def get(self, request, pk):
#         user = User.check_if_user_exists(pk)
#         if user is None or user.is_active == False:
#             return Response(data={"detail": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

#         seralizer = UserSerializer(user,  context={'request': request})
#         return Response(data=seralizer.data, status=status.HTTP_200_OK)

#     def patch(self,request, pk):
#         try:
#             user = User.objects.get(id=pk)
#         except User.DoesNotExist:
#             return Response(data={"detail": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

#         if request.user.id != user.id:
#             return Response(
#                 data={"detail": "You do not have permission to update this account!"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         serializer = UserSerializer(user, data=request.data, context={'request': request}, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         user = User.check_if_user_exists(pk)
#         if user is None:
#             return Response(
#                 data={"detail": "User not found!"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         if request.user.id != user.id:
#             return Response(
#                 data={"detail": "You do not have permission to do this!"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         # user.delete()
#         # return Response(
#         #     data={"detail": "Delete successful!"},
#         #     status=status.HTTP_200_OK
#         # )

#         seralizer = UserSerializer(user, data={'is_active': False} ,context={'request': request}, partial=True)
#         if seralizer.is_valid():
#             seralizer.save()
#             return Response({'message': 'All goods!', 'data': seralizer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response(data=seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
        

         
        

# # class UserListCreateAPI(generics.ListCreateAPIView):
# #     queryset = User.objects.all()
# #     serializer_class = UserSerializer






























# ==========================================






class UserListCreateAPIView(APIView):
    def get(self, request):
        users = User.objects.all().filter(is_active=True)
        serializer = UserSerializer(users, many=True, context={'request': request})

        if len(users) == 0:
            return Response(
                data={"detail": "No users yet!"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )



class UserRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, pk):
        user = User.check_if_user_exists(pk)

        if user is None or user.is_active == False:
            return Response(
                data={'detail': 'User not found!'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserSerializer(user, context={'request': request})

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        user = User.check_if_user_exists(pk)

        if user is None or user.is_active == False:
            return Response(
                data={'detail': 'User not found!'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.id != user.id:
            return Response(
                data={'detail': 'You do not have permission to do this!'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserSerializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk):
        user = User.check_if_user_exists(pk)

        if user is None or user.is_active == False:
            return Response(
                data={'detail': 'User not found!'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.id != user.id:
            return Response(
                data={'detail': 'You do not have permission to do this!'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Hard Delete
        serializer = UserSerializer(user, context={'request': request})
        user.delete()

        return Response(
            data={
                'detail': serializer.data,
                'msg': 'User deleted successfully!',
            },
            status=status.HTTP_200_OK,
        )


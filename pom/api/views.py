from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import filters
from authentication.models import User
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from api.serializers import UserSerializer
from django.db.models import Q  # For combining queries with OR
from  .serializers import *
from api.models import Messege
from django.core.exceptions import ObjectDoesNotExist



class UpdateUserProfileView(APIView):

    def post(self, request):

        post_data = request.data
        user_id = post_data.get('id')
        name = post_data.get("name")
        occupation = post_data.get('occupation')
        dob = post_data.get('dob')
        phone = post_data.get('phone')
        gender = post_data.get('gender')

        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            user.full_name = name
            user.occupation = occupation
            user.dob = dob
            user.phone = phone
            user.gender = gender
            user.save()
            return Response({'success': 'User updated successfully!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserListView(APIView):
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone', 'full_name','dob','email']

    def get(self, request):
        useres = User.objects.all()
        query = request.query_params.get('search', None)
        if query is not None:
            useres = useres.filter(Q(phone__icontains=query) | Q(full_name__icontains=query) | Q(dob__icontains=query) | Q(email__icontains=query))

        serializer = UserSerializer(useres, many=True)
        data = serializer.data

        response = []
        for i in range(len(data)):
            print(data[i]["id"])
            print(useres[i])

            i_data = {
                "id": data[i]['id'],
                "full_name": data[i]['full_name'],
                "phone": data[i]['phone'],
                "email": data[i]['email'],
                "created_at": data[i]['created_at'],
                "dob": data[i]['dob'],
            }

            response.append(i_data)

        return Response(response, status=status.HTTP_200_OK)


class MessegeView(APIView):
    def post(self, request):
        post_data = request.data
        user_id = post_data.get('id')

        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            messege_objects = Messege.objects.filter(user=user)
            if not messege_objects.exists():
                return Response({'error': 'No messages found for the user'}, status=status.HTTP_404_NOT_FOUND)

            serializer = MessegeSerializer(messege_objects, many=True)
            res_data = serializer.data
            return Response(res_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateMessegeView(APIView):
    def post(self, request):
        serializer = MessegeSerializer2(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Messege Sent successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        try:
            messege_id = request.data.get('id')
            messege = Messege.objects.get(id=messege_id)
        except Messege.DoesNotExist:
            return Response("Messege not found", status=status.HTTP_404_NOT_FOUND)

        serializer = MessegeSerializer2(messege, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Attendance updated successfully", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



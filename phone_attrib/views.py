from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Customer
from .serializers import CustomerSerializer, PhoneAttribSerializer
from .services import PhoneAttribService
import phonenumbers


class CustomerListApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        todos = Customer.objects.all();
        serializer = CustomerSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name')
        }
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PhoneListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **customerId):
        customerId = int(self.kwargs['customerId'])
        areaCode = int(self.kwargs['areaCode'])

        if not Customer.objects.filter(pk=customerId).exists():
            return Response("Customer does not exists", status=status.HTTP_400_BAD_REQUEST)

        if  PhoneAttribService.phone_list.get(areaCode) is None or len(PhoneAttribService.phone_list.get(areaCode)) == 0:
            return Response("Phone Numbers not available for this area code", status=status.HTTP_400_BAD_REQUEST)

        if(not phonenumbers.is_valid_number_for_region(phonenumbers.parse("+1%s9999999" % areaCode, None), "US")):
            return Response("Invalid area code for US", status=status.HTTP_400_BAD_REQUEST)

        phone = PhoneAttribService.attribPhone(customerId, areaCode);

        if phone is None:
            return Response("Error in phone attribution", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = PhoneAttribSerializer(data={'phone': phone})
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
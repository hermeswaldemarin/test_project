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
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
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

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **customer_id):
        customer_id = int(self.kwargs['customer_id'])
        area_code = int(self.kwargs['area_code'])

        if not Customer.objects.filter(pk=customer_id).exists():
            return Response("Customer does not exists", status=status.HTTP_400_BAD_REQUEST)

        number = phonenumbers.parse("+1%s9999999" % area_code, None)

        if not phonenumbers.is_valid_number_for_region(number, "US"):
            return Response("Invalid area code for US", status=status.HTTP_400_BAD_REQUEST)

        if PhoneAttribService.phone_list.get(area_code) is None or len(PhoneAttribService.phone_list.get(area_code)) == 0:
            return Response("Phone Numbers not available for this area code", status=status.HTTP_400_BAD_REQUEST)

        phone = PhoneAttribService.attrib_phone(customer_id, area_code)

        if phone is None:
            return Response("Error in phone attribution", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = PhoneAttribSerializer(data={'phone': phone})
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

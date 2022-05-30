import os
import sendgrid
from sendgrid.helpers.mail import *
from django.conf import settings
import phonenumbers

from phone_attrib.models import Customer


class PhoneAttribService(object):
    SENDGRID_API_KEY = getattr(settings, "SENDGRID_API_KEY", None)
    PHONEATTRIB_MAILFROM = getattr(settings, "PHONEATTRIB_MAILFROM", None)
    PHONEATTRIB_SUBJECT = getattr(settings, "PHONEATTRIB_SUBJECT", None)

    phone_list = {306:
        [
            {"number": "224-2700"},
            {"number": "224-2701"},
            {"number": "224-2702"},
            {"number": "224-2703"},
            {"number": "224-2704"},
            {"number": "224-2705"},
            {"number": "224-2706"}
        ],
        430:
            [
                {"number": "852-0501"},
                {"number": "852-0502"},
                {"number": "852-0503"},
                {"number": "852-0504"},
                {"number": "852-0505"},
                {"number": "852-0506"},
                {"number": "852-0507"}
            ]
    }

    @staticmethod
    def attribPhone(customerId, areaCode):

        customer = Customer.objects.get(pk=customerId);

        phone_object = PhoneAttribService.phone_list.get(areaCode).pop();
        phone_number = phone_object["number"];

        from_email = Email(PhoneAttribService.PHONEATTRIB_MAILFROM)
        to_email = Email(customer.email)
        content = Content("text/plain", "Phone Number: (%s) %s" % (areaCode,phone_number))
        mail = Mail(from_email, PhoneAttribService.PHONEATTRIB_SUBJECT, to_email, content)
        try:
            sg = sendgrid.SendGridAPIClient(api_key=PhoneAttribService.SENDGRID_API_KEY)
            response = sg.client.mail.send.post(request_body=mail.get())
            return "(%s) %s" % (areaCode,phone_number);
        except Exception as e:
            print(e)
            return;
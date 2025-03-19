from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer, SignupSerializer
from django.conf import settings
import requests
import os

class ContactView(APIView):
    def post(self, request):
        print(request.data)
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            subject = f"New Contact Form Submission - {data['enquiryType']}"
            message = f"""
            Enquiry Type: {data['enquiryType']}
            Name: {data['name']}
            Email: {data['email']}
            Message: {data['enquiry']}
            """

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],  # Receiver
                    fail_silently=False,
                )
                return Response({"message": "Contact email sent successfully!"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": "Failed to send email.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Google reCAPTCHA Verification
            captcha_value = data["captchaValue"]
            recaptcha_secret = os.getenv("RECAPTCHA_SECRET_KEY")
            recaptcha_response = requests.post(
                f"https://www.google.com/recaptcha/api/siteverify?secret={recaptcha_secret}&response={captcha_value}"
            ).json()

            if not recaptcha_response.get("success"):
                return Response({"message": "Invalid captcha."}, status=status.HTTP_400_BAD_REQUEST)

            subject = "New Signup Submission"
            message = f"""
            New user signed up:
            - Name: {data["firstName"]} {data["lastName"]}
            - Email: {data["email"]}
            - Profession: {data["profession"]}
            - Topics: {", ".join(data.get("topics", []))}
            - Teams: {", ".join(data.get("teams", []))}
            - Privacy Policy Accepted: {"Yes" if data["privacyPolicy"] else "No"}
            """

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],  # Receiver
                    fail_silently=False,
                )
                return Response({"message": "Signup email sent successfully!"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": "Failed to send email.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

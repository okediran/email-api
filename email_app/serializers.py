from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    enquiryType = serializers.CharField(max_length=100)
    enquiry = serializers.CharField()

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    firstName = serializers.CharField(max_length=100)
    lastName = serializers.CharField(max_length=100)
    profession = serializers.CharField(max_length=255)
    topics = serializers.ListField(child=serializers.CharField(max_length=255), required=False)
    teams = serializers.ListField(child=serializers.CharField(max_length=255), required=False)
    privacyPolicy = serializers.BooleanField()
    captchaValue = serializers.CharField()

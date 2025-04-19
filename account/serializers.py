import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import OTP, Profile
from config import settings

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        # Generate OTP
        otp_code = str(random.randint(1000, 9999))
        OTP.objects.create(user=user, code=otp_code)

        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP code is {otp_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        return user


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            otp = OTP.objects.filter(user=user, code=data['code']).latest('created_at')

            if otp.is_expired():
                raise serializers.ValidationError("OTP has expired.")

        except (User.DoesNotExist, OTP.DoesNotExist):
            raise serializers.ValidationError("Invalid OTP.")

        user.is_verified = True
        user.save()
        otp.delete()

        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_verified:
            raise serializers.ValidationError('Your email is not verified.')

        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

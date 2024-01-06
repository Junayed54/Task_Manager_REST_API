from .models import User
from rest_framework import serializers,status
from rest_framework.validators import ValidationError
from django.contrib.auth.hashers import make_password
from phonenumber_field.serializerfields import PhoneNumberField


class UserCreationSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=40,allow_blank=True)
    email=serializers.EmailField(max_length=80,allow_blank=False)
    phone_number=PhoneNumberField(allow_null=False,allow_blank=False)
    password=serializers.CharField(allow_blank=False,write_only=True)


    class Meta:
        model=User
        fields=['id','username', 'email', 'phone_number','password']

    def validate(self,attrs):
        email_exists=User.objects.filter(username=attrs.get('username')).exists()

        if email_exists:
            raise ValidationError(detail="User with email exists",code=status.HTTP_403_FORBIDDEN)

        username_exists=User.objects.filter(username=attrs.get('username')).exists()

        if username_exists:
            raise ValidationError(detail="User with username exists",code=status.HTTP_403_FORBIDDEN)

        return super().validate(attrs)


    def create(self,validated_data):
        new_user=User(**validated_data)

        new_user.password=make_password(validated_data.get('password'))

        new_user.save()

        return new_user
    
    
class UserProfileUpdateSerializer(UserCreationSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        instance.save()

        return instance
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=80, allow_blank=False)
    password = serializers.CharField(allow_blank=False, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials. Please try again.')

        data['user'] = user
        return data
    
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(allow_blank=False, write_only=True)
    new_password = serializers.CharField(allow_blank=False, write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        current_password = data.get('current_password')

        if not user.check_password(current_password):
            raise serializers.ValidationError('Current password is incorrect.')

        return data
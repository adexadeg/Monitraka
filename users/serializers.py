from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    class Meta: 
        model = User
        fields = ['id', 'fullname', 'email', 'phone_number', 'password', 'confirm_password', 'how_did_you_hear_about_us']
        extra_kwargs = {
            'password': {'style': {'input_type': 'password'},'write_only': True}
        }


    def validate(self, args):
        email = args.get('email', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email already exists')})
        return super().validate(args)



    def create(self, validated_data):
        password = validated_data.pop('password', None)
        confirm_password = validated_data.pop('confirm_password', None)

        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    remember_me = serializers.BooleanField()
    class Meta: 
        model = User
        fields = ['id', 'email', 'password', 'remember_me']
        extra_kwargs = {
            'password': {'style': {'input_type': 'password'},'write_only': True}
        }


class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ''


class ProfileSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'phone_number', 'avatar']

    def create(self, validated_data):
        user = User(
            fullname=validated_data['fullname'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            avatar=validated_data['avatar']
        )
        user.save

        return user

class PasswordSettingsSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_new_password']

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({'new_password': 'Password fields must match.'})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'old_password': 'Old password is not correct'})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance




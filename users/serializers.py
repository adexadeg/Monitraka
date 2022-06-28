import profile
from attr import fields
from rest_framework import serializers
from .models import User, Profile
from django.dispatch import receiver
from django.db.models.signals import post_save

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
            'password': {'write_only': True}
        }


class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ''


class ProfileSettingsSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    avatar = serializers.ImageField()
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'phone_number', 'avatar']


    # def get_fullname(self, obj):
    #         customer_account_query = models.Profile.objects.filter(
    #             customer_id=obj.id)
    #         serializer = AccountSerializer(customer_account_query, many=True)
    
    #         return serializer.data

    # def get_fullname(self, obj):
    #     request = self.context['request']
    #     return request.User.get_fullname()

    def update(self, instance, validated_data):
        # retrieve the User
        profile = validated_data.pop('profile', None)
        for attr, value in profile.items():
            setattr(instance.user, attr, value)

        # retrieve Profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance

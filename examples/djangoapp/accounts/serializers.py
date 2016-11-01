from accounts.cqrs import app
from accounts.models import User
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from ses.contrib.django.shortcuts import get_entity_or_404


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        if app.storage.get_unique('user', value) is not None:
            raise serializers.ValidationError('E-mail is already registered')
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'last_logged_in', 'last_logged_out']


class CredentialsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data['email']
        password = data['password']

        try:
            user = app.get_by_email(email)
        except app.repo.DoesNotExist:
            raise serializers.ValidationError({
                'email': 'Could not find user for this email',
            })
        if not check_password(password, user.encoded_password):
            raise serializers.ValidationError({
                'password': 'Wrong password',
            })
        return data


class AccountActivationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64)

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id

    def validate_token(self, value):
        user = get_entity_or_404(app.repo, self.user_id)
        if value != user.activation_token:
            raise serializers.ValidationError("Wrong activation token")
        if user.is_active:
            raise serializers.ValidationError("User is already is_active")
        return value

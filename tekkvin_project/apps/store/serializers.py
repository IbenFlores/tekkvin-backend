from django.contrib.auth import authenticate, get_user_model, password_validation
from django.db import transaction
from rest_framework import serializers

from .models import Brand, Category, Customer, Product

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('Ya existe una cuenta con este correo.')
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Ya existe una cuenta con este correo.')
        if Customer.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Ya existe un cliente con este correo.')
        return value

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        Customer.objects.create(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            created_id=user.pk,
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs['email'].strip().lower()
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=attrs['password'],
        )
        if user is None:
            raise serializers.ValidationError('Correo o contraseña incorrectos.')
        attrs['user'] = user
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'parent_category')
        read_only_fields = fields


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'support_url')
        read_only_fields = fields


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'sku',
            'name',
            'technical_specifications',
            'sale_price',
            'current_stock',
            'minimum_stock',
            'is_active',
            'category',
            'brand',
        )
        read_only_fields = fields
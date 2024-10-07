from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Product, Category, Order, OrderItem, Review
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

# User model (using Django's get_user_model for flexibility)
UserModel = get_user_model()
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2", "is_buyer", "is_seller")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            is_buyer=validated_data.get("is_buyer", False),
            is_seller=validated_data.get("is_seller", False),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


# User Registration Serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "email",
            "username",
            "password",
        )  # Use specific fields for registration

    def create(self, validated_data):
        # Use create_user method to handle password hashing
        user_obj = UserModel.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user_obj


# User Login Serializer
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        return user


# Basic User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email", "username")


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "stock_quantity",
            "image_url",
            "created_at",
        ]


# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the username instead of user id

    class Meta:
        model = Review
        fields = ["id", "user", "product", "rating", "comment", "created_at"]


# Order Item Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "unit_price"]


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "total_price",
            "created_at",
            "updated_at",
            "order_items",
        ]


# User Model in Order (if needed, you could expand on user details in the OrderSerializer)
class UserDetailInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "username", "email"]

"""
Serializers for API endpoints.
"""
from rest_framework import serializers
from apps.users.models import User
from apps.routes.models import Route
from apps.bookings.models import Booking
from apps.reviews.models import Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'profile_image', 'bio', 'location', 'is_guide', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'is_guide'
        ]

    def validate(self, data):
        """Validate passwords match."""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data

    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class RouteSerializer(serializers.ModelSerializer):
    """Serializer for Route model."""
    created_by = UserSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = [
            'id', 'title', 'description', 'location', 'difficulty',
            'duration', 'price', 'image', 'created_by', 'created_at',
            'average_rating', 'reviews_count', 'is_active'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def get_average_rating(self, obj):
        """Get average rating for route."""
        return obj.get_average_rating()

    def get_reviews_count(self, obj):
        """Get reviews count for route."""
        return obj.get_reviews_count()


class RouteCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating routes."""
    
    class Meta:
        model = Route
        fields = [
            'title', 'description', 'location', 'difficulty',
            'duration', 'price', 'image'
        ]


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model."""
    user = UserSerializer(read_only=True)
    route = RouteSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'route', 'date', 'participants',
            'status', 'total_price', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'total_price', 'created_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings."""
    
    class Meta:
        model = Booking
        fields = ['route', 'date', 'participants', 'notes']

    def validate_date(self, value):
        """Validate booking date is not in the past."""
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("No puedes reservar una fecha pasada")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    user = UserSerializer(read_only=True)
    route = RouteSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'route', 'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating reviews."""
    
    class Meta:
        model = Review
        fields = ['route', 'rating', 'comment']

    def validate_rating(self, value):
        """Validate rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("La calificación debe estar entre 1 y 5")
        return value

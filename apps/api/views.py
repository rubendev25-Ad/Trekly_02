"""
API ViewSets for RESTful endpoints.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from apps.users.models import User
from apps.routes.models import Route
from apps.bookings.models import Booking
from apps.reviews.models import Review

from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    RouteSerializer, RouteCreateSerializer,
    BookingSerializer, BookingCreateSerializer,
    ReviewSerializer, ReviewCreateSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User operations."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """Use different serializer for registration."""
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def guides(self, request):
        """Get all guides."""
        guides = User.objects.filter(is_guide=True)
        serializer = self.get_serializer(guides, many=True)
        return Response(serializer.data)


class RouteViewSet(viewsets.ModelViewSet):
    """ViewSet for Route operations."""
    queryset = Route.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty', 'location', 'created_by']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['created_at', 'price', 'title']

    def get_serializer_class(self):
        """Use different serializer for create/update."""
        if self.action in ['create', 'update', 'partial_update']:
            return RouteCreateSerializer
        return RouteSerializer

    def perform_create(self, serializer):
        """Set created_by to current user."""
        if not self.request.user.is_guide:
            raise PermissionError("Solo los guías pueden crear rutas")
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def my_routes(self, request):
        """Get routes created by current user."""
        routes = Route.objects.filter(created_by=request.user, is_active=True)
        serializer = self.get_serializer(routes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular routes."""
        from django.db.models import Count
        routes = Route.objects.filter(is_active=True).annotate(
            booking_count=Count('bookings')
        ).order_by('-booking_count')[:5]
        serializer = self.get_serializer(routes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get reviews for a route."""
        route = self.get_object()
        reviews = Review.objects.filter(route=route)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for Booking operations."""
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['status', 'date']
    ordering_fields = ['date', 'created_at']

    def get_serializer_class(self):
        """Use different serializer for create."""
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def get_queryset(self):
        """Filter bookings by user."""
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        # Show user's bookings or bookings for their routes
        return Booking.objects.filter(
            user=user
        ) | Booking.objects.filter(route__created_by=user)

    def perform_create(self, serializer):
        """Set user to current user and calculate total price."""
        booking = serializer.save(user=self.request.user)
        booking.total_price = booking.calculate_total_price()
        booking.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking."""
        booking = self.get_object()
        if booking.status == 'cancelled':
            return Response(
                {'error': 'Esta reserva ya está cancelada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.status = 'cancelled'
        booking.save()
        return Response({'status': 'Reserva cancelada'})

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking (guide only)."""
        booking = self.get_object()
        if booking.route.created_by != request.user and not request.user.is_staff:
            return Response(
                {'error': 'No tienes permiso para confirmar esta reserva'},
                status=status.HTTP_403_FORBIDDEN
            )
        booking.status = 'confirmed'
        booking.save()
        return Response({'status': 'Reserva confirmada'})


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for Review operations."""
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['route', 'rating']
    ordering_fields = ['created_at', 'rating']

    def get_serializer_class(self):
        """Use different serializer for create."""
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_queryset(self):
        """Filter reviews if specified."""
        queryset = Review.objects.all()
        route_id = self.request.query_params.get('route', None)
        if route_id:
            queryset = queryset.filter(route_id=route_id)
        return queryset

    def perform_create(self, serializer):
        """Set user to current user."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Get reviews by current user."""
        reviews = Review.objects.filter(user=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

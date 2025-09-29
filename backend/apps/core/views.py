from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Restaurant, Menu, Vote
from .serializers import RestaurantSerializer, MenuSerializer, EmployeeCreateSerializer, VoteSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .authentication import MixedAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

User = get_user_model()

class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]  # або IsAuthenticated

class EmployeeCreateView(generics.CreateAPIView):
    serializer_class = EmployeeCreateSerializer
    permission_classes = [AllowAny]

class RestaurantCreateView(generics.CreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [MixedAuthentication]

class UploadMenuView(generics.CreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [MixedAuthentication]

    def perform_create(self, serializer):
        # перевіримо унікальність restaurant+date — модель має constraint,
        # але додатково можемо охопити помилку тут
        serializer.save()

class TodayMenuView(APIView):
    authentication_classes = [MixedAuthentication]
    permission_classes = [AllowAny]  # меню доступні без логіна для перегляду

    def get(self, request):
        restaurant_id = request.query_params.get('restaurant')
        today = timezone.localdate()
        qs = Menu.objects.filter(date=today)
        if restaurant_id:
            qs = qs.filter(restaurant_id=restaurant_id)
        menus = MenuSerializer(qs, many=True).data
        return Response(menus)

class VoteView(APIView):
    authentication_classes = [MixedAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, menu_id):
        user = request.user
        try:
            menu = Menu.objects.get(pk=menu_id)
        except Menu.DoesNotExist:
            return Response({'detail': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)
        # перевірка: голосувати можна тільки за поточний день
        if menu.date != timezone.localdate():
            return Response({'detail': 'Cannot vote for non-current menu'}, status=status.HTTP_400_BAD_REQUEST)
        # унікальність vote enforced на рівні моделі
        vote, created = Vote.objects.get_or_create(employee=user, menu=menu)
        if not created:
            return Response({'detail': 'Already voted'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(VoteSerializer(vote).data, status=status.HTTP_201_CREATED)

class ResultsTodayView(APIView):
    authentication_classes = [MixedAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        restaurant_id = request.query_params.get('restaurant')
        today = timezone.localdate()
        qs = Menu.objects.filter(date=today)
        if restaurant_id:
            qs = qs.filter(restaurant_id=restaurant_id)
        results = []
        for menu in qs:
            results.append({
                'menu_id': menu.id,
                'restaurant_id': menu.restaurant_id,
                'votes': menu.votes.count(),
                'items_preview': menu.items[:3] if isinstance(menu.items, list) else menu.items
            })
        # сортуємо за кількістю голосів
        results.sort(key=lambda r: r['votes'], reverse=True)
        return Response(results)

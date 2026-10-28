from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import LoginSerializer, ProductSerializer, RegisterSerializer


class RegisterView(APIView):
	permission_classes = (permissions.AllowAny,)

	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		token, _ = Token.objects.get_or_create(user=user)
		return Response(
			{'token': token.key, 'user_id': user.pk, 'email': user.email},
			status=status.HTTP_201_CREATED,
		)


class LoginView(APIView):
	permission_classes = (permissions.AllowAny,)

	def post(self, request):
		serializer = LoginSerializer(
			data=request.data,
			context={'request': request},
		)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, _ = Token.objects.get_or_create(user=user)
		return Response({'token': token.key, 'user_id': user.pk, 'email': user.email})


class ProductListView(generics.ListAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = ProductSerializer

	def get_queryset(self):
		queryset = Product.objects.filter(status=True, is_active=True).select_related(
			'category', 'brand'
		)
		category_id = self.request.query_params.get('category')
		brand_id = self.request.query_params.get('brand')
		if category_id:
			queryset = queryset.filter(category_id=category_id)
		if brand_id:
			queryset = queryset.filter(brand_id=brand_id)
		return queryset


class ProductDetailView(generics.RetrieveAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = ProductSerializer
	queryset = Product.objects.filter(status=True, is_active=True).select_related(
		'category', 'brand'
	)

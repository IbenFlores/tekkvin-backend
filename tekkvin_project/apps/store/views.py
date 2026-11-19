from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
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


class LogoutView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request):
		Token.objects.filter(user=request.user).delete()
		return Response(
			{'detail': 'Sesión cerrada correctamente.'},
			status=status.HTTP_200_OK,
		)


class ProfileView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request):
		customer = getattr(request.user, 'customer', None)
		return Response(
			{
				'user_id': request.user.pk,
				'customer_id': customer.pk if customer else None,
				'email': request.user.email,
				'first_name': request.user.first_name,
				'last_name': request.user.last_name,
				'role': request.user.role.name if request.user.role else None,
			},
			status=status.HTTP_200_OK,
		)


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
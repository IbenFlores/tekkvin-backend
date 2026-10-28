from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Brand, Category, Customer, Product


class StoreApiTests(APITestCase):
	def setUp(self):
		self.category = Category.objects.create(name='Audio', create_id=1)
		self.brand = Brand.objects.create(name='Acme', create_id=1)

	def test_registration_creates_account_customer_and_token(self):
		response = self.client.post(
			'/api/auth/register/',
			{
				'first_name': 'Ada',
				'last_name': 'Lovelace',
				'email': 'ada@example.com',
				'password': 'A-long-and-unique-password-938!',
			},
			format='json',
		)

		self.assertEqual(response.status_code, 201)
		self.assertTrue(response.data['token'])
		self.assertTrue(get_user_model().objects.filter(username='ada@example.com').exists())
		self.assertTrue(Customer.objects.filter(email='ada@example.com').exists())

	def test_login_returns_token(self):
		user = get_user_model().objects.create_user(
			username='ada@example.com',
			email='ada@example.com',
			password='A-long-and-unique-password-938!',
		)

		response = self.client.post(
			'/api/auth/login/',
			{'email': user.email, 'password': 'A-long-and-unique-password-938!'},
			format='json',
		)

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.data['token'])

	def test_product_list_filters_by_category_and_brand(self):
		matching_product = Product.objects.create(
			name='Headphones',
			category=self.category,
			brand=self.brand,
			is_active=True,
			create_id=1,
		)
		Product.objects.create(name='Inactive', is_active=False, create_id=1)

		response = self.client.get(
			'/api/products/',
			{'category': self.category.pk, 'brand': self.brand.pk},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual([item['id'] for item in response.data], [matching_product.pk])

	def test_product_detail_returns_active_product(self):
		product = Product.objects.create(name='Headphones', is_active=True, create_id=1)

		response = self.client.get(f'/api/products/{product.pk}/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['id'], product.pk)

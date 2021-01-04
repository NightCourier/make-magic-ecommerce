from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

User = get_user_model()


class LatestPopularProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:
    objects = LatestPopularProductsManager()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class RatingStar(models.Model):
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинг"
        verbose_name_plural = "Звёзды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField("IP-address", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Категория")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')  # add ForeignKey to multiple models

    def __str__(self):
        return f"{self.star} - {self.content_object}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинг"


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Текст отзыва", max_length=1000)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Категория")
    object_id = models.PositiveIntegerField(verbose_name="Номер продукта")
    content_object = GenericForeignKey('content_type', 'object_id', )  # add ForeignKey to multiple models

    def __str__(self):
        return f"{self.email} - {self.content_object}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Product(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=100, default='Кубик Рубика', verbose_name='Название')
    url = models.SlugField(max_length=50, unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    manufacturer = models.CharField(max_length=100, verbose_name='Производитель')
    rating = GenericRelation(Rating)
    review = GenericRelation(Review)

    class Meta:
        abstract = True


class RubiksCube(Product):
    dimension = models.PositiveIntegerField(verbose_name='Размерность')
    material = models.CharField(max_length=100, verbose_name='Материал')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    complexity = models.PositiveSmallIntegerField(verbose_name='Сложность')
    packaging = models.CharField(max_length=255, verbose_name='Упаковка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кубик Рубика'
        verbose_name_plural = 'Кубики Рубика'


# TODO: implement normal authorization functionality with clients
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адресс доставки')

    def __str__(self):
        return f'Покупатель {self.user}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class CartProduct(models.Model):
    customer = models.ForeignKey("Customer", verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name='Корзина', on_delete=models.CASCADE, related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количевство')
    final_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return f'Продукт в корзине {self.object_id}'

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'


class Cart(models.Model):
    owner = models.ForeignKey("Customer", on_delete=models.CASCADE, verbose_name='Покупатель')
    products = models.ManyToManyField("CartProduct", verbose_name='Товары', blank=True, related_name="related_cart")
    total_products = models.PositiveIntegerField(default=0, verbose_name='Общее количевство товаров')
    final_price = models.DecimalField(max_digits=7, decimal_places=2,  verbose_name='Общая цена')

    def __str__(self):
        return f'Корзина {self.owner}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

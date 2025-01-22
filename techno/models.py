from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(draft=False)

class FilterSettings(models.Model):
    show_category_filter = models.BooleanField(default=True, verbose_name="Показывать фильтр категорий")
    show_brand_filter = models.BooleanField(default=True, verbose_name="Показывать фильтр брендов")
    show_availability_filter = models.BooleanField(default=True, verbose_name="Показывать фильтр по наличию")
    show_power_filter = models.BooleanField(default=True, verbose_name="Показывать фильтр мощности")
    show_blocktype_filter = models.BooleanField(default=True, verbose_name="Показывать фильтр по типу блока")
    show_invertor_filter = models.BooleanField(default=True, verbose_name="Показывать фильтр инвертора")
    show_splitsystem_filter = models.BooleanField(default=True, verbose_name="Показывать фильтр сплит систем")
    show_price_filter = models.BooleanField(default=True, verbose_name="Показывать фильтр по ценам")


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=100)
    description = models.TextField("Описание", blank=True, null=True)
    url = models.SlugField(max_length=160, unique=True)
    image = models.ImageField("Изображение", upload_to="data/", blank=True, null=True)
    sort_order = models.PositiveIntegerField("Сортировка", default=0)

    objects = models.Manager()  # Стандартный менеджер
    active = ActiveManager()    # Менеджер для активных записей
    draft = models.BooleanField("Черновик", default=False)

    def update_related_drafts(self):
        # Если категория в черновике, поместить все связанные бренды и товары в черновик
        if self.draft:
            Brand.objects.filter(category=self).update(draft=True)
            Product.objects.filter(category=self).update(draft=True)
        else:
            Brand.objects.filter(category=self).update(draft=False)
            Product.objects.filter(category=self).update(draft=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse('category_detail_path', args=[self.url])


class Brand(models.Model):
    """Бренды"""
    name = models.CharField("Бренд", max_length=100)
    description = models.TextField("Описание", blank=True, null=True)
    url = models.SlugField(max_length=160, unique=True)
    image = models.ImageField("Изображение", upload_to="data/", blank=True, null=True)
    category = models.ManyToManyField(Category, verbose_name="Категория", related_name="brand_category")
    sort_order = models.PositiveIntegerField("Сортировка", default=0, blank=True, null=True)


    objects = models.Manager()
    active = ActiveManager()
    draft = models.BooleanField("Черновик", default=False)

    def update_related_products(self):
        # Если бренд в черновике, поместить все товары в черновик
        if self.draft:
            Product.objects.filter(brand=self).update(draft=True)
        else:
            Product.objects.filter(brand=self).update(draft=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


    def get_absolute_url(self):
        if self.category.exists():
            return reverse('brand_category_list', args=[self.category.first().url, self.url])
        return '#'

@receiver(post_save, sender=Category)
def update_category_draft(sender, instance, **kwargs):
    instance.update_related_drafts()

@receiver(post_save, sender=Brand)
def update_brand_draft(sender, instance, **kwargs):
    instance.update_related_products()

class CategoryBrand(models.Model):
    """Промежуточная модель для связи между Category и Brand"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    url = models.SlugField(max_length=160, unique=True)


class Currency(models.Model):
    """Валюта"""
    name = models.CharField("Наименование валюты", max_length=255, unique=True)
    symbol = models.CharField("Валютный знак", max_length=2, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class Powerr(models.Model):
    """Мощность"""
    NamePower = models.CharField("Мощность", max_length=255, unique=True)

    def __str__(self):
        return self.NamePower

    class Meta:
        verbose_name = 'Мощность'
        verbose_name_plural = 'Мощности'

class BlockType(models.Model):
    """Тип блока"""
    BlockType = models.CharField("Тип блока", max_length=255, unique=True)

    def __str__(self):
        return self.BlockType

    class Meta:
        verbose_name = 'Тип блока'
        verbose_name_plural = 'Типы блоков'

class SplitSystem(models.Model):
    """Тип блока"""
    SplitSystem = models.CharField("Сплит система", max_length=255, unique=True)

    def __str__(self):
        return self.SplitSystem

    class Meta:
        verbose_name = 'Сплит система'
        verbose_name_plural = 'Сплит системы'


class Product(models.Model):
    """Товар, продукт"""
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True, related_name="product_category"
    )
    brand = models.ForeignKey(
        Brand, verbose_name="Бренд", on_delete=models.SET_NULL, null=True, related_name="product_brand"
    )
    Powerr = models.ForeignKey(
        Powerr, verbose_name="Мощность", on_delete=models.SET_NULL, null=True, related_name="power_category", blank=True
    )
    BlockType = models.ForeignKey(
        BlockType, verbose_name="Тип блока", on_delete=models.SET_NULL, null=True, related_name="blocktype_category", blank=True
    )
    SplitSystem = models.ForeignKey(
        SplitSystem, verbose_name="Сплит система", on_delete=models.SET_NULL, null=True, related_name="splitsystem_category", blank=True
    )
    title = models.CharField("Название", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    series = models.CharField("Серия", max_length=100, null=True, blank=True)
    type = models.CharField("Исполнение", max_length=50, null=True, blank=True)
    price = models.DecimalField("Цена", default=0, help_text="Проверить валюту", max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name="Валюта", default=0)
    availability = models.PositiveIntegerField("Наличие", default=0)
    power = models.DecimalField("Производительность", default=0, max_digits=8, decimal_places=2, null=True, blank=True)
    relevance = models.CharField("Актуальность", max_length=100, null=True, default=1)
    mark = models.CharField("Отметка", max_length=50, default='0')
    date_of_establishment = models.DateField("Дата заведения", default=date.today().strftime('%Y-%m-%d'))
    image = models.ImageField("Изображение", upload_to="data/", blank=True)
    number_of_views = models.PositiveIntegerField("Количество просмотров", default=0)
    draft = models.BooleanField("Черновик", default=False)
    invertor = models.BooleanField("Инвертор", default=False) # Инвертор
    url = models.SlugField(max_length=130, unique=True)
    noise = models.CharField("Шум", max_length=50, null=True, blank=True)
    refrigerant = models.CharField("Хладагент", max_length=50, null=True, blank=True)
    compressor_type = models.CharField("Тип компрессора", max_length=50, null=True, blank=True)
    split_type = models.CharField("Тип сплита", max_length=50, null=True, blank=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail_brand", kwargs={"category_n": self.category.url,
                                                       "brand_n": self.brand.url,
                                                       "slug": self.url})
        # return reverse("product_detail", kwargs={"id": self.id, "slug": self.url})

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Attributes(models.Model):
    """Атрибуты"""
    product = models.ForeignKey(
        Product, verbose_name="Товар", on_delete=models.CASCADE, null=True, related_name="attr_product"
    )
    name = models.CharField("Название поля атрибута", max_length=100, default="", blank=True)
    value = models.CharField("Значение поля атрибута", max_length=100, default="", blank=True)
    # heat_power = models.CharField("Мощность нагрева", max_length=100, default="", blank=True)
    # power_requirement = models.CharField("Потребляемая мощность", max_length=100, default="", blank=True)
    # operating_mode = models.CharField("Режим работы", max_length=100, default="", blank=True)
    # weight = models.CharField("Вес", max_length=100, default="", blank=True)
    # size = models.CharField("Габариты", max_length=100, default="", blank=True)
    # panel_dimensions = models.CharField("Габариты панели", max_length=100, default="", blank=True)
    # power_supply = models.CharField("Электропитание", max_length=100, default="", blank=True, help_text="В, ф, Гц")
    # refrigerant_pipes = models.CharField("Диаметр труб хладагента", max_length=100, default="", blank=True)
    # noise = models.CharField("Уровень шума", max_length=100, default="", blank=True)
    # served_area = models.CharField("Обслуживаемая площадь", max_length=100, default="", blank=True)
    # refrigerant = models.CharField("Хладагент", max_length=100, default="", blank=True)
    # operating_temperature = models.CharField("Диапазон рабочих температур", max_length=100, default="", blank=True)
    # guarantee = models.CharField("Гарантия", max_length=100, default="", blank=True)
    # air_pressure = models.CharField(
    #     "Напор воздуха", max_length=100, default="", blank=True, help_text="доступное статическое давление"
    # )
    # connected_blocks = models.CharField("Количество подключаемых блоков", max_length=100, default="", blank=True)
    # airflow_rate = models.CharField("Расход воздуха", max_length=100, default="", blank=True)
    # additional_heating = models.CharField("Дополнительный электро нагрев", max_length=100, default="", blank=True)
    # country = models.CharField("Страна производитель", max_length=100, default="", blank=True)
    # amperage = models.CharField("Рабочий ток", max_length=100, default="", blank=True, help_text="А")
    # number_compressors = models.CharField("Количество компрессоров", max_length=100, default="", blank=True)
    # type_compressors = models.CharField("Тип компрессоров", max_length=100, default="", blank=True)
    # fluid_temperature = models.CharField("Температура теплоносителя", max_length=100, default="", blank=True)
    # inverter = models.CharField("Инвертер", max_length=100, default="", blank=True)
    # connection_dimensions = models.CharField(
    #     "Присоединительные размеры водяных патрубков вход/выход", max_length=100, default="", blank=True
    # )
    # fluid_flow = models.CharField("Поток жидкости", max_length=100, default="", blank=True)

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"


class Visitor(models.Model):
    """Посетитель"""
    name = models.CharField("Логин", max_length=130, blank=True)
    ip = models.CharField("IP адрес", max_length=15, default='1.0.0.1')
    password = models.CharField("Пароль", max_length=150, blank=True)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    discount = models.IntegerField(default=0, verbose_name="Персональная скидка")
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    products = models.ManyToManyField('Product', through='CartQuantity', related_name='carts')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая цена')

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def calculate_total_price(self):
        total_price = sum(item.product.price * item.quantity for item in self.cartquantity_set.all())
        self.total_price = total_price
        self.save()

    def get_total_quantity(self):
        return sum(item.quantity for item in self.cartquantity_set.all())

class CartQuantity(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



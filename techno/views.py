import logging
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, authenticate, login
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.http import JsonResponse
from .models import Attributes, Profile, SplitSystem, CartQuantity
from .forms import LoginForm
from rest_framework.decorators import api_view
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from .models import Category, Brand, FilterSettings, Powerr, BlockType
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Product
from django.shortcuts import render
from .models import Category, Brand, Product
from django.shortcuts import render
from .models import Brand

def some_view(request):
    brands_all = Brand.active.all()  # Используем кастомный менеджер
    return render(request, 'index.html', {'brands_all': brands_all})

def product_list(request):
    categories = Category.active.all()  # Получаем только активные категории
    brands = Brand.active.all()         # Получаем только активные бренды
    products = Product.active.all()     # Получаем только активные товары
    return render(request, 'product_list.html', {
        'categories': categories,
        'brands': brands,
        'products': products
    })

@transaction.atomic
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_quantity, created = CartQuantity.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_quantity.quantity = quantity
        else:
            cart_quantity.quantity += quantity
        cart_quantity.save()

    cart.calculate_total_price()

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@transaction.atomic
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_quantity = CartQuantity.objects.get(cart=cart, product=product)
    if cart_quantity.quantity > 1:
        cart_quantity.quantity -= 1
        cart_quantity.save()
    else:
        cart_quantity.delete()
    cart.calculate_total_price()
    return redirect('profile')


def cart_view(request):
    user = User.objects.get(username='admin')
    cart = Cart.objects.get(user=user)
    context = {
        'username': cart.user.username,
        'num_products': cart.cartquantity_set.count(),
    }
    return render(request, 'accounts/profile.html', context)


class ProductViewAll(View):
        """Список товаров"""

        def get(self, request):
            # Получаем состояние фильтров из базы данных
            filter_settings = FilterSettings.objects.first()

            # Получаем список всех категорий и брендов
            categories = Category.objects.all()
            brands_all = Brand.objects.all()
            powerr_all = Powerr.objects.all()
            blocktype_all = BlockType.objects.all()
            splitsystem_all = SplitSystem.objects.all()

            # Получение списка продуктов ( фильтруя черновики )
            products_all = Product.objects.filter(draft=False).order_by('title')

            # Фильтр по типу сплит системы
            if filter_settings and filter_settings.show_splitsystem_filter:
                selected_splitsystem = request.GET.get('SplitSystem')
                if selected_splitsystem:
                    products_all = products_all.filter(SplitSystem__SplitSystem=selected_splitsystem)

            # Фильтр по инвентору
            if filter_settings and filter_settings.show_invertor_filter and request.GET.get('invertor'):
                products_all = products_all.filter(invertor=True)

            # Фильтр мощности
            if filter_settings and filter_settings.show_power_filter:
                selected_powerr = request.GET.get('Powerr')
                if selected_powerr:
                    products_all = products_all.filter(Powerr__NamePower=selected_powerr)

            # Фильтр типа блока
            if filter_settings and filter_settings.show_blocktype_filter:
                selected_blocktype = request.GET.get('BlockType')
                if selected_blocktype:
                    products_all = products_all.filter(BlockType__BlockType=selected_blocktype)

            # Если фильтр по категориям включен, применяем его
            if filter_settings and filter_settings.show_category_filter:
                selected_category = request.GET.get('category')
                if selected_category:
                    products_all = products_all.filter(category__name=selected_category)

            # Если фильтр по брендам включен, применяем его
            if filter_settings and filter_settings.show_brand_filter:
                selected_brand = request.GET.get('brand')
                if selected_brand:
                    products_all = products_all.filter(brand__name=selected_brand)

            # Фильтр по наличию
            if filter_settings and filter_settings.show_availability_filter and request.GET.get('availability'):
                products_all = products_all.filter(availability__gt=0)

            # Фильтр по ценам
            price_min = request.GET.get('price_min')
            price_max = request.GET.get('price_max')
            if price_min and price_max:
                products_all = products_all.filter(price__range=(price_min, price_max))
            elif price_min:
                products_all = products_all.filter(price__gte=price_min)
            elif price_max:
                products_all = products_all.filter(price__lte=price_max)

            per_page = request.GET.get('per_page')
            if per_page:
                if per_page == 'all':
                    # Если пользователь выбрал "Все", показываем все товары
                    paginator = None  # Не используем пагинацию
                    products = products_all
                else:
                    # Иначе ограничиваем количество товаров на странице выбранным значением
                    paginator = Paginator(products_all, int(per_page))
                    page = request.GET.get('page', 1)
                    products = paginator.get_page(page)
            else:
                # По умолчанию показываем 30 товаров на странице
                paginator = Paginator(products_all, 30)
                page = request.GET.get('page', 1)
                products = paginator.get_page(page)

            return render(request, "goods/product_list.html", {
                'categories': categories,
                'brands_all': brands_all,
                'products': products,
                'filter_settings': filter_settings,
                'powerr_all': powerr_all,
                'blocktype_all': blocktype_all,
                'splitsystem_all': splitsystem_all,

            })



def contacts(request):
    brands_all = Brand.objects.all()
    return render(request, "goods/contacts.html", {'brands_all': brands_all})


class SearchResultsView(View):
    def get(self, request):
        categories = Category.objects.all()
        brands_all = Brand.objects.all()
        object_list = []
        query = None
        if 'q' in request.GET:
            query = self.request.GET.get('q')
            object_list = Product.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query), draft=False
            )
        else:
            object_list = Product.objects.filter(draft=False)

        return render(request, 'goods/search_results.html', {'query': query,
                                                             'results': object_list,
                                                             'categories': categories,
                                                             'brands_all': brands_all})

def brand_page(request, brand_name):
    # Получение данных о бренде из базы данных
    brand = Brand.objects.get(name=brand_name)
    context = {
        'brand': brand
    }
    return render(request, 'brand.html', context)

class ProductBrandCategoryDetailView(View):
    """Полное описание товара"""

    def get(self, request, category_n, brand_n, slug):

        # Получение списка всех категорий и брендов для использования в фильтрах
        powerr_all = Powerr.objects.all()
        blocktype_all = BlockType.objects.all()
        splitsystem_all = SplitSystem.objects.all()

        # Получение настроек фильтров
        filter_settings = FilterSettings.objects.first()

        categories = Category.objects.all()
        category_cor_id = Category.objects.get(url=category_n)
        brands = Brand.objects.filter(category=category_cor_id.id)
        brand_cor_id = Brand.objects.get(url=brand_n)
        product = Product.objects.filter(brand_id=brand_cor_id, url=slug, category_id=category_cor_id, draft=False)
        if product.exists():
            product = product.first()
        else:
            response = render(self.request, 'goods/404.html',)
            response.status_code = 404

            return response
        attributes = Attributes.objects.filter(product=product.id)
        brands_all = Brand.objects.all()

        product.number_of_views += 1
        product.save()

        return render(request, "goods/product_detail.html", {'categories': categories,
                                                             'categories': categories,
                                                             'brands_all': brands_all,
                                                             'powerr_all': powerr_all,
                                                             'blocktype_all': blocktype_all,
                                                             'splitsystem_all': splitsystem_all,
                                                             'filter_settings': filter_settings,
                                                             'brand': brand_cor_id,
                                                             'brands_all': brands_all,
                                                             "product": product,
                                                             "attributes": attributes,
                                                             "category": category_cor_id,
                                                             "brands": brands
                                                             })


class CategoryDetailView(View):
    """Отдельное описание категории и вовод брендов этой категории"""


    def get(self, request, slug):
        categories_all = Category.objects.all()
        category = get_object_or_404(Category, url=slug)  # Заменил Category.objects.get на get_object_or_404
        brands = Brand.objects.filter(category=category.id)
        brands_all = Brand.objects.all()
        products_all = Product.objects.filter(category=category.id, draft=False)
        arrts = Attributes.objects.filter(name__contains="Режим работы")


        paginator = Paginator(products_all, 30)
        page_number = request.GET.get('page_number')
        try:
            products = paginator.page(page_number)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, "goods/category_detail.html", {'categories': categories_all,
                                                              "category": category,
                                                              'brands_all': brands_all,
                                                              "brands": brands,
                                                              "products_all" : products,
                                                              "arrts" : arrts,
                                                              'paginator': paginator,
                                                              })


class BrandCategoryDetailView(View):
    def get(self, request, brand_n):
        categories_all = Category.objects.all()
        brands_all = Brand.objects.all()
        brand = get_object_or_404(Brand, url=brand_n)
        category = brand.category.first()  # Предполагая, что бренд имеет хотя бы одну категорию
        products_all = brand.product_brand.all()

        paginator = Paginator(products_all, 30)
        page_number = request.GET.get('page')
        try:
            products = paginator.page(page_number)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, "goods/brand_detail.html", {
            'categories': categories_all,
            'category': category,
            'brands_all': brands_all,
            'brands': category.brand_category.all() if category else [],
            'brand': brand,
            'products': products,
            'all_products_for_count': products_all,
            'page': page_number
        })


logger = logging.getLogger(__name__)


@api_view(["POST"])
def contact_form(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if request.method == 'POST' and is_ajax:
        subject = 'Запрос'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ["iphonemayner@mail.ru"]

        msg_text = ""

        # Логирование всех полученных данных
        logger.debug("Полученные данные POST запроса:")
        for key, value in request.POST.items():
            logger.debug(f"{key}: {value}")

        # Получаем данные из запроса
        for post_param_key, post_param_value in request.POST.items():
            if post_param_key == 'csrfmiddlewaretoken':
                continue
            elif post_param_key == 'subject':
                subject = post_param_value
                continue
            msg_text += f"\n{post_param_key}: {post_param_value}"

        msg = EmailMultiAlternatives(subject, msg_text, from_email, recipient_list)

        # Обработка прикрепленных файлов
        for upload_file in request.FILES.getlist('files[]'):
            image_data = upload_file.read()
            msg.attach(upload_file.name, image_data, 'image/jpeg')

        try:
            msg.send()
            return JsonResponse({'success': True})
        except Exception as e:
            logger.error(f"Ошибка отправки письма: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})


    return JsonResponse({'success': False, 'error': 'Invalid request'})














@login_required(login_url='login')
def me(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile, created = Profile.objects.get_or_create(user=request.user)

    request.user.cart.calculate_total_price()

    return render(request, 'accounts/me.html', {'user': request.user, 'profile': profile})

def doLogout(request):
    logout(request)
    return redirect('login')


class LoginUser(LoginView):
    form_class = LoginForm
    success_url = reverse_lazy('profile')
    template_name = 'accounts/login.html'

class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

def logout_user(request):
    logout(request)
    return redirect('/')

class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'accounts/profile.html')

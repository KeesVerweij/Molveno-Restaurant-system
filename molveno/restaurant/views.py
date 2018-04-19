from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.views import generic, View
from .forms import MenuItemForm, OrderForm, MenuForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin, auth, messages
from .models import *
from django.forms import ModelForm


# We will use class-based views
# TemplateView is a class that renders an html page with django variables in double curly brackets {{ }}

class InventoryPageView(TemplateView):
    # this is a reserved variable that leads to the html template page.
    template_name = "restaurant/inventory.html"


class IndexView(TemplateView):
    template_name = "restaurant/index.html"

    # get overview of all models in our app
    restaurant_app = apps.get_app_config('restaurant')
    restaurant_app_models = restaurant_app.models.values()
    restaurant_app_model_names = [
        model._meta.verbose_name for model in restaurant_app_models]

    # comes out e.g. as 'restaurant.menu_menu_items'
    model_short_names = [
        model._meta.label_lower for model in restaurant_app_models]

    # admin.site._registry is a dictionary with all registered tables
    registered_model_names = [
        key._meta.verbose_name.capitalize() for key in admin.site._registry]

    # replace the dot after the app prefix with a slash, for the url
    model_short_names_as_links = [
        'management/' + short_name.replace('restaurant.', 'restaurant/') + '/' for short_name in model_short_names]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = self.registered_model_names
        context['links'] = self.model_short_names_as_links
        context['title'] = 'Site Administration'
        context['table_title'] = 'Restaurant'

        return context


class MenuAddView(TemplateView):
    template_name = "restaurant/menu-add.html"

    # query to get all items out of menu table
    menu_table = Menu.objects.all()
    print(menu_table)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = self.menu_table
        return context


class MenuChangeView(TemplateView):
    template_name = "restaurant/menu-change.html"
    menu_table = Menu.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = self.menu_table
        return context


class SupplierAddView(TemplateView):
    template_name = "restaurant/supplier-add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SupplierChangeView(TemplateView):
    template_name = "restaurant/supplier-change.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


class MenuItemView(generic.DetailView):
    model = MenuItem
    template_name = 'restaurant/menu_item.html'
    context_object_name = 'menu_item'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        menu_item_addition = get_object_or_404(
            MenuItemAddition, menu_item=self.kwargs['pk'])
        context['selling_price'] = menu_item_addition.selling_price
        context['form'] = MenuItemForm()
        context['table_id'] = self.request.session['table_id']
        # context['error_message'] = self.kwargs['error_message']
        return context


def add_order_view(request, item_id):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            order_amount = int(form.cleaned_data['order_amount'])
            request.session['order_item'] = {
                'id': item_id, 'amount': order_amount}
            return HttpResponseRedirect(reverse('restaurant:orders'))
        else:
            return HttpResponse("Oops! something went wrong!")
    else:
        return HttpResponse("Oops! something went wrong!")


class AddOrderMenu(View):
    def get(self, request, *args, **kwargs):
        '''
        if request method is GET
        '''
        pass

    def post(self, request, *args, **kwargs):
        '''
        if request method is POST
        '''
        return HttpResponseRedirect(reverse('restaurant:orders'))


def orders_view(request):
    table_id = request.session['table_id']  # THIS GIVES AN ERROR WHEN THERE IS NO TABLE ID!
    if request.method == 'POST':
        # if form is submitted, save orders to databaseself.
        message = ""
        for item, amount in request.POST.items():
            if item in request.session['order']:
                message += item + ', ' + amount + '</br>'
                order_item = get_object_or_404(MenuItem, name=item)
                table_id = request.session['table_id']
                for orders in range(int(amount)):
                    order = Order(menu_item=order_item, table_no=table_id,
                                  order_time=datetime.datetime.now())
                    try:
                        order.save()
                    except Exception as e:
                        print(e)
                        messages.error(
                            request, 'There was a problem, your order was not places!')
                        return HttpResponseRedirect(reverse('restaurant:orders'))
        request.session['orderplaced'] = True
        del request.session['order']
        request.session.modified = True
        messages.success(request, 'Your order was placed succesfully!')
        return HttpResponseRedirect(reverse('restaurant:orders'))
    else:
        # otherwise render the order page.
        context = {}
        if request.session.get('order_item'):
            # there will not always be an order item to add!
            order_item = request.session['order_item']
            item = get_object_or_404(MenuItem, pk=order_item['id'])
            if request.session.get('order'):
                order = request.session['order']
                if item.name in order:
                    messages.success(
                        request, 'Your order was updated succesfully!')
                else:
                    messages.success(
                        request, 'Your order was added succesfully!')
                order[item.name] = order_item['amount']
                request.session['order'] = order

                print("order session variable updated")
            else:
                order = {item.name: order_item['amount']}
                request.session['order'] = order
                print("order session variable made")
                messages.success(request, 'Your order was added succesfully!')
            del request.session['order_item']
            request.session.modified = True

        if request.session.get('order'):
            '''
            if orders have been placed before
            '''
            order = request.session['order']
            '''
            get the combined price for the amount of menu items (eg 3x carpaccio = €27 total) as
            well as the overall totall of all orders and put them in a dictionary to be passed to
            the form {menu_item: {'price': price, 'amount': amount}, ... }
            '''
            total = 0
            form_data = dict()
            for item in order:
                amount = order[item]
                # print('AMOUNT: ' + str(amount))
                item_id = MenuItem.objects.values().filter(name=item)[0]['id']
                item_price = MenuItemAddition.objects.values().filter(menu_item=item_id)[
                    0]['selling_price']
                combined_price = item_price * amount
                form_data[item] = {'amount': amount,
                                   'price': str(combined_price)}
                total += combined_price
            form = OrderForm(form_data)
            context['orders'] = order
            context['total'] = total
            context['form'] = form
        else:
            if request.session.get('orderplaced'):
                del request.session['orderplaced']
                request.session.modified = True

        get_orders = Order.objects.filter(table_no=table_id)
        if(get_orders):
            placed_orders = dict()
            total_price = 0
            for order in get_orders:
                item_name = order.menu_item.name
                price_addition = MenuItemAddition.objects.filter(
                    menu_item=order.menu_item)
                selling_price = price_addition.values_list(
                    'selling_price', flat=True)[0]
                total_price += selling_price
                if item_name not in placed_orders:
                    placed_orders[item_name] = {
                        'selling_price': selling_price, 'amount': 1}
                else:
                    placed_orders[item_name]['amount'] += 1
                    placed_orders[item_name]['selling_price'] += selling_price
            context['placed_orders'] = placed_orders
            context['total_pice'] = total_price

        context['table_id'] = table_id
        return render(request, 'restaurant/orders.html', context)


class MenuCardList(TemplateView):
    template_name = "restaurant/menucard_list.html"

    def get_course_types(self):
        types = [i for i in CourseType.objects.all()]
        return types

    def get_queryset_items(self):
        course_types = self.get_course_types()
        course_type_lists = []

        i = 0
        for course_type in course_types:
            i += 1
            c = MenuItemAddition.objects.filter(menu_item__course_type=i)
            course_type_lists.append(c)

        return course_type_lists

    def get_queryset_menus(self):
        return MenuAddition.objects.all()

    def get_menu_items_on_menus(self):
        menus = self.get_queryset_menus()

        menu_courses_list = []
        i = 0
        for menu in menus:
            i += 1
            d = [m for m in menu.menu.menu_items.all()]
            # menu_courses_list.append(d)
            # print(d)
        # print("menu course list:", menu_courses_list)

        # for menu in menus_courses_list:
        #     courses = self.get_course_types()
        #     for dish in menu:
        #         # sort the list based on course type
        #         pass
        #     pass

        return d

    def get_table_id(self, **kwargs):
        table_id = self.kwargs['table_id']
        return table_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menucard_list'] = self.get_queryset_items()
        context['course_types'] = self.get_course_types()
        context['menu_types'] = self.get_queryset_menus()
        context['table_id'] = self.get_table_id()
        context['menu_courses'] = self.get_menu_items_on_menus()
        self.request.session['table_id'] = self.get_table_id()
        return context


class MenuView(TemplateView):
    template_name = 'restaurant/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_id = context['pk']
        menu = self.get_menu(menu_id)[0]
        form = MenuForm()
        context['form'] = form
        context['menu'] = menu
        return context

    def get_menu(self, pk):
        return MenuAddition.objects.filter(menu=pk)


class DrinksList(TemplateView):
    template_name = "restaurant/entry.html"

    def get_drinks_query(self):
        drinks_list = MenuItemAddition.objects.filter(
            menu_item__menu_item_type=4)
        return drinks_list

    def get_table_id(self, **kwargs):
        table_id = self.kwargs['table_id']
        return table_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drinks_list'] = self.get_drinks_query()
        self.request.session['table_id'] = self.get_table_id()
        return context


def request_waiter(request):
    table_id = request.session['table_id']
    context = {"table_id": table_id}
    return render(request, 'restaurant/waiter.html', context)

from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.views import generic
from .forms import MenuItemForm, OrderForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin, auth
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
    restaurant_app_model_names = [model._meta.verbose_name for model in restaurant_app_models]

    # comes out e.g. as 'restaurant.menu_menu_items'
    model_short_names = [model._meta.label_lower for model in restaurant_app_models]

    # admin.site._registry is a dictionary with all registered tables
    registered_model_names = [key._meta.verbose_name.capitalize() for key in admin.site._registry]

    # replace the dot after the app prefix with a slash, for the url
    model_short_names_as_links = [
        'management/'+short_name.replace('restaurant.', 'restaurant/') + '/' for short_name in model_short_names]

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
            request.session['order_item'] = {'id': item_id, 'amount': order_amount}
            return HttpResponseRedirect(reverse('restaurant:orders'))
        else:
            return HttpResponse("Oops! something went wrong!")
    else:
        return HttpResponse("Oops! something went wrong!")


def orders_view(request):
    table_id = request.session['table_id']

    if request.session.get('order'):
        '''
        if orders have been placed before
        '''
        order = request.session['order']
        message = False
    else:
        order = False
        message = "no items added to your order yet!"

    if request.session.get('order_item'):
        # there will not always be an order item!
        order_item = request.session['order_item']
        item = get_object_or_404(MenuItem, pk=order_item['id'])
        if request.session.get('order'):
            order = request.session['order']
            order[item.name] = order_item['amount']
            request.session['order'] = order

            print("order session variable updated")
        else:
            order = {item.name: order_item['amount']}
            request.session['order'] = order
            print("order session variable made")
        del request.session['order_item']
        request.session.modified = True
        message = item.name + " " + str(order_item['amount']) + "x added to order!"
    form = OrderForm(orders=order)
    context = {
        'orders': order,
        'form': form,
        'message': message,
        'table_id': table_id
    }

    return render(request, 'restaurant/orders.html', context)


def ConfirmOrderView(request, item_id):
    order_item = get_object_or_404(MenuItem, pk=item_id)
    order_amount = int(request.POST.get('order_amount'))
    table_id = request.session['table_id']
    if order_amount and table_id:
        for orders in range(order_amount):
            order = Order(menu_item=order_item, table_no=table_id)
            try:
                order.save()
            except Exception as e:
                print(e)
                return HttpResponse("<h1>There was a problem. Item not saved.</h1>")

        return HttpResponse("you ordered " + order_item.name + " " +
                            str(order_amount) +
                            " times for table " + str(table_id) + "<br>" +
                            "<h1>Item successfully saved</h1>")
    else:
        # Redisplay the menu item: "No amount chosen"
        return HttpResponse("<h1>You didn't select an order amount</h1>")


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
            print('current course type: ', course_type)
            c = MenuItemAddition.objects.filter(menu_item__course_type=i)
            course_type_lists.append(c)
            for dish in c:
                # course_type_lists.append(dish)
                print(dish.menu_item)
                print(dish.selling_price)

        return course_type_lists

    def get_queryset_menus(self):
        return MenuAddition.objects.all()

    def get_table_id(self, **kwargs):
        table_id = self.kwargs['table_id']
        return table_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menucard_list'] = self.get_queryset_items()
        context["course_types"] = self.get_course_types()
        context['menu_types'] = self.get_queryset_menus()
        context['table_id'] = self.get_table_id()
        self.request.session['table_id'] = self.get_table_id()
        return context

from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views import generic
from .models import MenuItem
from .models import MenuItemAddition
from .models import Order
from .forms import AddOrderForm
from django.http import HttpResponse
from .models import MenuCard
from .models import MenuAddition
from .models import CourseType


class InventoryPageView(TemplateView):
    # this is a reserved variable that leads to the html template page.
    template_name = "restaurant/inventory.html"


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
        context['form'] = AddOrderForm()
        context['table_id'] = self.request.session['table_id']
        # context['error_message'] = self.kwargs['error_message']
        return context


def AddOrderView(request, item_id):
    order_item = get_object_or_404(MenuItem, pk=item_id)
    order_amount = int(request.POST.get('order_amount'))
    table_id = request.session['table_id']
    if order_amount and table_id:
        # Always return an HttpResponseRedirect after successfully
        # dealing with POST data. This prevents data from being posted
        # twice if a user hits the Back button.
        # return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
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

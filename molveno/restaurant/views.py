from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views import generic
from .models import MenuItem
from .models import MenuItemAddition
from .models import Order
from .forms import AddOrderForm
from django.http import HttpResponse


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
        self.request.session['table_id'] = 1

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

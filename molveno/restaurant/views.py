from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import generic
from .models import MenuCard
from .models import MenuItemAddition
from .models import MenuAddition
from .models import MenuItem
from .models import CourseType

# We will use class-based views
# TemplateView is a class that renders an html page with django variables in double curly brackets {{ }}

class InventoryPageView(TemplateView):

    # this is a reserved variable that leads to the html template page.
    template_name = "restaurant/inventory.html"


class MenuCardList(TemplateView):
    template_name="restaurant/menucard_list.html"

    def get_course_types(self):
        types=[i for i in CourseType.objects.all()]
        return types

    def get_queryset_items(self):
        course_types = self.get_course_types()
        course_type_lists = []

        i = 0
        for course_type in course_types:
            i += 1
            print('current course type: ', course_type)
            c = MenuItemAddition.objects.filter(menu_item__course_type = i)
            course_type_lists.append(c)
            for dish in c:
                # course_type_lists.append(dish)
                #print(dish.menu_item)
                #print(dish.selling_price)

        return course_type_lists

    def get_queryset_menus(self):
        return MenuAddition.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menucard_list'] = self.get_queryset_items()
        context["course_types"] = self.get_course_types()
        context['menu_types'] = self.get_queryset_menus()
        return context

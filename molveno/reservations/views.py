from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import re

# Create your views here.
class IndexView(TemplateView):
    template_name = "reservations/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['variable'] = self.value
        return context

    def validate_email(self, email):
         if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None:
             return True
         return False

    def get(self,request,*args,**kwargs):
        #check availability
        context = super().get_context_data(**kwargs)

        if "date" in request.GET:
            responses_for_customer = [ "Our restaurant is closed on this date.",
                                        "Our restaurant has no free tables at the selected time. Please try another timeslot.",
                                        "Selected date & time are available!"]
            page_actions = ["request_another_date",
                            "request_another_time",
                            "request_booking_confirmation"]

            selected_date = ""
            selected_time_hours = "12"
            selected_time_minutes = "00"
            selected_num_people = "2"
            first_name = ""
            last_name = ""
            email = ""
            phone = ""

            if "date" in request.GET:
                selected_date = request.GET["date"]
            if "time-hour" in request.GET:
                selected_time_hours = request.GET["time-hour"]
            if "time-minutes" in request.GET:
                selected_time_minutes = request.GET["time-minutes"]
            if "people" in request.GET:
                selected_num_people = request.GET["people"]
            if "email" in request.GET:
                email = request.GET["email"]
            if "phone" in request.GET:
                phone = request.GET["phone"]
            if "first_name" in request.GET:
                first_name = request.GET["first_name"]
            if "last_name" in request.GET:
                last_name = request.GET["last_name"]

            email_valid = False
            if self.validate_email(email) == True:
                email_valid = True



            variable_content = {"response":responses_for_customer[2],
                                "page_action":page_actions[2],
                                "selected_date":selected_date,
                                "selected_time_hours":selected_time_hours,
                                "selected_time_minutes":selected_time_minutes,
                                "selected_num_people":selected_num_people,
                                "email":email,
                                "email_valid":email_valid,
                                "phone":phone,
                                "selected_num_people":selected_num_people,
                                "first_name":first_name,
                                "last_name":last_name}

            return render(request, IndexView.template_name, variable_content)
        return render(request, self.template_name)

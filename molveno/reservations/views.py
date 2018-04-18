from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Reservation
from .models import Table

from datetime import datetime
from time import strptime
import re

# Create your views here.
class IndexView(TemplateView):
    template_name = "reservations/index.html"
    confirmation_page = "reservations/confirmation.html"

    def __init__(self):
        self.reservation_concept = Reservation()
        self.reservation_tables = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['variable'] = self.value
        print('context data called')
        return context

    def validate_email(self, email):
         if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None:
             return True
         return False

    def save_reservation(self):
        self.reservation_concept.save()
        self.reservation_concept.tables.add(self.reservation_tables)


    def post(self,request,*args,**kwargs):
        #check availability
        context = super().get_context_data(**kwargs)

        if "reservation_check" in request.POST:
            print('this is a check only')
            responses_for_customer = [ "Our restaurant is closed on this date.",
                                        "Our restaurant has no free tables at the selected time. Please try another timeslot.",
                                        "Selected date & time are available!"]
            page_actions = ["request_another_date",
                            "request_another_time",
                            "request_booking_confirmation"]
            self.collect_reservation_data_from_post_request(request)
            self.format_reservation(request)

            email_valid = True if self.validate_email(self.email) == True else False

            variable_content = {"response":responses_for_customer[2],
                                "page_action":page_actions[2],
                                "selected_date":self.selected_date,
                                "selected_time_hours":self.selected_time_hours,
                                "selected_time_minutes":self.selected_time_minutes,
                                "selected_num_people":self.selected_num_people,
                                "email":self.email,
                                "email_valid":email_valid,
                                "phone":self.phone,
                                "selected_num_people":self.selected_num_people,
                                "first_name":self.first_name,
                                "last_name":self.last_name,
                                "remark":self.remark}

            return render(request, IndexView.template_name, variable_content)

        elif "reservation_confirmation" in request.POST:
            # check again if all is available
            self.collect_reservation_data_from_post_request(request)
            self.format_reservation(request)
            self.save_reservation()
            return render(request, self.confirmation_page)
        else:
            return render(request, self.template_name)

    def collect_reservation_data_from_post_request(self,request):
        self.selected_date = request.POST.get("date","")
        self.selected_time_hours = request.POST.get("time-hour","12")
        self.selected_time_minutes = request.POST.get("time-minutes","00")
        self.selected_num_people = request.POST.get("people", "2")
        self.email = request.POST.get("email","")
        self.phone = request.POST.get("phone","")
        self.first_name = request.POST.get("first_name","")
        self.last_name = request.POST.get("last_name","")
        self.remark = request.POST.get("remark","")

    def format_reservation(self,request):
        reservation_name = self.first_name + " " + self.last_name
        reservation_day = int(self.selected_date[:2])
        reservation_month = strptime(self.selected_date[3:6],'%b').tm_mon
        reservation_year = int(self.selected_date[7:11])
        reservation_hour = int(self.selected_time_hours)
        reservation_minutes = int(self.selected_time_minutes)

        reservation_start_datetime = datetime(reservation_year,reservation_month,reservation_day, reservation_hour, reservation_minutes)
        reservation_end_datetime = datetime(reservation_year,reservation_month,reservation_day, reservation_hour+3, reservation_minutes)

        reservation_guests = int(self.selected_num_people)
        reservation_duration = 180
        reservation_special_request = self.remark
        reservation_tables = Table.objects.get(pk=1)


        self.reservation_concept = Reservation( name=reservation_name,
                                                num_guests=reservation_guests,
                                                start_date_time=reservation_start_datetime,
                                                end_date_time=reservation_end_datetime,
                                                special_request=reservation_special_request,)

        self.reservation_tables = reservation_tables
        print(self.reservation_concept)



class ConfirmationView(TemplateView):
    print('confirmation')

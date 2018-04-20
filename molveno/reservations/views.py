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
        self.reservation_checker = ReservationChecker()
        self.reservation_table = None


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

    def post(self,request,*args,**kwargs):
        #check availability
        context = super().get_context_data(**kwargs)

        if "reservation_check" in request.POST:
            print('this is a check only')
            response_for_customer_options = [ "Our restaurant is closed on this date.",
                                        "Our restaurant has no free tables for this number of guests at the selected time.",
                                        "The selected date and time are available! Please confirm your booking."]

            page_actions = ["request_another_date",
                            "request_another_time",
                            "request_booking_confirmation"]
            self.collect_reservation_data_from_post_request(request)
            self.format_reservation(request)

            datetime_valid = self.future_datetime(self.reservation_concept.start_date_time)

            email_valid = self.validate_email(self.email)
            #print('dt',datetime(self.reservation_concept.start_date_time))

            reservation_table = self.reservation_checker.check_reservation_possible(self.selected_num_people,
                                                                                        self.reservation_concept.start_date_time,
                                                                                        self.reservation_concept.end_date_time)
            if reservation_table:
                response_for_customer = response_for_customer_options[2]
                page_action = page_actions[2]
            else:
                response_for_customer = response_for_customer_options[1]
                page_action = page_actions[1]

            variable_content = {"response":response_for_customer,
                                "page_action":page_action,
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

    def future_datetime(self, rdatetime):
        return rdatetime >= datetime.now()

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
        reservation_special_request = self.remark
        reservation_table = self.reservation_checker.check_reservation_possible(reservation_guests,
                                                                                reservation_start_datetime,
                                                                                reservation_end_datetime)
        print('table in concept:',reservation_table)


        self.reservation_concept = Reservation( name=reservation_name,
                                                num_guests=reservation_guests,
                                                start_date_time=reservation_start_datetime,
                                                end_date_time=reservation_end_datetime,
                                                special_request=reservation_special_request,
                                                table=reservation_table)

        self.reservation_table = reservation_table
        print(self.reservation_concept)


class ReservationChecker:
    def __init__(self):
        pass

    def get_reservations_for_day(self, start_datetime, end_datetime):
        # smarter would be to check for the start time instantly
        # filter range : endtime >=
        try:
            # any reservations that overlap should remain, as their table numbers have to be checked.
            # overlap means:
            # their start datetime falls between start_datetime and end_datetime OR
            # their end datetime falls between start_time and end_time
            # for OR use Q - objects
            reservations1 = Reservation.objects.filter(start_date_time__range=(start_datetime,end_datetime))
        except Reservation.DoesNotExist:
            reservations1 = None

        try:
            reservations2 = Reservation.objects.filter(end_date_time__range=(start_datetime,end_datetime))
        except Reservation.DoesNotExist:
            reservations2 = None

        print('reservations that start in this range:',reservations1)
        print('reservations that end in this range:',reservations2)

        reservations = reservations1 | reservations2

        return reservations

    def filter_time_span(self, reservations, start_time, end_time):
        reservations.filter(start_date_time)
        filtered_reservations = None
        return filtered_reservations

    def check_reservation_possible(self, num_guests, start_date_time, end_date_time):
        # retrieve all reservations for date, so that these tables can be excluded
        #print('checking',start_date_time,end_date_time)
        reservations = self.get_reservations_for_day(start_date_time, end_date_time)
        print('reservations for ',start_date_time,":",reservations)

        try:
            available_tables = set(Table.objects.all())
        except Table.DoesNotExist:
            available_tables = None

        print('all tables:')
        for t in available_tables:
            print(t)

        if reservations and available_tables:
            for r in reservations:
                if r.table:
                    if t in available_tables:
                        available_tables.remove(t)
        else:
            # no reservations yet
            pass

        print('still available:')
        for t in available_tables:
            print(t)

        #with available tables, calculate what's possible
        resulting_table = self.find_exact_table_match(num_guests, available_tables)
        if not resulting_table:
            resulting_table = self.find_larger_table_match(num_guests, available_tables)

        print('result:',resulting_table)

        return resulting_table

    def find_exact_table_match(self, persons, tables):
        # tables = list
        print('guests:',persons,"; received table options:",tables)
        for t in tables:
            if int(t.capacity) == int(persons):
                return t

    def find_larger_table_match(self, persons, tables):
        #print('finding a larger match')
        #print('received these options for iteration: ',tables)
        table_list = [t for t in tables]
        table_list.sort(key=self.sort_by_capacity)
        #print('sorted tables by capacity:',table_list)
        for t in tables:
            #print('iterating... cap:',t.capacity)
            if int(t.capacity) > int(persons):
                return t

    def sort_by_capacity(self,x):
        return x.capacity







class ConfirmationView(TemplateView):
    print('confirmation')

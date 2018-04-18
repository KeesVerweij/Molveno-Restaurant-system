from django.db import models

class Table(models.Model):
    '''contains properties for each table in the restaurant '''

    # unique table number
    table_number = models.PositiveIntegerField(unique=True)

    # capacity (number of guests that can be seated on this table)
    capacity = models.PositiveIntegerField(default=2)

    def __str__(self):
        return "Table " + str(self.table_number) + " - " + str(self.capacity) + " persons"

class Reservation(models.Model):
    ''' contains all reservations '''

    # guest name
    name = models.CharField(max_length=200,default="")

    # number of guests
    num_guests = models.PositiveIntegerField(default=0, verbose_name="Guests")

    # date & start time
    start_date_time = models.DateTimeField(verbose_name="Start")

    # duration in minutes
    end_date_time = models.DateTimeField(verbose_name="End")

    # any special requests
    special_request = models.TextField(blank=True)

    # associated table(s)
    tables = models.ManyToManyField(Table)

    def __str__(self):
        timezonelocal = 'Europe/Amsterdam'
        return "Reservation for " + str(self.num_guests) + " people on " + self.start_date_time.strftime("%d-%m-%Y, %H:%M") + " - " + self.end_date_time.strftime("%H:%M")

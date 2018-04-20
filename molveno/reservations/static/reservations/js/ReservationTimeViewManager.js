function ReservationTimeViewManager(date, selectedDate openingHours, closingHours){
  //date is the current assumed time, taking date into account
  this.date = date;
  this.year = date.getFullYear();
  this.month = date.getMonth();
  this.day = date.getDay();
  this.hours = date.getHours();
  this.minutes = date.getMinutes();

  this.openingHours = openingHours;
  this.closingHours = closingHours;

  this.minuteValues = ["00", "15", "30", "45"];

  this.startMinutesIndex = 0;

  this.resultYear = "";
  this.resultMonth = "";
  this.resultDay = "";
  this.resultHours = "";
  this.resultMinutes = "";

  this.nextDayDisplay = false;

  this.init = function() {
    this.startHours = this.openingHours;
    this.endHours = this.closingHours;
    var today = new Date();
    if(this.date.getDate() == today.getDate() &&
    this.date.getMonth() == today.getMonth() &&
    this.date.getFullYear() == today.getFullYear()) {
      console.log("today");
      if(this.hours < this.startHours) {
        console.log("flow: morning");
        this.startMinutesIndex = 0;
      } else if (this.hours == today.getHours()) {
        console.log("flow: this hour");
        this.startHours = this.hours;
        this.startMinutesIndex = (Math.floor(((this.minutes) % 60)/15) + 1)%4;
        if (this.minutes >= 45) {
          this.startHours++;
        }
      } else if(this.hours < this.endHours){
        console.log("flow: after this hour, before closing");
        this.startHours = today.getHours();
        this.startMinutesIndex = 0;
      } else if (this.hours >= this.closingHours){
        console.log("flow: after closing");
        this.nextDayDisplay = true;
      }
    } else{
      console.log("another date");
      this.startHours = this.openingHours;
      this.startMinutesIndex = 0;
      this.nextDayDisplay = false;
    }

  };
  this.init();

  this.getNextHoursAsHTML = function(){
    this.resultHours = "";
    for(var i = this.startHours; i <= this.endHours; i++){
        this.resultHours += '<option value="' + i +'">' + i + '</option>';
    }
    return this.resultHours;
  }

  this.getNextMinutesAsHTML = function() {
    this.resultMinutes = "";
    for(var i = this.startMinutesIndex; i < 4; i++){
        this.resultMinutes += '<option value="' + this.minuteValues[i] +'">' + this.minuteValues[i] + '</option>';
    }
    return this.resultMinutes;
  }
  this.getFirstMinutesAsHTML = function() {
    this.resultMinutes = '<option value="' + this.minuteValues[0] +'" selected>' + this.minuteValues[0] + '</option>';
    return this.resultMinutes;
  }
  this.getAllMinutesAsHTML = function() {
    this.resultMinutes = "";
    for(var i = 0; i < 4; i++){
        this.resultMinutes += '<option value="' + this.minuteValues[i] +'">' + this.minuteValues[i] + '</option>';
    }
    return this.resultMinutes;
  }

  this.getDisplayDate = function(){
    //this.startHours == this.openingHours
    var d;
    if(this.nextDayDisplay === true) {
      console.log('next day');
      d = new Date(this.date);
      d.setDate(d.getDate()+1);
      return new Date(this.date.setDate(this.day + 1));

    } else {
      return this.date;
    }
  }

  this.updateTime = function(date){
    this.year = date.getFullYear();
    this.month = date.getMonth();
    this.day = date.getDay();
    this.hours = date.getHours();
    this.minutes = date.getMinutes();
    this.init();
  }
}

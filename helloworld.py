import webapp2
import cgi

form = """
<form method="post"> 
    What is your birthday?
    <br>
    <label> Month
        <input type="text" name="month" value="%(month)s">
    </label> 
    <label> Day
        <input type="text" name="day" value="%(day)s">
    </label> 
    <label> Year
        <input type="text" name="year" value="%(year)s">
    </label> 
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""


class MainPage(webapp2.RequestHandler):
    def write_form(self, error = "", month = "", day = "", year = ""):
        self.response.out.write(form % {"error": error, 
            "month": cgi.escape(month),
            "day": cgi.escape(day), 
            "year": cgi.escape(year)})

    def get(self):

        # self.response.headers["Content-Type"] = "text/plain"
        self.write_form()

    def post(self):

        user_month = self.request.get("month")
        user_day = self.request.get("day")
        user_year = self.request.get("year")
        
        month = self.valid_month(user_month)
        day = self.valid_day(user_day)
        year = self.valid_year(user_year)
        
        if not (month and day and year):
            self.write_form("The date input is not valid!", 
                    user_month, user_day, user_year)
        else:
            self.redirect("/thanks")

    def valid_month(self, month):
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        month_abbvs = dict((m[:3].lower(), m) for m in months)
        if month:
            month = month[:3].lower()
            return month_abbvs.get(month)


    def valid_day(self, day):
        if day and day.isdigit():
            day = int(day)
            if day in range(1, 32):
                return day


    def valid_year(self, year):
        if year and year.isdigit():
            year = int(year)
            if year in range(1901, 2020):
                return year


class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([("/", MainPage), ("/thanks", ThanksHandler)], debug=True)



from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

import simplejson as json
import csv
import re

def convert_month(num):
    try:
        num = int(num)
    except ValueError:
        return(False)
    
    months = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]
    return(months[num - 1])

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "tracker_app/index.html")
    else:
        return redirect(reverse("login_view"))

def login_view(request):
    if request.method == "GET":
        logout(request)
        return render(request, "tracker_app/login.html")

    # POST REQUEST
    else:
        logout(request)
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse("index"))
        else:
            messages.error(request, "Invalid Credentials")
            return redirect(reverse("login_view"))


def logout_view(request):
    logout(request)
    return redirect(reverse("login_view"))

def register(request):
    if request.method == "GET":
        logout(request)
        return render(request, "tracker_app/register.html")
    
    # POST REQUESTS
    username = request.POST.get("username", "")
    email = request.POST.get("email", "")
    password = request.POST.get("password", "")
    confirm_pw = request.POST.get("confirm_pw", "")

    # check for empty fields
    if "" in {username, email, password, confirm_pw}:
        messages.error(request, "All fields are required")
        return redirect(reverse("register"))

    # check for password that do not match
    if password != confirm_pw:
        messages.error(request, "Passwords do not match")
        return redirect(reverse("register"))
    
    # check that email address is in a correct format NOTE: Not a full proof regex
    regex = re.compile(r".+@.+\.[A-Za-z]{2,4}")
    if not regex.match(email):
        messages.error(request, "Invalid Email")
        return redirect(reverse("register"))

    # create new user
    new_user = User.objects.create_user(username, email, password)
    new_user.save()
    messages.success(request, "Account created!")
    return redirect(reverse("login_view"))

@login_required
def view_hours(request):
    table_type = request.GET.get("table_type", None)
    if table_type == None:
        return HttpResponse(json.dumps({"status": "error"}))
    file_name = request.user.username + "_" + table_type + ".csv"

    try:
        with open(file_name, "r") as f:
            reader = csv.reader(f)
            headings = next(reader)
            user_hours = [row for row in reader]
    except FileNotFoundError:
        messages.error(request, "No Data Found")
        user_hours = False
        headings = False
    
    context = {
        "headings": headings,
        "hours": user_hours,
        "table_type": table_type,
    }
    return render(request, "tracker_app/view-hours.html", context)

@login_required
def log_data(request):
    # gather user data, set "default" variables
    data = json.loads(request.body)
    devisor = 1
    data_set = {data["date"], data["hours"], data["obs_time"]}
    file_header = ["DATE", "HOURS WORKED", "HOURS OBSERVED", "SUPERVISOR"]

    # customize which fields need to be validated, as well as file to write to
    if data["form_type"] == "day":
        data_set = {data["date"], data["hours"], data["obs_time"], data["supervisor"]}
        file_end = "_daily.csv"
        devisor = 60
    elif data["form_type"] == "week":
        file_end = "_weekly.csv"
        file_header.pop()
    elif data["form_type"] == "month":
        file_end = "_monthly.csv"
        file_header[0] = "MONTH"
        file_header.insert(0, "YEAR")
        file_header.pop()
    else:
        return HttpResponse(json.dumps({"status": "error", "message": "Data Transfer Error: Unexpected form_type value"}))
       
    # check for empty fields
    if "" in data_set:
        return HttpResponse(json.dumps({"status": "error", "message": "All fields are required"}))

    # check for proper data format | regex modified from https://www.regextester.com/96683
    regex = re.compile(r"([12]\d{3})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])")
    if not regex.match(data["date"]):
        return HttpResponse(json.dumps({"status": "error", "message": "Invalid date format"}))

    # check for proper min/hours format
    try:
        session_hours = int(data["hours"])
        obs_time = round((int(data["obs_time"]) / devisor), 2)
    except ValueError:
        return HttpResponse(json.dumps({"status": "error", "message": "Invalid time format"}))

    # check ensure obs time is less then session hours 
    if session_hours < obs_time:
        return HttpResponse(json.dumps({"status": "error", "message": "Observation time too long"}))

    # open file, check for empty
    try:
        f = open(request.user.username + file_end, "r", newline="")
    except FileNotFoundError:
        empty = True
    else:
        empty = False
        f.close()

    # prepare data to write
    file_data = [data["date"], session_hours, obs_time, data["supervisor"]]
    if data["form_type"] == "day":
        pass
    if data["form_type"] == "week":
        file_data.pop()
    elif data["form_type"] == "month":
        year = regex.search(data["date"]).group(1)
        month = regex.search(data["date"]).group(2)
        file_data.pop()
        file_data[0] = convert_month(month)
        file_data.insert(0, year)
    
    print(file_data)
    # write data to file
    with open(request.user.username + file_end, "a", newline="") as f:
        writer = csv.writer(f)
        if empty:
            writer.writerow(file_header)
        writer.writerow(file_data)

    return HttpResponse(json.dumps({"status": "success", "message": "Data Logged Successfully"}))

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import models
from django.http import HttpResponse

import simplejson as json
import csv
import re

from . import helper
"""-------------------------------------------------------------------------"""
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
    
    # check that email address is in a correct format
    # NOTE: Not a full proof regex
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
def view_hours(request, table_type):
    # Set prepare proper Models
    
    if table_type == "daily":
        log = models.Daily_log
    elif table_type == "monthly":
        log = models.Monthly_log
    else:
        context = {
            "headings": False,
            "data": False,
            "message": "Error: Incorrect URL Path :|",
            "table_type": "No Such Table"
        }
        return render(request, "tracker_app/view-hours.html", context)

    # get user's data from table
    try:
        if table_type == "daily":
            user_data = log.objects.filter(
                user_id=request.user.id).order_by("date").values(
                    "id", "date", "session_hours",
                    "observed_hours", "supervisor"
                )
        else:
            user_data = log.objects.filter(
                user_id=request.user.id).order_by("year", "month").values(
                    "id", "year", "month",
                    "session_hours", "observed_hours"
                )
    # check if no data can be found
    except log.DoesNotExist:
        user_data = False
        headings = False

    # convert monthly log month indexs to their string form
    id_list = []
    for row in user_data:
        if table_type == "monthly":
            row["month"] = helper.convert_month(row["month"])
        id_list.append(row["id"])
        del row["id"]
    
    zipped_data = zip(id_list, user_data)

    # prepare headings for template replacement
    headings = [key.upper().replace("_", " ") for key in user_data[0].keys()]

    # create context
    context = {
        "headings": headings,
        "data": zipped_data,
        "message": "No Data Found :(",
        "table_type": table_type
    }
    return render(request, "tracker_app/view-hours.html", context)

@login_required
def log_data(request, log_type):
    # get POST DATA, prepare initial variables for monthly
    request_data = json.loads(request.body)
    devisor = 1
    data_set = {
        request_data["date"], 
        request_data["hours"],
        request_data["obs_time"]
    }

    # customize required fields
    if log_type == "day":
        data_set = {
            request_data["date"],
            request_data["hours"],
            request_data["obs_time"],
            request_data["supervisor"]
        }
        devisor = 60
       
    # check for empty fields
    if "" in data_set:
        return HttpResponse(json.dumps({
            "status": "error",
            "message": "All fields are required"
        }))

    
    # regex modified from https://www.regextester.com/96683
    regex = re.compile(
        r"([12]\d{3})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])"
    )

    # check for proper data format
    if not regex.match(request_data["date"]):
        return HttpResponse(json.dumps({
            "status": "error",
            "message": "Invalid date format"
        }))

    # check for proper min/hours format
    try:
        session_hours = int(request_data["hours"])
        obs_time = round((int(request_data["obs_time"]) / devisor), 2)
    except ValueError:
        return HttpResponse(json.dumps({
            "status": "error",
            "message": "Invalid time format"
        }))

    # check ensure observation time is less then session hours 
    if session_hours < obs_time:
        return HttpResponse(json.dumps({
            "status": "error",
            "message": "Observation time too long"
        }))

    # ----------- Log User Data in Daily Table --------- #
    if log_type == "day":
        # add data to daily log
        new_log = models.Daily_log(
            user_id=models.User.objects.get(pk=request.user.id),
            date=request_data["date"],
            session_hours=session_hours,
            observed_hours=obs_time,
            supervisor=request_data["supervisor"]
        )

        try:
            new_log.save()
        except:
            # error if date is not unique
            return HttpResponse(json.dumps({
                "status": "error",
                "message": "This date has already been logged."
            }))

        # update monthly log if possible
        month = int(regex.search(
            request_data["date"]).group(2))
        year = regex.search(request_data["date"]).group(1)

        # check if corresponding date exists
        try:
            current_month_log = models.Monthly_log.objects.get(
                month=month, 
                year=year
            )

        # create new month log if None exists
        except models.Monthly_log.DoesNotExist:
            print("No month row for this date")
            new_month_log = models.Monthly_log(
                user_id=models.User.objects.get(pk=request.user.id),
                year=year,
                month=month,
                session_hours=session_hours,
                observed_hours=obs_time,
                mutable=True,
            )
            # save new row
            try:
                new_month_log.save()
            except:
                return HttpResponse(json.dumps({
                    "status": "unknown error",
                    "message": "Monthly log could not be updated."
                }))
        else:
            print("There is already row for this date")
            # check if row is currently mutable
            if current_month_log.mutable:
                # update hours
                current_month_log.session_hours = round(
                    float(current_month_log.session_hours) + session_hours, 2
                )
                current_month_log.observed_hours = round(
                    float(current_month_log.observed_hours) + obs_time, 2
                )
                # save update
                current_month_log.save()
            else:
                print("cannot update this data")

    # ----------- Log User Data in the Monthly Table --------- #
    else:
        # add data to monthly log
        new_log = models.Monthly_log(
            user_id=models.User.objects.get(pk=request.user.id),
            month=int(regex.search(request_data["date"]).group(2)),
            year=regex.search(request_data["date"]).group(1),
            session_hours=session_hours,
            observed_hours=obs_time
        )

        try: 
            new_log.save()
        except:
            # error if date is not unique
            return HttpResponse(json.dumps({
                "status": "error",
                "message": "This date has already been logged."
            }))

        print("logged monthly data")

    # return success message
    return HttpResponse(json.dumps({
        "status": "success",
        "message": "Data Logged Successfully"
    }))

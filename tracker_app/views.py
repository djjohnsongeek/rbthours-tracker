from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import models
from django.http import HttpResponse

import os
import simplejson as json
import csv
import re
import datetime

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

        # prepare current date, file path, response obj
        response = render(request, "tracker_app/login.html")
        today = datetime.date.today()
        one_year = datetime.timedelta(days=365)
        path = os.path.join(settings.BASE_DIR, "delete_date", "date.txt")

        # create file if missing
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(datetime.date.strftime(today + one_year, "%m/%d/%Y"))

        # get date
        with open(path, "r") as f:
            string_date = f.read()

        # convert date from file to date obj
        delete_date = datetime.datetime.strptime(string_date, "%m/%d/%Y").date()
        time_till_delete = delete_date - today

        # delete all user logs, store new date
        if delete_date == today:
            models.Monthly_log.objects.all().delete()
            models.Daily_log.objects.all().delete()        
            
            new_date = datetime.datetime.today() + one_year
            with open(path, "w") as f:
                f.write(datetime.date.strftime(new_date, "%m/%d/%Y"))

        elif time_till_delete.days <= 14:
            # warn user with message at login page
            messages.error(
                request, f"On {helper.convert_month(delete_date.month)}" 
                         f" {delete_date.day}, {delete_date.year} all user "
                         f"logs will be deleted. Download them now."
            )
        
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
    try:
        new_user = User.objects.create_user(username, email, password)
        new_user.save()
    except:
        messages.error(request, "Username already taken")
        return redirect(reverse("register"))

    # create user file path
    current_user = User.objects.get(username=username)
    path = os.path.join(settings.BASE_DIR, "userlog_files", str(current_user.pk))
    os.mkdir(path)

    messages.success(request, "Account created!")
    return redirect(reverse("login_view"))

@login_required
def view_hours(request, table_type):
    # Prepare proper Models
    
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

    # check for no data
    if not user_data.exists():
        context = {
            "headings": False,
            "data": False,
            "message": "No Data Found :(",
            "table_type": table_type.capitalize() + " Logs"
        }
        return render(request, "tracker_app/view-hours.html", context)

    # convert monthly log month numbers to their string form
    id_list = []
    for row in user_data:
        if table_type == "monthly":
            row["month"] = helper.convert_month(row["month"])
            if .05 * float(row["session_hours"]) <= float(row["observed_hours"]):
                row["5% ?"] = "Yes"
            else:
                row["5% ?"] = "No"

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
        "table_type_arg": table_type,
        "table_type": table_type.capitalize() + " Logs"

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
        session_hours = float(request_data["hours"])
        obs_time = round((float(request_data["obs_time"]) / devisor), 2)
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
                user_id=request.user.id,
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
                "message": "This Month has already been logged."
            }))

        print("logged monthly data")

    # return success message
    return HttpResponse(json.dumps({
        "status": "success",
        "message": "Data Logged Successfully"
    }))

@login_required
def delete_data(request, data_type, primary_key):
    url_error = HttpResponse(
        json.dumps({
            "status": "error",
            "message": "Invalid URL"
        }))

    nolog_error = HttpResponse(
        json.dumps({
            "status": "error",
            "message": "This log does not exist"
        })
    )

    # check for proper method
    if request.method != "DELETE":
        return HttpResponse(json.dumps({
            "status": "error",
            "message": "Method not Allowed"
        }))

    # check for valid url arguments
    if data_type == "daily":
        log_type = models.Daily_log
    elif data_type == "monthly":
        log_type = models.Monthly_log
    else:
        return url_error

    # find log to delete
    try:
        row_for_delete = log_type.objects.get(pk=int(primary_key))
    except ValueError:
        return url_error
    except log_type.DoesNotExist:
        return nolog_error

    # update monthly info if necssary
    if data_type == "daily":
        date = datetime.datetime.strftime(row_for_delete.date, "%Y/%m/%d/")
        date = date.split("/")
        year = int(date[0])
        month = (int(date[1]))
        obs_hours = row_for_delete.observed_hours
        session_hours = row_for_delete.session_hours

        try:
            monthly_log = models.Monthly_log.objects.get(user_id=request.user.id, month=month, year=year)

            if monthly_log.mutable:
                monthly_log.observed_hours = monthly_log.observed_hours - obs_hours
                monthly_log.session_hours = monthly_log.session_hours - session_hours
                monthly_log.save()
        except models.Monthly_log.DoesNotExist:
            pass
    
    row_for_delete.delete()

    return HttpResponse(json.dumps({
        "status": "success",
        "message": "Data Deleted"
    }))

@login_required
def download(request, user_id, file_name):
    if int(user_id) != request.user.id:
        raise PermissionDenied
        
    no_file_error = redirect(
        reverse("view_hours", kwargs={"table_type": "daily"})
    )

    # ensure safe html args, query for user logs
    if file_name == "daily":
        fieldnames = ["date", "session_hours", "observed_hours", "supervisor"]
        user_logs = models.Daily_log.objects.filter(
            user_id=request.user.id
        ).order_by("date").values(
            "date", "session_hours",
            "observed_hours", "supervisor"
        )

    elif file_name == "monthly":
        fieldnames = ["year", "month", "session_hours", "observed_hours"]
        user_logs = models.Monthly_log.objects.filter(
            user_id=request.user.id
        ).order_by("year", "month").values(
            "year", "month","session_hours",
            "observed_hours"
        )
    else:
        messages.error(request, "No File Found")
        return no_file_error


    # prepare file path
    file_name = file_name + ".csv"
    path = os.path.join(
        settings.BASE_DIR, "userlog_files", str(user_id), file_name
    )

    # remove last file
    if os.path.exists(path):
        os.remove(path)

    # write new file
    with open(path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in user_logs:
            writer.writerow(data)

    # read and send file data
    if os.path.exists(path):
        with open(path) as f:
            response = HttpResponse(f.read(), content_type="text/csv")
            response["Content-Disposition"] = f"attachment/filename={file_name}"
            return response

    messages.error(request, "No File Found")
    return no_file_error
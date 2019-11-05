    // show/hide table
    function toggle_visible(tableElement){
        if (tableElement.style.display == "none"){
            tableElement.style.display = "";
        }
        else {
            tableElement.style.display = "none";
        }
    }
    // change chevron direction
    function toggle_chevron(chevron){
        if (chevron.className == "fas fa-chevron-up"){
            chevron.className = "fas fa-chevron-down";
        }
        else {
            chevron.className = "fas fa-chevron-up";
        }
    }

    // change table to daily or monthly based on user's selection
    document.getElementById("rbt-select").addEventListener("change", () => {
        const rbtName = document.getElementById("rbt-select").value.split(" ");
        window.location = `http://127.0.0.1:8000/view-rbt/${rbtName[0]}%20${rbtName[1]}`;
    });

    // set event lister for chevrons if they exist
    if (document.getElementById("daily-log-showorhide")) {

        document.getElementById("daily-log-showorhide").addEventListener("click", (event) => {
            const dailyTableBody = event.target.parentElement.parentElement.parentElement.children[2];
            const chevron = document.getElementById("daily-chevron");
            toggle_visible(dailyTableBody);
            toggle_chevron(chevron);
        });
    }

    if (document.getElementById("monthly-log-showorhide")) {
        
        document.getElementById("monthly-log-showorhide").addEventListener("click", (event) => {
            const dailyTableBody = event.target.parentElement.parentElement.parentElement.children[2];
            const chevron = document.getElementById("monthly-chevron");
            toggle_visible(dailyTableBody);
            toggle_chevron(chevron);
        });
    }

    // setup events for 'Sign Here' text
    signHereElements = document.getElementsByClassName("sign-here");
    for(let element of signHereElements){
        element.addEventListener("click", (event) => {
            // prepare data for request
            const rowElement = event.target.parentElement;
            const tableType = rowElement.className;
            const rowIndex = rowElement.dataset.rowIndexNumber;
            const supervName = Cookies.get("supervisor_name");
            const url = "http://127.0.0.1:8000/log-data/sign";
            const data = {
                "table_type": tableType,
                "rowID": rowIndex,
                "supervisor_name": supervName,
                "csrfmiddlewaretoken": Cookies.get("csrftoken")
            }
            // send request, fetch server response
            fetch(url, {
                method: "PUT",
                credentials: "include",
                headers: {
                  "X-CSRFToken": Cookies.get("csrftoken"),
                  "Content-type": "application/json",
                  "X-Requested-With": "XMLHttpRequest"
                },
                body: JSON.stringify(data)
            }).then(res => {
                return res.json();
            }).then(function (response){
                // update selected row with appropriate data
                if (response.status === "success"){
                    months = ["Jan.", "Feb.", "Mar.", "Apr.", "May.", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]
                    const date = new Date();
                    string_date = ''.concat(months[date.getMonth()], " ", date.getDate(), ", ", date.getFullYear());
                    event.target.className = "";
                    event.target.innerHTML = supervName;
                    event.target.nextElementSibling.innerHTML = string_date;
                }
                // alert user to the failure
                else {
                    alert("Signing Failed")
                }
            })
        })
    }
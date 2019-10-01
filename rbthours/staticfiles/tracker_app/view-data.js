    // change table to daily or monthly based on user's selection
    document.getElementById("select-viewhours").addEventListener("change", () => {
        const tableType = document.getElementById("select-viewhours").value;

        // no table is rendered if there is no data
        if (tableType !== document.getElementById("table-caption").innerHTML.toLowerCase()){
            window.location = `https://rbt-tracker.herokuapp.com/view-hours/${tableType}`;
        }
    });

    // add event listeners to each row of the table
    const tableRows = document.getElementsByTagName("tr");
    let i;
    for (i = 0; i < tableRows.length; i++) {
        tableRows[i].addEventListener("click", (event) => {
            const tableType = document.getElementById("table-caption").innerHTML.replace(" Logs", "").toLowerCase();
            const tr_element = event.target.parentElement.parentElement;
            const pk = tr_element.id;

            // setup url and data for the DELETE request
            const url = `https://rbt-tracker.herokuapp.com/delete-data/${tableType}/${pk}`;
            const data = {
                "csrfmiddlewaretoken": Cookies.get("csrftoken")
            };

            // send DELETE request to server
            if (tr_element.parentElement === document.getElementsByTagName("tbody")[0]){
                fetch(url, {
                    method: "DELETE",
                    credentials: "include",
                    headers: {
                        "X-CSRFToken": Cookies.get("csrftoken"),
                        "Content-type": "application/json",
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    body: JSON.stringify(data)
                }).then(res => res.json())
                .then(response =>{
                    if (response.status === "success"){
                        tr_element.remove();
                        if (!document.getElementsByTagName("td")[0]){
                            document.getElementById("download-link").remove();
                        }
                    }
                    console.log(response.message);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
            // TODO add animation
        });
    }
class Message extends React.Component {
    render() {
        return (
            <div className={`${this.props.messagetype}`}>
                <span>{`${this.props.messagecontent}`}</span>
            </div>
        )
    }
}
class SelectTitle extends React.Component {
    render() {
        return(
            <div className="header">
                <select onChange={this.props.handleChange} id="slct-logdata">
                    <option id="op-daily" value="day">Daily Hours</option>
                    <option id="op-monthly" value="month">Monthly Hours</option>
                </select>
            </div>
        )
    }
}

class DayForm extends React.Component {
    render() {
        return(
            <form className="form-logdata" data-formtype="day" id="daily">
                <input id="input-date" type="date" placeholder="yyyy-mm-dd" name="date"/><br/>
                <input placeholder="Session Hours" type="text" name="session_hours" className="input-login-double"/>
                <input placeholder="Session Minutes" type="test" name="session_min" className="input-login-double"/><br/>
                <input placeholder="Hours Observed" type="test" name="obs_min"  className="input-login-double"/>
                <input placeholder="Minutes Observed" type="text" name="obs_time"  className="input-login-double"/><br/>
                <input placeholder="Supervisor" type="text" name="supervisor"/><br/>
                <button onClick={this.props.postData} className="btn-submit-data">Submit</button>
            </form>
        )
    }
}

class MonthForm extends React.Component {
    render() {
        return (
            <form className="form-logdata" data-formtype="month" id="monthly">
                <input id="input-date" type="date" placeholder="yyyy-mm-dd" name="date"/><br/>
                <input placeholder="Session Hours" type="text" name="session_hours"/><br/>
                <input placeholder="Hours Observed" type="text" name="obs_time"/><br/>
                <button onClick={this.props.postData} className="btn-submit-data">Submit</button>
            </form>
        )
    }
}

class App extends React.Component {
    
    constructor(props){
        super(props);
        this.state = {
            messagetype: "hidden",
            messagecontent: "",
            day: true,
            month: false
        }
    }

    postData = (event) => {
        // get form DOM node
        const logForm = document.getElementsByClassName("form-logdata")[0]

        //prevent default form submission
        event.preventDefault();

        // capture data from form's input fields
        const logData = [];
        const logType = logForm.dataset.formtype;        
        for (let element of document.getElementsByTagName("input")){
            logData.push(element.value);
        }

        // assume a monthly log
        const date = logData[0];
        let sessionHours = logData[1];
        let sessionMin = 0
        let obsHours = logData[2];
        let obsMin = 0
        let supervisor = "";
        let factor = 1;

        // update varible if the log is daily
        if (logType === "day"){
            sessionMin = logData[2];
            obsHours = logData[3];
            obsMin = logData[4];
            supervisor = logData[5];
            factor = 60
        }

        // consolidate time data
        const hours = Number(sessionHours) + (Number(sessionMin) / 60);
        const obsTime = (Number(obsHours) * factor) + Number(obsMin);

        console.log(hours, obsTime);
        // setup url and data for the POST request
        const url = `http://127.0.0.1:8000/log-data/${logType}`;
        const data = {
            "date": date,
            "hours": hours,
            "obs_time": obsTime,
            "supervisor": supervisor,
            "csrfmiddlewaretoken": Cookies.get("csrftoken")
        };
        
        // send POST request to server
        fetch(url, {
            method: "POST",
            credentials: "include",
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken"),
                "Content-type": "application/json",
                "X-Requested-With": "XMLHttpRequest"
            },
            body: JSON.stringify(data)
        }).then(res => res.json())
        .then(response => {
            // display error/success message given by server response
            this.setState({
                messagecontent: response.message,
                messagetype: response.status
            });
            // clear form input fields if data was successfully submited
            if (response.status === "success"){
                logForm.reset();
            } 
        })
        .catch(error => {
            console.error('Error:', error);
            this.setState({
                messagecontent: "Server Error: No Response",
                messagetype: "error",
            });
        });
    }
    handleChange = (event) => {
        const newFormType = event.target.value;
        if (newFormType === "day"){
            this.setState({
                month: false,
                day: true
            })
        }
        else{
            this.setState({
                month: true,
                day: false
            })
        }
        // reset message contents to hidden
        this.setState({
            messagecontent: "",
            messagetype: "hidden"
        })
    }

    render(){
        if (this.state.day){
            return(
                <div>
                    <SelectTitle 
                        handleChange={this.handleChange}/>
                    <div className="spacer-tiny"></div>
                    <Message 
                        messagetype={this.state.messagetype}
                        messagecontent={this.state.messagecontent}
                    />
                    <DayForm postData={this.postData}/>
                </div>
            );
        }
        else if (this.state.month){
            return(
                <div>
                    <SelectTitle handleChange={this.handleChange}/>
                    <div className="spacer-tiny"></div>
                    <Message 
                        messagetype={this.state.messagetype}
                        messagecontent={this.state.messagecontent}
                    />
                    <MonthForm postData={this.postData}/>
                </div>
            );
        }
        else{
            return(
                <div>
                    <span>An Error Occcured</span>
                </div>
            )
        }
    }
}

ReactDOM.render(<App />, document.querySelector("#app"));
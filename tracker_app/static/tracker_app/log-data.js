"use strict";

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _instanceof(left, right) { if (right != null && typeof Symbol !== "undefined" && right[Symbol.hasInstance]) { return !!right[Symbol.hasInstance](left); } else { return left instanceof right; } }

function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!_instanceof(instance, Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

var Message =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Message, _React$Component);

  function Message() {
    _classCallCheck(this, Message);

    return _possibleConstructorReturn(this, _getPrototypeOf(Message).apply(this, arguments));
  }

  _createClass(Message, [{
    key: "render",
    value: function render() {
      return React.createElement("div", {
        className: "".concat(this.props.messagetype)
      }, React.createElement("span", null, "".concat(this.props.messagecontent)));
    }
  }]);

  return Message;
}(React.Component);

var SelectTitle =
/*#__PURE__*/
function (_React$Component2) {
  _inherits(SelectTitle, _React$Component2);

  function SelectTitle() {
    _classCallCheck(this, SelectTitle);

    return _possibleConstructorReturn(this, _getPrototypeOf(SelectTitle).apply(this, arguments));
  }

  _createClass(SelectTitle, [{
    key: "render",
    value: function render() {
      return React.createElement("div", {
        className: "header"
      }, React.createElement("select", {
        onChange: this.props.handleChange,
        id: "slct-logdata"
      }, React.createElement("option", {
        id: "op-daily",
        value: "day"
      }, "Daily Hours"), React.createElement("option", {
        id: "op-monthly",
        value: "month"
      }, "Monthly Hours")));
    }
  }]);

  return SelectTitle;
}(React.Component);

var DayForm =
/*#__PURE__*/
function (_React$Component3) {
  _inherits(DayForm, _React$Component3);

  function DayForm() {
    _classCallCheck(this, DayForm);

    return _possibleConstructorReturn(this, _getPrototypeOf(DayForm).apply(this, arguments));
  }

  _createClass(DayForm, [{
    key: "render",
    value: function render() {
      return React.createElement("form", {
        className: "form-logdata",
        "data-formtype": "day",
        id: "daily"
      }, React.createElement("input", {
        id: "input-date",
        type: "date",
        placeholder: "yyyy-mm-dd",
        name: "date"
      }), React.createElement("br", null), React.createElement("input", {
        placeholder: "Session Hours",
        type: "text",
        name: "session_hours",
        className: "input-login-double"
      }), React.createElement("input", {
        placeholder: "Session Minutes",
        type: "test",
        name: "session_min",
        className: "input-login-double"
      }), React.createElement("br", null), React.createElement("input", {
        placeholder: "Hours Observed",
        type: "test",
        name: "obs_min",
        className: "input-login-double"
      }), React.createElement("input", {
        placeholder: "Minutes Observed",
        type: "text",
        name: "obs_time",
        className: "input-login-double"
      }), React.createElement("br", null), React.createElement("input", {
        placeholder: "Supervisor",
        type: "text",
        name: "supervisor"
      }), React.createElement("br", null), React.createElement("button", {
        onClick: this.props.postData,
        className: "btn-submit-data"
      }, "Submit"));
    }
  }]);

  return DayForm;
}(React.Component);

var MonthForm =
/*#__PURE__*/
function (_React$Component4) {
  _inherits(MonthForm, _React$Component4);

  function MonthForm() {
    _classCallCheck(this, MonthForm);

    return _possibleConstructorReturn(this, _getPrototypeOf(MonthForm).apply(this, arguments));
  }

  _createClass(MonthForm, [{
    key: "render",
    value: function render() {
      return React.createElement("form", {
        className: "form-logdata",
        "data-formtype": "month",
        id: "monthly"
      }, React.createElement("input", {
        id: "input-date",
        type: "date",
        placeholder: "yyyy-mm-dd",
        name: "date"
      }), React.createElement("br", null), React.createElement("input", {
        placeholder: "Session Hours",
        type: "text",
        name: "session_hours"
      }), React.createElement("br", null), React.createElement("input", {
        placeholder: "Hours Observed",
        type: "text",
        name: "obs_time"
      }), React.createElement("br", null), React.createElement("button", {
        onClick: this.props.postData,
        className: "btn-submit-data"
      }, "Submit"));
    }
  }]);

  return MonthForm;
}(React.Component);

var App =
/*#__PURE__*/
function (_React$Component5) {
  _inherits(App, _React$Component5);

  function App(props) {
    var _this;

    _classCallCheck(this, App);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(App).call(this, props));

    _defineProperty(_assertThisInitialized(_this), "postData", function (event) {
      // get form DOM node
      var logForm = document.getElementsByClassName("form-logdata")[0]; //prevent default form submission

      event.preventDefault(); // capture data from form's input fields

      var logData = [];
      var logType = logForm.dataset.formtype;
      var _iteratorNormalCompletion = true;
      var _didIteratorError = false;
      var _iteratorError = undefined;

      try {
        for (var _iterator = document.getElementsByTagName("input")[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
          var element = _step.value;
          logData.push(element.value);
        } // assume a monthly log

      } catch (err) {
        _didIteratorError = true;
        _iteratorError = err;
      } finally {
        try {
          if (!_iteratorNormalCompletion && _iterator.return != null) {
            _iterator.return();
          }
        } finally {
          if (_didIteratorError) {
            throw _iteratorError;
          }
        }
      }

      var date = logData[0];
      var sessionHours = logData[1];
      var sessionMin = 0;
      var obsHours = logData[2];
      var obsMin = 0;
      var supervisor = "";
      var factor = 1; // update varible if the log is daily

      if (logType === "day") {
        sessionMin = logData[2];
        obsHours = logData[3];
        obsMin = logData[4];
        supervisor = logData[5];
        factor = 60;
      } // consolidate time data


      var hours = Number(sessionHours) + Number(sessionMin) / 60;
      var obsTime = Number(obsHours) * factor + Number(obsMin);
      console.log(hours, obsTime); // setup url and data for the POST request

      var url = "https://rbt-tracker.herokuapp.com/log-data/".concat(logType);
      var data = {
        "date": date,
        "hours": hours,
        "obs_time": obsTime,
        "supervisor": supervisor,
        "csrfmiddlewaretoken": Cookies.get("csrftoken")
      }; // send POST request to server

      fetch(url, {
        method: "POST",
        credentials: "include",
        headers: {
          "X-CSRFToken": Cookies.get("csrftoken"),
          "Content-type": "application/json",
          "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify(data)
      }).then(function (res) {
        return res.json();
      }).then(function (response) {
        // display error/success message given by server response
        _this.setState({
          messagecontent: response.message,
          messagetype: response.status
        }); // clear form input fields if data was successfully submited


        if (response.status === "success") {
          logForm.reset();
        }
      }).catch(function (error) {
        console.error('Error:', error);

        _this.setState({
          messagecontent: "Server Error: No Response",
          messagetype: "error"
        });
      });
    });

    _defineProperty(_assertThisInitialized(_this), "handleChange", function (event) {
      var newFormType = event.target.value;

      if (newFormType === "day") {
        _this.setState({
          month: false,
          day: true
        });
      } else {
        _this.setState({
          month: true,
          day: false
        });
      } // reset message contents to hidden


      _this.setState({
        messagecontent: "",
        messagetype: "hidden"
      });
    });

    _this.state = {
      messagetype: "hidden",
      messagecontent: "",
      day: true,
      month: false
    };
    return _this;
  }

  _createClass(App, [{
    key: "render",
    value: function render() {
      if (this.state.day) {
        return React.createElement("div", null, React.createElement(SelectTitle, {
          handleChange: this.handleChange
        }), React.createElement("div", {
          className: "spacer-tiny"
        }), React.createElement(Message, {
          messagetype: this.state.messagetype,
          messagecontent: this.state.messagecontent
        }), React.createElement(DayForm, {
          postData: this.postData
        }));
      } else if (this.state.month) {
        return React.createElement("div", null, React.createElement(SelectTitle, {
          handleChange: this.handleChange
        }), React.createElement("div", {
          className: "spacer-tiny"
        }), React.createElement(Message, {
          messagetype: this.state.messagetype,
          messagecontent: this.state.messagecontent
        }), React.createElement(MonthForm, {
          postData: this.postData
        }));
      } else {
        return React.createElement("div", null, React.createElement("span", null, "An Error Occcured"));
      }
    }
  }]);

  return App;
}(React.Component);

ReactDOM.render(React.createElement(App, null), document.querySelector("#app"));
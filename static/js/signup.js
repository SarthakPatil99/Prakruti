//email valid

var emailvalid = document.getElementById("signup_email_error");
emailvalid.style.display = "none";
function validate_email() {
  email = document.getElementById("email").value;
  var validRegex =
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (validRegex.test(email)) {
    emailvalid.style.display = "none";
  } else {
    emailvalid.style.display = "block";
  }
}

var phonevalid = document.getElementById("signup_phone_error");
phonevalid.style.display = "none";
function validate_phone() {
  phone = document.getElementById("phone").value;
  var validRegex = /^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$/;
  if (validRegex.test(phone)) {
    phonevalid.style.display = "none";
  } else {
    phonevalid.style.display = "block";
  }
}

//password validetion
// var btn = document.getElementById("newPassBtn");
var passmtch = document.getElementById("signup_passmtch");
var passrules = document.getElementById("signupup_Pass_rules");
var pwd, confirm_pwd;
passrules.style.display = "none";
passmtch.style.display = "none";

function validate_pass() {
  pwd = document.getElementById("pwd").value;
  var validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  if (validRegex.test(pwd)) {
    passrules.style.display = "none";
  } else {
    passrules.style.display = "block";
  }
}

function validate_cpass() {
  confirm_pwd = document.getElementById("confirm_pwd").value;
  validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  if (validRegex.test(confirm_pwd)) {
    passrules.style.display = "none";
    if (confirm_pwd === pwd) {
      passmtch.style.display = "none";
    } else {
      passmtch.style.display = "block";
    }
  } else {
    passrules.style.display = "block";
  }
}
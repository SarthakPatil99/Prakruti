var getotp = document.getElementById("OTPbtn");
var verify = document.getElementById("verify");
var otp;
verify.style.display = "none";
getotp.disabled = true;
function onBtn() {
  var email = document.getElementById("emailFP").value;
  var spn = document.getElementById("wrMail");
  var validRegex =
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (validRegex.test(email)) {
    getotp.disabled = false;
    spn.style.display = "none";
  } else {
    spn.style.display = "block";
  }
}
function generateOTP() {
  var digits = "0123456789";
  let OTP = "";
  for (let i = 0; i < 6; i++) {
    OTP += digits[Math.floor(Math.random() * 10)];
  }
  return OTP;
}

function sendmail() {
  var email = document.getElementById("emailFP").value;
  otp = generateOTP();
  ebody = "This is your OTP : " + otp;
  Email.send({
    SecureToken: "8f05dc42-76d3-41bf-ba0a-07da1b89f398", //add your token here
    To: "suyashsv47@gmail.com",
    From: "getyourprakruti@gmail.com",
    Subject: "This is the subject",
    Body: ebody,
  }).then((message) => {
    alert("Email has been sent successfully!!!");
    verify.style.display = "block";
    getotp.style.display = "none";
  });
}
function verifyOTP() {
  var spn = document.getElementById("wrOTP");
  var Ch_otp1 = document.getElementById("otp1").value;
  var Ch_otp2 = document.getElementById("otp2").value;
  var Ch_otp3 = document.getElementById("otp3").value;
  var Ch_otp4 = document.getElementById("otp4").value;
  var Ch_otp5 = document.getElementById("otp5").value;
  var Ch_otp6 = document.getElementById("otp6").value;
  var Ch_OTP = Ch_otp1 + Ch_otp2 + Ch_otp3 + Ch_otp4 + Ch_otp5 + Ch_otp6;
  if (Ch_OTP === otp) {
    $("#myModal1").modal("hide");
    $("#chPassModal").modal("show");
    spn.style.display = "none";
  } else {
    // alert("wrong");
    spn.style.display = "block";
  }
}

function clickEvent(prev, first, last) {
  if (first.value.length) {
    document.getElementById(last).focus();
  } else if (first.value.length == 0) {
    document.getElementById(prev).focus();
  }
}
var btn = document.getElementById("newPassBtn");
var passmtch = document.getElementById("passmtch");
var passrules = document.getElementById("Pass_rules");
var npass, nconpass;
passrules.style.display = "none";
passmtch.style.display = "none";
function nPass() {
  npass = document.getElementById("npass").value;
  var validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  if (validRegex.test(npass)) {
    passrules.style.display = "none";
  } else {
    passrules.style.display = "block";
  }
}
function nConPass() {
  nconpass = document.getElementById("nconpass").value;
  validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  if (validRegex.test(nconpass)) {
    passrules.style.display = "none";
    // alert(nconpass + " " + npass);
    if (nconpass === npass) {
      passmtch.style.display = "none";
      // btn.submit();
    } else {
      passmtch.style.display = "block";
    }
  } else {
    passrules.style.display = "block";
  }
}

// Reschedule part

function dayChoose() {
  document.getElementById("dateSec").style.display = "none";
  day = document.getElementById("Day");
  if (parseInt(day.value) > 0 && parseInt(day.value) < 3) {
    console.log(getday(day.value));
    // showAppnt(getday(day));
    // window.alert("day selected");
  } else if (day.value == "0") {
    document.getElementById("Appnts").style.display = "block";
    document.getElementById("schedule").disabled = true;
  } else {
    document.getElementById("date").min = getday("-1");
    document.getElementById("dateSec").style.display = "block";
  }
}
function showAppnt() {
  // appointment showing code
  // console.log(document.getElementById("date").value);
  var ele = document.getElementsByName("appnt");
  for (i = 0; i < ele.length; i++) {
    if (ele[i].checked) console.log(ele[i].value);
  }
  document.getElementById("schedule").disabled=false;
}
function getday(DAY) {
  var dt = new Date();
  var day = String(dt.getDate()).padStart(2, 0);
  var month = String(dt.getMonth() + 1).padStart(2, 0);
  var year = dt.getFullYear();
  if (DAY == "1") {
    return `${day}-${month}-${year}`;
  } else if (DAY == "2") {
    day = parseInt(day) + 1;
    return `${day}-${month}-${year}`;
  } else {
    day = parseInt(day) + 2;
    return `${year}-${month}-${day}`;
  }
  DAY.value;
}
function dayReset() {
  document.getElementById("Day").value = "0";
  var ele = document.getElementsByName("appnt");
  for (i = 0; i < ele.length; i++) {
    ele[i].checked=false;
  }
  dayChoose();
}
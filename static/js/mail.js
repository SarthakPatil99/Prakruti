var otp;
function onBtn() {
  console.log("onBtn clicked");
  var email = document.getElementById("emailFP");
  var validRegex =
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (validRegex.test(email.value)) {
    email.border = "none";
    document.getElementById("OTPbtn").disabled = false;
  } else {
    email.border = "1px solid red";
    document.getElementById("OTPbtn").disabled = true;
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
  console.log(email);
  // check if email is present in database or not
  otp = generateOTP();
  ebody = "This is your OTP : " + otp;
  Email.send({
    SecureToken: "8f05dc42-76d3-41bf-ba0a-07da1b89f398", //add your token here
    To: "suyashsv47@gmail.com",
    From: "getyourprakruti@gmail.com",
    Subject: "This is the subject",
    Body: ebody,
  })
    .then((message) => {
      alert("Email has been sent successfully!!!" + message);
      document.getElementById("verify").style.display = "block";
      document.getElementById("OTPbtn").style.display = "none";
      $("#getOTP").collapse("toggle");
    })
    .catch((error) => {
      alert(error);
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

var npass, nconpass;
function nPass() {
  npass = document.getElementById("npass");
  var validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  if (validRegex.test(npass.value)) {
    npass.style.border = "none";
    document.getElementById("newPassBtn").disabled = false;
  } else {
    npass.style.border = "1px solid red";
    document.getElementById("newPassBtn").disabled = true;
  }
}
function nConPass() {
  nconpass = document.getElementById("nconpass");
  validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  if (validRegex.test(nconpass.value)) {
    nconpass.style.border = "none";

    if (nconpass.value === npass.value) {
      document.getElementById("passmtch").style.display = "none";
      document.getElementById("newPassBtn").disabled = false;
      // btn.submit();
    } else {
      document.getElementById("passmtch").style.display = "block";
      document.getElementById("newPassBtn").disabled = true;
    }
  } else {
    nconpass.style.border = "1px solid red";
    document.getElementById("newPassBtn").disabled = true;
  }
}

function passCont() {
  document.getElementById("BType").innerHTML =
    document.getElementById("Btype").innerHTML;
  document.getElementById("Btitle").innerHTML =
    document.getElementById("title").innerHTML;
  document.getElementById("Content").innerHTML =
    document.getElementById("content").innerHTML;
}

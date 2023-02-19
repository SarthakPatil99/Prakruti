var otp;
function onBtn() {
  console.log("onBtn clicked");
  var email = document.getElementById("emailFP");
  var validRegex =
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (validRegex.test(email.value)) {
    $.ajax({
      type: "GET",
      url: "/mailCheck/",
      data: { email: email.value },
      success: function callback(response) {
        /* do whatever with the response */
        if (response == "False") {
          document.getElementById("OTPbtn").disabled = true;
          document.getElementById("email_not_exist").style.display = "block";
          email.style.border = "1px solid red";
        } else {
          document.getElementById("OTPbtn").disabled = false;
          document.getElementById("email_not_exist").style.display = "none";
          email.style.border = "none";
        }
        console.log(response);
      },
    });
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

function passCont(who) {
  document.getElementById("BType").innerHTML = document.getElementById(
    "Btype" + who
  ).innerHTML;
  document.getElementById("Btitle").innerHTML = document.getElementById(
    "title" + who
  ).innerHTML;
  document.getElementById("Content").innerHTML = document.getElementById(
    "content" + who
  ).innerHTML;
}

function passPD(who){
  console.log(who);
  document.getElementById("PName").innerHTML = document.getElementById("name"+who).innerHTML;
  document.getElementById("PImage").src= document.getElementById("pimage"+who).src;
  document.getElementById("PDesc").innerHTML = document.getElementById("desc"+who).value;
  document.getElementById("PContents").innerHTML = document.getElementById("cont"+who).value;
  document.getElementById("Price").innerHTML = document.getElementById("price"+who).value;
  document.getElementById("Quantity").innerHTML = document.getElementById("quantity" + who).value;
  document.getElementById("buy_now").value = who;
  document.getElementById("cart").value = who;
}

// data tranfer Edit Details
function transferED() {
  var Fname = document.getElementById("Fname");
  var Mname = document.getElementById("Mname");
  var Lname = document.getElementById("Lname");
  var Email = document.getElementById("Email");
  var Phone = document.getElementById("Phone");
  var Age = document.getElementById("Age");
  var Gender = document.getElementById("Gender");
  var Prakruti = document.getElementById("Prakruti");
  var Img = document.getElementById("Img");
  var gender = document.getElementById("gender").innerHTML;

  Fname.value = document.getElementById("fname").innerHTML;
  Mname.value = document.getElementById("mname").innerHTML;
  Lname.value = document.getElementById("lname").innerHTML;
  Email.value = document.getElementById("email").innerHTML;
  Phone.value = document.getElementById("phone").innerHTML;
  Img.src = document.getElementById("dp").src
  Age.value = parseInt(document.getElementById("age").innerHTML);
  Prakruti.innerHTML = document.getElementById("prakruti").innerHTML;
  if (gender == "male") {
    Gender.value = "1";
  } else if (gender == "female") {
    Gender.value = "2";
  } else if (gender == "other") {
    Gender.value = "3";
  } else {
    Gender.value = "0";
  }
}
function chQuant(id){
  Qt = document.getElementById('qt'+id).value;
  document.getElementById("qprice"+id).innerHTML =
    Qt * document.getElementById("pprice"+id).value;
}
function chng(id){
  ch = document.getElementById(id)
  Tprice = document.getElementById("Tprice");
  qprice = document.getElementById("qprice" + id).innerHTML;
  Prdno = document.getElementById("prds");
  if(ch.checked){
    tprice = parseInt(Tprice.innerHTML) + parseInt(qprice);
    prdno  = parseInt(Prdno.innerHTML) + 1;
  } else{
    tprice = parseInt(Tprice.innerHTML) - parseInt(qprice);
    prdno = parseInt(Prdno.innerHTML) - 1;
  }
  Prdno.innerHTML + prdno;
  Tprice.innerHTML = tprice;
  console.log(prdno,tprice);
}
window.onload = function(){
  prdno = parseInt(document.getElementById("prds").innerHTML);
  for (var i=1; i<=prdno;i++){
    chng(i);
  }
}
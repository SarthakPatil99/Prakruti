var btnSubmit = document.getElementById("btn_Submit");
//email phone valid
function validate_email() {
  email = document.getElementById("email");
  var validRegex =
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (validRegex.test(email.value)) {
    $.ajax({
      type: "GET",
      url: "/mailCheck/",
      data: { email: email.value },
      success: function callback(response) {
        /* do whatever with the response */
        if (response == "True") {
          btnSubmit.disabled = true;
          document.getElementById("signup_email_exist").style.display = "block";
          email.style.border = "1px solid red";
        } else {
          btnSubmit.disabled = false;
          document.getElementById("signup_email_exist").style.display = "none";
          email.style.border = "none";
        }
        console.log(response);
      },
    });
  } else {
    email.style.border = "1px solid red";
    btnSubmit.disabled = true;
  }
}

function validate_UName() {
  var userName = document.getElementById('urname').value;
  // console.log(uname);
  $.ajax({
    type: "GET",
    url: "/unameCheck/",
    data: { uname: userName },
    success: function callback(response) {
      /* do whatever with the response */
      if (response == 'True') {
        btnSubmit.disabled = true;
        document.getElementById("signup_uname_exist").style.display = "block";
      } else {
        btnSubmit.disabled = false;
        document.getElementById("signup_uname_exist").style.display = "none";
      }
    },
  });
}

function validate_phone() {
  phone = document.getElementById("phone");
  var validRegex = /^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$/;
  if (validRegex.test(phone.value)) {
    phone.style.border = "none";
    btnSubmit.disabled = false;
  } else {
    phone.style.border = "1px solid red";
    btnSubmit.disabled = true;
  }
}

function validate_pass() {
  var msgPassNotMatch = document.getElementById("div_msgPassNotMatch");
  var msgPassRules = document.getElementById("div_msgPassRules");
  var input_Password = document.getElementById("input_Password");
  msgPassNotMatch.style.display = "none";
  var validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  if (validRegex.test(input_Password.value)) {
    input_Password.style.border = "none";
    msgPassRules.style.display = "none";
    btnSubmit.disabled = false;
  } else {
    input_Password.style.border = "1px solid red";
    msgPassRules.style.display = "block";
    btnSubmit.disabled = true;
  }
}

function validate_cpass() {
  var passmtch = document.getElementById("div_msgPassNotMatch");
  var input_Password = document.getElementById("input_Password");
  var input_ConfirmPassword = document.getElementById("input_ConfirmPassword");
  if (input_Password.value != "") {
    input_ConfirmPassword.style.border = "none";
    if (input_ConfirmPassword.value === input_Password.value) {
      passmtch.style.display = "none";
      btnSubmit.disabled = false;
    } else {
      passmtch.style.display = "block";
      btnSubmit.disabled = true;
    }
  } else {
    input_ConfirmPassword.style.border = "1px solid red";
    btnSubmit.disabled = true;
  }
}

function validateImage() {
  var input_File = document.getElementById("input_File");
  var img_DP = document.getElementById("img_DP");
  if (input_File) {
    var filePath = input_File.value;
    // Allowing file type
    var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;

    if (!allowedExtensions.exec(filePath)) {
      alert("Invalid file type");
      input_File.value = "";
      img_DP.src = "";
      btnSubmit.disabled = true;
    } else {
      // Image preview
      if (input_File.files && input_File.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
          img_DP.src = e.target.result;
        };
        reader.readAsDataURL(input_File.files[0]);
        btnSubmit.disabled = false;
      }
    }
  } else {
    console.log(input_File);
  }
}

function validateAge() {
  age = document.getElementById("input_Age");
  if (age.value > 0) {
    console.log("valid Age");
    age.style.border = "none";
    btnSubmit.disabled = false;
  } else {
    console.log("Invalid Age");
    age.value = "";
    age.placeholder = "Invalid Age";
    age.style.border = "1px solid red";
    btnSubmit.disabled = true;
  }
}

function validateGender() {
  gender = document.getElementById("input_Gender");
  if (gender.value > 0) {
    console.log("valid Gender");
    gender.style.border = "none";
    btnSubmit.disabled = false;
  } else {
    console.log("Invalid Gender");
    gender.value = "0";
    gender.style.border = "1px solid red";
    btnSubmit.disabled = true;
  }
}
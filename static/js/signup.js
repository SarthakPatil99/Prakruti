var btn = document.getElementById("Submit");

//email phone valid
function validate_email() {
  email = document.getElementById("email");
  var validRegex =
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (validRegex.test(email.value)) {
    email.style.border = "none";
    btn.disabled = false;
  } else {
    email.style.border = "1px solid red";
    btn.disabled = true;
  }
}

function validate_phone() {
  phone = document.getElementById("phone");
  var validRegex = /^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$/;
  if (validRegex.test(phone.value)) {
    phone.style.border = "none";
    btn.disabled = false;
  } else {
    phone.style.border = "1px solid red";
    btn.disabled = true;
  }
}

//password validetion
var pwd, confirm_pwd;

function validate_pass() {
  var passmtch = document.getElementById("signup_passmtch");
  var passrules = document.getElementById("signup_Pass_rules");
  pwd = document.getElementById("pwd");
  passmtch.style.display = "none";
  var validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  if (validRegex.test(pwd.value)) {
    pwd.style.border = "none";
    passrules.style.display = "none";
    btn.disabled = false;
  } else {
    pwd.style.border = "1px solid red";
    passrules.style.display = "block";
    btn.disabled = true;
  }
}

function validate_cpass() {
  var passmtch = document.getElementById("signup_passmtch");
  var passrules = document.getElementById("signup_Pass_rules");
  confirm_pwd = document.getElementById("confirm_pwd");
  validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  if (validRegex.test(confirm_pwd.value)) {
    confirm_pwd.style.border = "none";
    passrules.style.display = "none";
    if (confirm_pwd.value === pwd.value) {
      passmtch.style.display = "none";
      btn.disabled = false;
    } else {
      passmtch.style.display = "block";
      btn.disabled = true;
    }
  } else {
    confirm_pwd.style.border = "1px solid red";
    passrules.style.display = "block";
    // passmtch.style.display = "block";
    btn.disabled = true;
  }
}

function validateImage() {
  var fileInput = document.getElementById("inFile");
  var Img = document.getElementById("Img");
  if (fileInput) {
    var filePath = fileInput.value;
    // Allowing file type
    var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;

    if (!allowedExtensions.exec(filePath)) {
      alert("Invalid file type");
      fileInput.value = "";
      Img.src = "";
      document.getElementById("Submit").disabled = true;
    } else {
      // Image preview
      if (fileInput.files && fileInput.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
          Img.src = e.target.result;
        };
        reader.readAsDataURL(fileInput.files[0]);
        document.getElementById("Submit").disabled = false;
      }
    }
  } else {
    console.log(fileInput);
  }
}
function validateAge() {
  age = document.getElementById("Age");
  if (age.value > 0) {
    console.log("valid Age");
    age.style.border = "none";
    document.getElementById("Submit").disabled = false;
  } else {
    console.log("Invalid Age");
    age.value = "";
    age.placeholder = "Invalid Age";
    age.style.border = "1px solid red";
    document.getElementById("Submit").disabled = true;
  }
}
function validateGender() {
  gender = document.getElementById("Gender");
  if (gender.value > 0) {
    console.log("valid Gender");
    gender.style.border = "none";
    document.getElementById("Submit").disabled = false;
  } else {
    console.log("Invalid Gender");
    gender.value = "0";
    gender.style.border = "1px solid red";
    document.getElementById("Submit").disabled = true;
  }
}
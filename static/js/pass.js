var npass, nconpass;
function nPass() {
  npass = document.getElementById("npass");
  var validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  if (validRegex.test(npass.value)) {
    npass.style.border = "none";
    document.getElementById("newPass").disabled = false;
  } else {
    npass.style.border = "1px solid red";
    document.getElementById("newPass").disabled = true;
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
      document.getElementById("newPass").disabled = false;
      // btn.submit();
    } else {
      document.getElementById("passmtch").style.display = "block";
      document.getElementById("newPass").disabled = true;
    }
  } else {
    nconpass.style.border = "1px solid red";
    document.getElementById("newPassBtn").disabled = true;
  }
}
var btn = document.getElementById("newPass");
var passmtch = document.getElementById("passmtch");
btn.disabled = true;
var np = false,
  ncp = false;
var npass, nconpass;
function nPass() {
  var validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  npass = document.getElementById("npass").value;
  if (validRegex.test(npass)) {
    np = true;
  } else {
    np = false;
  }
}
function nConPass() {
  validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  nconpass = document.getElementById("nconpass").value;
  if (validRegex.test(nconpass)) {
    ncp = true;
  } else {
    ncp = false;
  }
}

if (ncp && np) {
  spn.style.display = "none";
  if (nconpass === npass) {
    btn.disabled = false;
    passmtch.style.display = "none";
  } else {
    btn.disabled = true;
    passmtch.styles.display = "block";
  }
} else {
  btn.disabled = true;
  passmtch.style.display = "none";
  spn.style.display = "block";
}

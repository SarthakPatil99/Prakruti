// console.log("transfer");
// data transfer Medicine Remedies
function transferMR(who) {
  var name = document.getElementById("Name");
  var img = document.getElementById("Img");
  var inFile = document.getElementById("inFile");
  var desc = document.getElementById("Desc");
  var content = document.getElementById("Content");
  var quantity = document.getElementById("Quantity");
  var price = document.getElementById("Price");
  var Submit = document.getElementById("Submit");
  var MTitle = document.getElementById("MTitle");
  if (who) {
    Submit.innerHTML = "Modify";
    MTitle.innerHTML = "Update Medicine";
    inFile.value = "";
    name.value = document.getElementById("name").innerHTML;
    img.src = document.getElementById("img").innerHTML;
    desc.value = document.getElementById("desc").innerHTML;
    content.value = document.getElementById("contents").innerHTML;
    quantity.value = parseInt(document.getElementById("quantity").innerHTML);
    price.value = parseInt(document.getElementById("price").innerHTML);
  } else {
    Submit.innerHTML = "Create";
    MTitle.innerHTML = "New Medicine";
    name.value = "";
    inFile.value = "";
    img.src = "";
    desc.value = "";
    content.value = "";
    quantity.value = "";
    price.value = "";
  }
}

// data transfer Blogs
function transferBlog(who) {
  var title = document.getElementById("Title");
  var type = document.getElementById("Btype");
  var contents = document.getElementById("Contents");
  var video = document.getElementById("Vdo");
  var img = document.getElementById("Img");
  var Submit = document.getElementById("Submit");
  var MTitle = document.getElementById("MTitle");
  if (document.getElementById("Vdo")) {
    stopVideo();
  }

  if (who) {
    Submit.innerHTML = "Modify";
    MTitle.innerHTML = "Update Blog";
    title.value = document.getElementById("title").innerHTML;
    type.value = gettype(document.getElementById("type").innerHTML);
    type.disabled = true;
    contents.value = document.getElementById("contents").textContent;
    // img.src = document.getElementById("img").src;
    // video.src = document.getElementById("vdo").src;
    seeType(type);
  } else {
    Submit.innerHTML = "Create";
    MTitle.innerHTML = "New Blog";
    title.value = "";
    type.value = "0";
    contents.value = "";
    // img.src = "";
    // video.src = "";
    document.getElementById("inGrp").style.display = "block";
    document.getElementById("textField").style.display = "none";
    document.getElementById("imgField").style.display = "none";
    document.getElementById("videoField").style.display = "none";
  }
}

// data transfer Home Remedies
function transferHR(who) {
  var title = document.getElementById("Title");
  var img = document.getElementById("Img");
  var inFile = document.getElementById("inFile");
  var desc = document.getElementById("Desc");
  var acce = document.getElementById("Acce");
  var Submit = document.getElementById("Submit");
  var MTitle = document.getElementById("MTitle");
  if (who) {
    Submit.innerHTML = "Modify";
    MTitle.innerHTML = "Update Remedy";
    inFile.value = "";
    title.value = document.getElementById("title").innerHTML;
    img.src = document.getElementById("img").innerHTML;
    desc.value = document.getElementById("desc").innerHTML;
    acce.value = document.getElementById("acce").innerHTML;
  } else {
    Submit.innerHTML = "Create";
    MTitle.innerHTML = "New Remedy";
    title.value = "";
    img.src = "";
    inFile.value = "";
    desc.value = "";
    acce.value = "";
  }
}

function transferED() {
  var Fname= document.getElementById("Fname");
  var Mname = document.getElementById("Mname");
  var Lname = document.getElementById("Lname");
  var Email = document.getElementById("Email");
  var Phone = document.getElementById("Phone");
  var Age = document.getElementById("Age");
  var Gender = document.getElementById("Gender");
  var Prakruti = document.getElementById("Prakruti");

  var gender =  document.getElementById("gender").innerHTML;
  var prakruti =document.getElementById("prakruti").innerHTML;

  Fname.value = document.getElementById("fname").innerHTML;
  Mname.value = document.getElementById("mname").innerHTML;
  Lname.value = document.getElementById("lname").innerHTML;
  Email.value = document.getElementById("email").innerHTML;
  Phone.value = document.getElementById("phone").innerHTML;
  Age.value = parseInt(document.getElementById("age").innerHTML);
  
  if(gender == "male"){
    Gender.value = "1";
  }else if(gender == "female"){
    Gender.value = "2";
  }else if(gender == "other"){
    Gender.value = "3";
  }else{
    Gender.value = "0";
  }

  if(prakruti=="Vata Kapha"){
    Prakruti.value = "1";
  }else if(prakruti =="Vata Pitta"){
    Prakruti.value = "2";
  }else if(prakruti =="Kapha Vata"){
    Prakruti.value = "3";
  }else if(prakruti =="Kapha Pitta"){
    Prakruti.value = "4";
  }else if(prakruti =="Pitta Vata"){
    Prakruti.value = "5";
  }else if(prakruti =="Pitta Kapha"){
    Prakruti.value = "6";
  } else{
    Prakruti.value = "0";
  }
}
// validators
function validateEmail() {
  var email = document.getElementById("emailP");
  var validRegex =
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (validRegex.test(email.value)) {
    console.log("valid Email");
    email.style.border = "none";
    document.getElementById("Submit").disabled = false;
  } else {
    console.log("Invalid Email");
    email.style.border = "1px solid red ";
    document.getElementById("Submit").disabled = true;
  }
}
function validatePhone() {
  phone = document.getElementById("phone");
  var validRegex = /^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$/;
  if (validRegex.test(phone.value)) {
    console.log("valid Phone");
    phone.style.border = "none";
    document.getElementById("Submit").disabled = false;
  } else {
    console.log("Invalid Phone");
    phone.style.border = "1px solid red";
    document.getElementById("Submit").disabled = true;
  }
}
function validateAge() {
  age = document.getElementById("age");
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
function validatePrakruti() {
  prakruti = document.getElementById("Prakruti");
  if (prakruti.value > 0) {
    console.log("valid Prakruti");
    prakruti.style.border = "none";
    document.getElementById("Submit").disabled = false;
  } else {
    console.log("Invalid Prakruti");
    prakruti.value = "0";
    prakruti.style.border = "1px solid red";
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
function validateQuantity() {
  quantity = document.getElementById("Quantity");
  if (quantity.value > 0) {
    console.log("valid Quantity");
    document.getElementById("Submit").disabled = false;
  } else {
    console.log("Invalid Quantity");
    quantity.value = "";
    quantity.placeholder = "Enter a valid Quantity";
    document.getElementById("Submit").disabled = true;
  }
}
function validatePrice() {
  price = document.getElementById("Price");
  if (price.value > 0) {
    console.log("valid Price");
    document.getElementById("Submit").disabled = false;
  } else {
    console.log("Invalid Price");
    price.value = "";
    price.placeholder = "Enter a valid Price";
    document.getElementById("Submit").disabled = true;
  }
}
function validateImage() {
  var fileInput = document.getElementById("inFile");
  var img = document.getElementById("Img");
  if (fileInput) {
    var filePath = fileInput.value;
    // Allowing file type
    var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;

    if (!allowedExtensions.exec(filePath)) {
      alert("Invalid file type");
      fileInput.value = "";
      img.src = "";
      document.getElementById("Submit").disabled = true;
    } else {
      // Image preview
      if (fileInput.files && fileInput.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
          img.src = e.target.result;
        };
        reader.readAsDataURL(fileInput.files[0]);
        document.getElementById("Submit").disabled = false;
      }
    }
  } else {
    console.log(fileInput);
  }
}

// Blog section functions
function validateBType() {
  type = document.getElementById("Btype");
  if (type.value > 0 && type.value < 4) {
    console.log("valid Type");
    type.style.border = "none";
    document.getElementById("Submit").disabled = false;
  } else {
    console.log("Invalid Type");
    type.value = "0";
    type.style.border = "1px solid red";
    document.getElementById("Submit").disabled = true;
  }
  seeType(type);
}

function gettype(val) {
  // console.log("gettype");
  if (val == "Blog") {
    return "1";
  } else if (val == "Image") {
    return "2";
  } else if (val == "Video") {
    return "3";
  } else {
    return "0";
  }
}
function seeType(type) {
  img = document.getElementById("imgField");
  vdo = document.getElementById("videoField");
  txt = document.getElementById("textField");
  inp = document.getElementById("inGrp");
  if (type.value == 3) {
    inp.style.display = "block";
    txt.style.display = "none";
    img.style.display = "none";
    vdo.style.display = "block";
  } else if (type.value == 2) {
    inp.style.display = "block";
    txt.style.display = "none";
    img.style.display = "block";
    vdo.style.display = "none";
  } else if (type.value == 1) {
    inp.style.display = "none";
    txt.style.display = "block";
    img.style.display = "none";
    vdo.style.display = "none";
  } else {
    inp.style.display = "block";
    txt.style.display = "none";
    img.style.display = "none";
    vdo.style.display = "none";
  }
}
function stopVideo() {
  var video = document.getElementById("Vdo");
  video.pause();
  video.currentTime = 0;
}

function blogChk() {
  imgfld = document.getElementById("imgField");
  vdofld = document.getElementById("videoField");
  imgfld.style.display = "none";
  vdofld.style.display = "none";
  var fileInput = document.getElementById("inFile");
  var img = document.getElementById("Img");
  var vdo = document.getElementById("Vdo");
  if (fileInput) {
    var filePath = fileInput.value;
    // Allowing file type
    var allowedImageExtensions = /(\.jpg|\.jpeg|\.png)$/i;
    var allowedVideoExtensions = /(\.mp4|\.mkv|\.avi)$/i;
    if (allowedImageExtensions.exec(filePath)) {
      var reader = new FileReader();
      reader.onload = function (e) {
        img.src = e.target.result;
      };
      reader.readAsDataURL(fileInput.files[0]);
      document.getElementById("Btype").value = "2";
      imgfld.style.display = "block";
      document.getElementById("Submit").disabled = false;
    } else if (allowedVideoExtensions.exec(filePath)) {
      var reader = new FileReader();
      reader.onload = function (e) {
        vdo.src = e.target.result;
      };
      reader.readAsDataURL(fileInput.files[0]);
      document.getElementById("Btype").value = "3";
      vdofld.style.display = "block";
      document.getElementById("Submit").disabled = false;
    } else {
      // Image preview
      if (fileInput.files && fileInput.files[0]) {
        alert("Invalid file type");
        fileInput.value = "";
        img.src = "";
        document.getElementById("Submit").disabled = true;
      }
    }
  } else {
    console.log(fileInput);
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
  dayChoose();
}

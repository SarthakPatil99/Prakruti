function sendEmail() {
    let x = Math.floor((Math.random() * 1000000) + 1);
    eml = document.getElementById("emailFP").value
    alert(eml)
      Email.send({
        Host: "smtp.gmail.com",
        Username: "getyourprakruti@gmail.com",
        Password: "mxgrtbsoevwiwnqb",
        To: eml,
        From: "getyourprakruti@gmail.com",
        Subject: "Sending Email using javascript",
        Body: "Your OTP : "+x.toString(),
      })
        .then(function (message) {
          alert("mail sent successfully")
        });
    }
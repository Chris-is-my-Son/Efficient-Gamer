if (document.URL.includes('contact.html')) {
	window.alert("Please Fill Out All Information!");
}

let emailCheckButton = document.getElementById("emailCheck");
let emailStatus = document.getElementById("emailStatus");
let emailValue = document.getElementById("myEmail");
let zipCode = document.getElementById("zipCode");
let zipStatus = document.getElementById("zipStatus");

zipCode.addEventListener("input", function() {
	var zip = zipCode.value;

	var xhr = new XMLHttpRequest();
	xhr.open("GET", "verify-zip.php?zip=" + zip);

	xhr.onload = function() {
		zipStatus.textContent = xhr.responseText;
	};

	xhr.send();
	zipStatus.textContent = "";
});

emailCheckButton.onclick = function() {
	if(emailValue.value.includes("gmail.com")) {
		emailStatus.innerHTML = emailValue.value + " contains @gmail.com and is invalid"
	} else if (emailValue.value == "") {
		emailStatus.innerHTML = "Please enter an email to check"
	} else {
		emailStatus.innerHTML = emailValue.value + " is a valid email"

	}
}

function validation() {
	//Storing the textbox value of myEmail in a variable
	let emailValue = document.getElementById("myEmail").value;
	//Storing "@" in a variable
	let atPosition = emailValue.indexOf("@");
	//Storing "." in a variable
	let dotPosition = emailValue.indexOf(".");
	//Storing the textbox value of myName in a variable
	let fullName = document.getElementById("myName").value;
	//Storing the textbox value of myGame in a variable
	let gameSelection = document.getElementById("myGame").value;
	//Running my try catch statement
	try {
		//Checking the position of the "@" and "." characters
		if (atPosition<1 || dotPosition<atPosition+2 || dotPosition+2>=emailValue.length || emailValue.includes("gmail.com"))
			//Throw message
			throw "Not a valid e-mail address";
	} catch(err) {
		//Window alert box presenting the throw message
		window.alert(err);
	}
	
	try {
		//Checking for empty strings in myName and myGame
		if (fullName == "" || gameSelection == "")
			//Throw message
			throw "Please Fill Out The Form";
	} catch(err) {
		//Window alert box presenting the throw message
		window.alert(err);
	}
}


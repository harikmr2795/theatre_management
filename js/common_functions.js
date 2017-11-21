function toastMessage(message) {
    var msg = document.getElementById("toastMessage");
    msg.innerHTML = message;
    msg.className = "show";
    setTimeout(function() { msg.className = msg.className.replace("show", ""); }, 4000);
}
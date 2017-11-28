function validate() {
    var name = document.getElementById("name").value;
    var capacity = document.getElementById("capacity").value;
    if (name == '' || capacity == '') {
        toastMessage('Name and Capacity must be filled');
        return false;
    } else if (!(capacity < 10000)) {
        toastMessage('Capacity must be less than 10,000');
        return false;
    } else if (!(capacity > 0)) {
        toastMessage('Capacity must be at least 1');
        return false;
    } else {
        document.getElementById("name").value = "";
        document.getElementById("capacity").value = "";
        add(name, capacity);
    }
}

function add(name, capacity) {
    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatre_management/v1/theatre_management",{
//     fetch("http://localhost:8080/_ah/api/theatre_management/v1/theatre_management",{
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "name": name, "capacity": capacity })
        })
        .then((response) => response.json())
        .then((data) => toastMessage(data.message))
        .catch((error) => console.log(error));
}
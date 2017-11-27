function load() {
    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatre_management/v1/theatre_management", { method: 'get' })
    // fetch("http://localhost:8080/_ah/api/theatre_management/v1/theatre_management", { method: 'get' })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            var tbody = document.getElementById("tb");
            if (!(data.items)) tbody.innerHTML = "<tr><td colspan='2'>No shows available</td></tr>";
            else {
                tbody.innerHTML = "";
                for (var i = 0; i < data.items.length; i++) {
                    var sold = data.items[i].capacity - data.items[i].available
                    tbody.innerHTML += "<tr><td>" + data.items[i].name + "</td><td>" + sold + "</td><td class='transparent'><button onclick='remove(this);' id='key' class='transparent' value = " + data.items[i].key + ">Remove</button></td></tr>";
                }
            }
        })
        .catch((error) => console.log(error));
}

function remove(data) {
    console.log(data.value);
    // fetch("http://localhost:8080/_ah/api/theatre_management/v1/theatre_management/" + data.value, { method: 'delete' })
    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatreManagement/v1/theatreManagement/" + data.value, { method: 'delete' })
        .then((response) => response.json())
        .then((data) => {
            toastMessage(data.message);
            setTimeout(function(){ load(); }, 300);
        })
        .catch((error) => console.log(error));
}
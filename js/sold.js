function load() {
    // fetch("http://localhost:8080/_ah/api/theatre_management/v1/theatre_management", { method: 'get' })
    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatre_management/v1/theatre_management", { method: 'get' })
        .then((response) => response.json())
        .then((data) => {
            var tbody = document.getElementById("tb");
            if (!(data.items)) tbody.innerHTML = "<tr><td colspan='3'>No shows available</td></tr>";
            else {
                for (var i = 0; i < data.items.length; i++) {
                    var sold = data.items[i].capacity - data.items[i].available;
                    tbody.innerHTML += "<tr><td>" + data.items[i].name + "</td><td>" + sold + "</td><td>" + data.items[i].available + "</td></tr>";
                }
            }
        }).catch((error) => console.log(error));
}
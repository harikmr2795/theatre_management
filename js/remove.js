function load() {
    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatreManagement/v1/show/list")
        .then((response) => response.json())
        .then((data) => {
            var tbody = document.getElementById("tb");
            if (!(data.items)) tbody.innerHTML = "<tr><td colspan='2'>No shows available</td></tr>";
            else {
                tbody.innerHTML = "";
                for (var i = 0; i < data.items.length; i++) {
                    var sold = data.items[i].capacity - data.items[i].available
                    tbody.innerHTML += "<tr><td>" + data.items[i].name + "</td><td>" + sold + "</td><td class='transparent'><button onclick='remove(this);' id='key' class='transparent' value = " + data.items[i].entityKey + ">Remove</button></td></tr>";
                }
            }
        })
        .catch((error) => console.log(error));
}

function remove(data) {
    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatreManagement/v1/show/delete/" + document.getElementById("key").value , { method: 'delete' })
        .then((response) => response.json())
        .then((data) => {
            toastMessage(data.name);
            setTimeout(load(), 300);
        })
        .catch((error) => console.log(error));
}
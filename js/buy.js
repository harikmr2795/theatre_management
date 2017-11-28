function load() {
//    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatre_management/v1/theatre_management", { method: 'get' })
     fetch("http://localhost:8080/_ah/api/theatre_management/v1/theatre_management", { method: 'get' })
        .then((response) => response.json())
        .then((data) => {
            var content = document.getElementById("content");
            if (!(data.items)) content.innerHTML = "<table> <thead> <tr> <th>Show Name</th> <th>Tickets Available</th> </tr></thead><tbody><tr><td colspan='2'>No shows available</td></tr></tbody></table>";
            else {
                content.innerHTML = "<table> <thead> <tr> <th>Show Name</th> <th>Tickets Available</th> </tr></thead><tbody id='tb'></tbody></table>";
                for (var i = 0; i < data.items.length; i++) {
                    document.getElementById("tb").innerHTML += "<tr><td>" + data.items[i].name + "</td><td>" + data.items[i].available + "</td><td class='transparent'><button onclick='details(this);' class='transparent' value = " + data.items[i].token + ">Details</button></td></tr>";
                }
            }
        })
        .catch((error) => console.log(error));
}

function details(key) {
//    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatre_management/v1/theatre_management", { method: 'get' })
     fetch("http://localhost:8080/_ah/api/theatre_management/v1/theatre_management", { method: 'get' })
        .then((response) => response.json())
        .then((data) => {
            for (var i = 0; i < data.items.length; i++) {
                console.log(key.value, data.items[i].token);
                if (key.value === data.items[i].token) {
                    document.getElementById("content").innerHTML = "<form><table><tr><td>Show Name: " + data.items[i].name + " </td></tr><tr><td>Total Seats: " + data.items[i].capacity + " </td></tr><tr><td>Tickets Available: " + data.items[i].available + " </td></tr><tr><td><input id='tickets' type='number' align='center' placeholder='No. of tickets' required></td></tr><tr><td class='transparent'><button id='key' onclick='validate()' type='button' value='" + data.items[i].token + "' class='transparent'>Book</button></td></tr></table></form>";
                    break;
                }
            }
        })
        .catch((error) => console.log(error));
}

function validate() {
    var tickets = parseInt(document.getElementById("tickets").value);
    document.getElementById("tickets").value = '';
    if (isNaN(tickets)) {
        toastMessage('Enter the no. of tickets to book');
        return false;
    }
//    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatre_management/v1/theatre_management", { method: 'get' })
     fetch("http://localhost:8080/_ah/api/theatre_management/v1/theatre_management", { method: 'get' })
        .then((response) => response.json())
        .then((data) => {
            for (var i = 0; i < data.items.length; i++) {
                if (document.getElementById("key").value === data.items[i].token) {
                    if (tickets > data.items[i].available) {
                        toastMessage('Oops. We don\'t have that many tickets');
                        return false;
                    } else if (tickets < 1) {
                        toastMessage('Book at least 1 ticket');
                        return false;
                    } else {
                        var successMessage = tickets + " tickets booked successfully.";
                        var json_data = {
                            'tickets': tickets
                        }
                        book(json_data, data.items[i].token);
                    }
                }
            }
        });
}

function book(data, key) {
//    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatre_management/v1/theatre_management/"+key, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
     fetch("http://localhost:8080/_ah/api/theatre_management/v1/theatre_management/"+key, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then((response) => response.json())
        .then((data) => {
            toastMessage(data.message);
            setTimeout(function(){ load(); }, 300);
        });
}
function load() {
    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatreManagement/v1/show/list")
        .then((response) => response.json())
        .then((data) => {
            var content = document.getElementById("content");
            if (!(data.items)) content.innerHTML = "<table> <thead> <tr> <th>Show Name</th> <th>Tickets Available</th> </tr></thead><tbody><tr><td colspan='2'>No shows available</td></tr></tbody></table>";
            else {
                content.innerHTML = "<table> <thead> <tr> <th>Show Name</th> <th>Tickets Available</th> </tr></thead><tbody id='tb'></tbody></table>";
                for (var i = 0; i < data.items.length; i++) {
                    document.getElementById("tb").innerHTML += "<tr><td>" + data.items[i].name + "</td><td>" + data.items[i].available + "</td><td class='transparent'><button onclick='details(this);' class='transparent' value = " + data.items[i].entityKey + ">Details</button></td></tr>";
                }
            }
        })
        .catch((error) => console.log(error));
}

function details(key) {
    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatreManagement/v1/show/list")
        .then((response) => response.json())
        .then((data) => {
            for (var i = 0; i < data.items.length; i++) {
                if (key.value === data.items[i].entityKey) {
                    $('.content').empty().append("<form><table><tr><td>Show Name: " + data.items[i].name + " </td></tr><tr><td>Total Seats: " + data.items[i].capacity + " </td></tr><tr><td>Tickets Available: " + data.items[i].available + " </td></tr><tr><td><input id='tickets' type='number' align='center' placeholder='No. of tickets' required></td></tr><tr><td class='transparent'><button id='entityKey' onclick='validate()' type='button' value='" + data.items[i].entityKey + "' class='transparent'>Book</button></td></tr></table></form>");
                    break;
                }
            }
        })
        .catch((error) => console.log(error));
}

function validate() {
    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatreManagement/v1/show/list")
        .then((response) => response.json())
        .then((data) => {
            for (var i = 0; i < data.items.length; i++) {
                if (document.getElementById("entityKey").value === data.items[i].entityKey) {
                    var tickets = parseInt($("#tickets").val());
                    if (tickets == '') {
                        toastMessage('Enter the no. of tickets to book');
                        return false;
                    } else if (tickets > data.items[i].available) {
                        toastMessage('Oops. We don\'t have that many tickets');
                        return false;
                    } else if (tickets < 1) {
                        toastMessage('Book atleast 1 ticket');
                        return false;
                    } else {
                        var successMessage = tickets + " tickets booked successfully.";
                        var data = {
                            "entityKey": data.items[i].entityKey,
                            "available": data.items[i].available - $("#tickets").val()
                        }
                        book(successMessage, data);
                    }
                }
            }
        });
}

function book(successMessage, data) {
    fetch("https://theatre-management-182106.appspot.com/_ah/api/theatreManagement/v1/show/book", { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then((response) => response.json())
        .then((data) => {
            toastMessage(successMessage);
            setTimeout(function() { load(); }, 300);
        });
}
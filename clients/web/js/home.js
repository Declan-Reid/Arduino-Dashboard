const serverIp = 'arduino.declan-reid.me';
const serverPort = 2053;
const socketUrl = `wss://${serverIp}:${serverPort}`;

function connect() {
    const socket = new WebSocket(socketUrl);

    socket.onopen = () => {
        console.log('Connected to server');
        socket.send('get_all_panels');
        setInterval(function(){
            socket.send('get_all_panels');
        }, 500);
    };

    socket.onmessage = (event) => {
        data_raw = event.data

        if (data_raw.startsWith("error"))
        {
            document.getElementById("grid-container").innerHTML = "<h1>Something went wrong... oops!</h1>"

            return;
        }

        data = JSON.parse(event.data);

        switch (data['request'])
        {
            case "get_all_panels":
                body_html = ''

                for (i in data['body'])
                {
                    panel_data = JSON.parse(data['body'][i])

                    body_html += `<div class="panel" id="panel-${parseInt(i)+1}">`

                    body_html += `<div><h3>${panel_data['name']}</h3><div class="status ${panel_data['status_colour']} small"></div></div>`

                    body_html += `<hr>`
                    
                    body_html += `<div class="info-container">`

                    for (j in panel_data)
                    {
                        if (j != "name" && j != "status_colour") body_html += `<div class="two-column-text"><p><b>${j}</b></p><p>${panel_data[j]}</p></div>`
                    }

                    body_html += `</div>`

                    body_html += `</div>`
                }

                document.getElementById("grid-container").innerHTML = body_html

                break;
        }
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        document.getElementById("grid-container").innerHTML = "<h1>Failed to connect to WebSocket server.";
    };

    socket.onclose = () => {
        console.log('Connection closed. Reconnecting...');
        setTimeout(connect, 1000); // Retry after 1 second
    };
}

connect(); // Start the connection
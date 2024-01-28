setInterval(function() {
    $.ajax({
        url: '/temperature',
        type: 'GET',
        success: function(data) {
            $('#temperature').text('Temperature: ' + data);
        },
        error: function(error) {
            $('#temperature').text('Temperature: Not available!');
            console.log(error);
        }
    });
}, 2500);

$(document).on('change', '.api-checkbox', function() {
    var anyChecked = $('.api-checkbox:checked').length > 0;
    $('#download-button-dialog').toggle(anyChecked);
});

function createCheckboxes(data) {
    $.each(data, function(index, value) {
        var checkbox = $('<input/>', {
            type: 'checkbox',
            id: 'checkbox' + index,
            value: value,
            'class': 'api-checkbox'
        });
        var label = $('<label/>', {
            for: 'checkbox' + index,
            text: value
        });
        $('#checkbox-dialog').append(checkbox, label);
    });
}

$( "#dialog" ).dialog({
    width: 450,
    // height: 400,
    autoOpen: false,
    open: function(event, ui) {
        $('#checkbox-dialog').empty();
        $.ajax({
            url: '/listreports',
            type: 'GET',
            success: function(data) {
                if (data === null || data.length === 0) {
                    $('#checkbox-dialog').text('No reports available!');
                } else {
                    createCheckboxes(data);
                }
            },
            error: function(error) {
                $('#checkbox-dialog').text('No reports available!');
                console.log(error);
            }
        });
    }
});

$( "#download-button" ).click(function() {
    $( "#dialog" ).dialog( "open" );
});

function getSelectedCheckboxes() {
    var checkboxes = [];
    $('.api-checkbox:checked').each(function() {
        checkboxes.push($(this).val());
    });
    return checkboxes;
}

$('#download-button-dialog').click(function() {
    var checkboxes = getSelectedCheckboxes();
    if (checkboxes.length > 0) {
        $.ajax({
            url: '/download_files',
            type: 'POST',
            data: JSON.stringify(checkboxes),
            contentType: 'application/json',
            success: function(data) {
               // Handle success
            },
            error: function(error) {
               // Handle error
            }
        });
    }
});

$(document).ready(function() {
    var ws;

    $('#startbutton').click(function() {
        var loc = window.location;
        var wsUrl = ((loc.protocol === "https:") ? "wss://" : "ws://") + loc.host + loc.pathname + "/start";
        ws = new WebSocket(wsUrl);

        ws.onopen = function() {
            console.log('WebSocket connection opened');
            $('#websocket').empty();
        };

        ws.onmessage = function(event) {
            console.log('Received data: ', event.data);
            $('#websocket').append('<p>' + event.data + '</p>');
        };

        ws.onclose = function() {
            console.log('WebSocket connection closed');
        };

        ws.onerror = function(error) {
            console.log('WebSocket error: ', error);
        };
    });

    $('#stopbutton').click(function() {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.close();
        }
        $('#websocket').hide();
        $.ajax({
            url: '/stop',
            type: 'POST',
            success: function(response) {
                console.log('POST request successful');
            },
            error: function(error) {
                console.log('POST request failed: ', error);
            }
        });
    });

    $('#testbutton').click(function() {
        var loc = window.location;
        var wsUrl = ((loc.protocol === "https:") ? "wss://" : "ws://") + loc.host + loc.pathname + "/test";
        ws = new WebSocket(wsUrl);

        ws.onopen = function() {
            console.log('WebSocket connection opened');
            $('#websocket').empty();
        };

        ws.onmessage = function(event) {
            console.log('Received data: ', event.data);
            $('#websocket').append('<p>' + event.data + '</p>');
        };

        ws.onclose = function() {
            console.log('WebSocket connection closed');
        };

        ws.onerror = function(error) {
            console.log('WebSocket error: ', error);
        };
    });
});

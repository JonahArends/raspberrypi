function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

setInterval(function() {
    $.ajax({
        url: '/temperature',
        type: 'GET',
        success: function(data) {
            if (data !== '403') {
                $("#bmp280").css("background-color", "green");
                $("#bmp280").attr("title", "Online");
                $('#temperature').text('Temperature: ' + data);
            } else {
                $("#bmp280").css("background-color", "red");
                $("#bmp280").attr("title", "Offline");
                $('#temperature').text('Temperature: Not available!');
            }
        },
        error: function(error) {
            $("#bmp280").css("background-color", "red");
            $("#bmp280").attr("title", "Offline");
            $('#temperature').text('Temperature: Not available!');
        },
    });
    $.ajax({
        url: '/state/ky020',
        type: 'GET',
        success: function(data) {
            if (data === 'true') {
                $("#ky020").css("background-color", "green");
                $("#ky020").attr("title", "Online");
            } else {
                $("#ky020").css("background-color", "red");
                $("#ky020").attr("title", "Offline");
            }
        },
        error: function(error) {
            $("#ky020").css("background-color", "red");
            $("#ky020").attr("title", "Offline");
        }
    });
    $.ajax({
        url: '/state/ttp223',
        type: 'GET',
        success: function(data) {
            if (data === 'true') {
                $("#ttp223").css("background-color", "green");
                $("#ttp223").attr("title", "Online");
            } else {
                $("#ttp223").css("background-color", "red");
                $("#ttp223").attr("title", "Offline");
            }
        },
        error: function(error) {
            $("#ttp223").css("background-color", "red");
            $("#ttp223").attr("title", "Offline");
        }
    });
    $.ajax({
        url: '/state/led',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var colorMapping = {
                "26": "green",
                "16": "yellow",
                "20": "red",
                "21": "orange"
            };
            for (var key in data) {
                var color = colorMapping[key];
                if (data[key] === true) {
                    $("#led_" + color).css("background-color", color);
                } else {
                    $("#led_" + color).css("background-color", 'grey');
                }
            }
        },
        error: function(error) {
            $("#led_green").css("background-color", 'grey')
            $("#led_yellow").css("background-color", 'grey')
            $("#led_red").css("background-color", 'grey')
            $("#led_orange").css("background-color", 'grey');
        }
    });
    $.ajax({
        url: '/state/fan',
        type: 'GET',
        success: function(data) {
            if (data === 'true') {
                $("#fan").css("background-color", "green");
                $("#fan").attr("title", "Online");
            } else {
                $("#fan").css("background-color", "red");
                $("#fan").attr("title", "Offline");
            }
        },
        error: function(error) {
            $("#fan").css("background-color", "red");
            $("#fan").attr("title", "Offline");
        }
    });
}, 5000);

$('#startbutton').click(function() {
    $.ajax({
        url: '/start',
        type: 'POST',
        success: function (data) {
            $("#script").css("background-color", "green");
            $("#script").attr("title", "Running");
        },
        error: function (error) {
            $("#script").css("background-color", "red");
            $("#script").attr("title", "Stopped");
        }
    });
    alert("The script has been started");
});

$('#stopbutton').click(function () {
    var confirmation = confirm("The script will be stopped!");
    if (confirmation) {
        $.ajax({
            url: '/stop',
            type: 'POST',
            success: function (data) {
                $("#script").css("background-color", "red");
                $("#script").attr("title", "Stopped");
            },
            error: function (error) {
                $("#script").css("background-color", "red");
                $("#script").attr("title", "Error");
            }
        });
    }
});

$('#testbutton').click(function() {
    var confirmation = confirm(`While the test runs, the script can't be started!
As long as the test runs, the script will be stopped!`);
    if (confirmation) {
        if ($("#script").css("background-color") === 'green') {
            $.ajax({
                url: '/stop',
                type: 'POST',
                success: function (data) {
                    $("#script").css("background-color", "red");
                    $("#script").attr("title", "Stopped");
                },
            });
        }
        $("#startbutton").attr("type", "disabled")
        $.ajax({
            url: '/test',
            type: 'POST',
            success: function (data) {
                $("#test").css("background-color", "gray");
                $("#test").attr("title", "Running");
                sleep(5000).then(() => {
                    $("#test").css("background-color", "green");
                    $("#test").attr("title", "Successful");
                });
            },
            error: function (error) {
                $("#test").css("background-color", "red");
                $("#test").attr("title", "Error");
            }
        });
        sleep(5000).then(() => { $("#startbutton").attr("type", "button") });
    }
});

$(window).ready(function () {
    sleep(5000).then(() => { $("#loader").fadeOut("slow") });
});

// $(document).on('change', '.api-checkbox', function() {
//     var anyChecked = $('.api-checkbox:checked').length > 0;
//     $('#download-button-dialog').toggle(anyChecked);
// });

// function createCheckboxes(data) {
//     $.each(data, function(index, value) {
//         var checkbox = $('<input/>', {
//             type: 'checkbox',
//             id: 'checkbox' + index,
//             value: value,
//             'class': 'api-checkbox'
//         });
//         var label = $('<label/>', {
//             for: 'checkbox' + index,
//             text: value
//         });
//         $('#checkbox-dialog').append(checkbox, label);
//     });
// }

// $( "#dialog" ).dialog({
//     width: 450,
//     // height: 400,
//     autoOpen: false,
//     open: function(event, ui) {
//         $('#checkbox-dialog').empty();
//         $.ajax({
//             url: '/listreports',
//             type: 'GET',
//             success: function(data) {
//                 if (data === null || data.length === 0) {
//                     $('#checkbox-dialog').text('No reports available!');
//                 } else {
//                     createCheckboxes(data);
//                 }
//             },
//             error: function(error) {
//                 $('#checkbox-dialog').text('No reports available!');
//                 console.log(error);
//             }
//         });
//     }
// });

// $( "#download-button" ).click(function() {
//     $( "#dialog" ).dialog( "open" );
// });

// function getSelectedCheckboxes() {
//     var checkboxes = [];
//     $('.api-checkbox:checked').each(function() {
//         checkboxes.push($(this).val());
//     });
//     return checkboxes;
// }

// $('#download-button-dialog').click(function() {
//     var checkboxes = getSelectedCheckboxes();
//     if (checkboxes.length > 0) {
//         $.ajax({
//             url: '/download_files',
//             type: 'POST',
//             data: JSON.stringify(checkboxes),
//             contentType: 'application/json',
//             success: function(data) {
//                // Handle success
//             },
//             error: function(error) {
//                // Handle error
//             }
//         });
//     }
// });

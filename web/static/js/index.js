setInterval(function() {
    $.ajax({
        url: '/temperature',
        type: 'GET',
        success: function(data) {
            $('#temperature').text('Temperature: ' + data);
            $("#bmp280").css("background-color", "green");
        },
        error: function(error) {
            $('#temperature').text('Temperature: Not available!');
            $("#bmp280").css("background-color", "red");
            console.log(error);
        }
    });
    $.ajax({
        url: '/state/ky020',
        type: 'GET',
        success: function(data) {
            $("#ky020").css("background-color", "green");
        },
        error: function(error) {
            $("#ky020").css("background-color", "red");
            console.log(error);
        }
    });
    $.ajax({
        url: '/state/ttp223',
        type: 'GET',
        success: function(data) {
            $("#ttp223").css("background-color", "green");
        },
        error: function(error) {
            $("#ttp223").css("background-color", "red");
            console.log(error);
        }
    });
    $.ajax({
        url: '/state/led',
        type: 'GET',
        success: function(data) {
            for (var key in data) {
                if (data[key] === true) {

                } else if (data[key] === false) {

                }
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
    $.ajax({
        url: '/state/fan',
        type: 'GET',
        success: function(data) {
            var colorMapping = {
                "26": "green",
                "16": "yellow",
                "20": "red",
                "21": "orange"
            };
            for (var key in data) {
                var color = colorMapping[key];
                if (data[key]) {
                    $("#led_" + color).css("background-color", color);
                }
            }
        },
        error: function(error) {
            $("#fan_").css("background-color", "red");
            console.log(error);
        }
    });
}, 5000);

$('#startbutton').click(function() {
    alert("The script has been started");
    $.ajax({
        url: '/start',
        type: 'POST',
        success: function (data) {
            $("#script").css("background-color", "green");
        },
        error: function (error) {
            $("#script").css("background-color", "red");
            console.log(error);
        }
    });
});

$('#stopbutton').click(function () {
    var confirmation = confirm("The script will be stopped!");
    if (confirmation) {
        $.ajax({
            url: '/stop',
            type: 'POST',
            success: function (data) {
                $("#script").css("background-color", "red");
            },
            error: function (error) {
                $("#script").css("background-color", "white");
                console.log(error);
            }
        });
    }
});

$('#testbutton').click(function() {
    alert("The test has been started");
    $.ajax({
        url: '/test',
        type: 'POST',
        success: function (data) {
            $("#script").css("background-color", "green");
        },
        error: function (error) {
            $("#script").css("background-color", "red");
            console.log(error);
        }
    });
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

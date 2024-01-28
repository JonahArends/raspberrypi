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
}, 1000);

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

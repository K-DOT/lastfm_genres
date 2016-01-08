function displayChart(data) {
    var chart = new CanvasJS.Chart("chartContainer", {
        data: [              
            {
            type: "pie",
            dataPoints: data
            }
        ]
    });
    chart.render();
}

function progressbar(action) {
    if (action == 'show') {
        $('.wait').show();
    }   else {
            $('.wait').hide();
    }
}

$(document).ready(function() {
    $('#submitbutton').click(function() {
        $.ajax({
            type: 'POST',
            url: '/start_task',
            data : $('#form').serialize(),
            success: function(data, status, request) {
                status_url = request.getResponseHeader('Location');
                update_progress(status_url);
            },
            error: function() {
                alert('Unexpected error');
            }
        });
    });
}); 

function update_progress(status_url) {
    $.getJSON(status_url, function (data) {
        if (data['state'] == 'PENDING') {
            $('.error').hide();
            progressbar('show');
            setTimeout(function() {
                update_progress(status_url);
            }, 2000);
        }   else if (data['error']) {
                $('.error').append(data['error']);
                $('.error').show();
                progressbar('hide');
            }    
            else {
                progressbar('hide');
                displayChart(data);
            }
    }); 
}
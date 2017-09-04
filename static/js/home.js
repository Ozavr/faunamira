/**
 * Created by Max on 10.08.2017.
 */

// функция получения csrf_token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// результаты фильтрации по животным
function get_animal_results() {
    var kind = $('#animal_filter #id_kind').val(),
        gender = $('#animal_filter #id_gender').val(),
        age = $('#animal_filter #id_age').val(),
        csrf = getCookie('csrftoken'),
        data = {
            'kind' : kind,
            'gender' : gender,
            'age' : age,
            'csrfmiddlewaretoken' : csrf
        };
    $.ajax(
        {
            url : 'animal_results/',
            type : 'POST',
            data : data,
            dataType: 'json',
            success: function (response) {
                $('#block_content').html(response.html_content);
            },
            error: function (xhr, status, error) {
                console.log('error =', error);
            }
        }
    )
}
$(document).ready(function () {
    $('#animal_filter #animal_filter_button').click(function () {
        get_animal_results();
    });
})

// результаты фильтрации по людям
function get_people_results() {
    var gender = $('#people_filter #id_gender').val(),
        age = $('#people_filter #id_age').val(),
        hobbies = $('#people_filter #id_hobbies').val(),
        csrf = getCookie('csrftoken'),
        data = {
            'gender' : gender,
            'age' : age,
            'hobbies' : hobbies,
            'csrfmiddlewaretoken' : csrf
        };
    $.ajax(
        {
            url : 'people_results/',
            type : 'POST',
            data : data,
            dataType : 'json',
            success: function (response) {
                console.log('ok');
                $('#block_content').html(response.html_content);
            },
            error: function (xhr, status, error) {
                console.log('error =', error);
            }
        }
    )
}

$(document).ready(function () {
    $('#people_filter #people_filter_button').click(function () {
        get_people_results();
    });
})
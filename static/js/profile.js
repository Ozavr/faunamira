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

// загрузка формы для редактирования информации обо мне
function get_about_edit_form () {
    $.ajax(
        {
            url: '/profile/get_edit_about/',
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                $('#about').html(response.html_content);
                $('#about #about-submit').attr('id', 'about-submit-edit');
                $('#about #about-submit-edit').prop('type', 'button');
                $('#about #about-submit-edit').click(function () {
                    post_about_edit_form();
                });
            },
            error: function (xhr, status, error) {
                console.log('error: ', error);
            }
        }
    )
}

$(document).ready(function () {
    $('#about #about-edit').click(function () {
        get_about_edit_form();
    })
})

function post_about_edit_form() {
    var data = {
        'find' : $('#about select[name=find]').val(),
        'purpose' : $('#about select[name=purpose]').val(),
        'about_me' : $('#about textarea[name=about_me]').val(),
        'csrfmiddlewaretoken' : getCookie('csrftoken')
    };
    $.ajax(
        {
            url: '/profile/post_edit_about/',
            type: 'POST',
            dataType: 'json',
            data: data,
            success: function (response) {
                console.log(response.reload);
                if (response.reload) {
                    location.reload();
                } else {
                    $('#about').html(response.html_content);
                }
            },
            error: function (xhr, status, error) {
                console.log('error: ', error);
            }
        }
    )
}

function get_similar_people(username) {
    var data = {
        'username': username,
        'csrfmiddlewaretoken': getCookie('csrftoken')
    };
    $.ajax(
        {
            url: '/profile/get_similar_people/',
            type: 'POST',
            dataType: 'json',
            data: data,
            success: function (response) {
                $('#block_similar_people').html(response.html_content);
                $('#similar_people_form').hide();
            },
            error: function (xhr, status, error) {
                console.log('error: ', error);
            }
        }
    )

}



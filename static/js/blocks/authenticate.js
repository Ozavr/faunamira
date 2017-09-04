/**
 * Created by Max on 17.08.2017.
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

// логин пользователя
function user_login() {
    var login = $('#login_form input[name=login]').val(),
        password = $('#login_form input[name=password]').val(),
        csrf = getCookie('csrftoken'),
        data = {
            'login' : login,
            'password' : password,
            'csrfmiddlewaretoken' : csrf
        };
    $.ajax(
        {
            url : '/user_login/',
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (response) {
                if (response.reload) {
                    location.reload();
                } else {
                   $('#block_user').html(response.html_content);
                }
            },
            error: function (response, xhr, status, error) {
                console.log('error:', error);
            }
        }
    )
}

$(document).ready(function () {
    $('#login_form #login_button').click(function () {
        user_login();
    });
})


// регистрация пользователя
function user_signup() {
    var username = $('#signup_form input[name=username]').val(),
        password1 = $('#signup_form input[name=password1]').val(),
        password2 = $('#signup_form input[name=password2]').val(),
        csrf = getCookie('csrftoken'),
        data = {
            'username' : username,
            'password1' : password1,
            'password2' : password2,
            'csrfmiddlewaretoken' : csrf
        };
    $.ajax(
        {
            url : '/user_signup/',
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (response) {
                if (response.reload) {
                    location.reload();
                } else {
                   $('#block_user').html(response.html_content);
                }
            },
            error: function (response, xhr, status, error) {
                console.log('error:', error);
            }
        }
    )
}

$(document).ready(function () {
    console.log('click work');
    $('#signup_form #signup_button').click(function () {
        user_signup();
    });
})
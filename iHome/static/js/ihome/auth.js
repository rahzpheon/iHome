function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // TODO: 查询用户的实名认证信息
    // 若用户已有信息,则不可设置
    $.get('/api/1.0/users/auth', function (response) {
        if (response.errno == 0){
            // 显示信息,
            $('#real-name').val(response.data.real_name);
            $('#id-card').val(response.data.id_card);
            // 关闭修改
            $('#real-name').attr('disabled', true);
            $('#id-card').attr('disabled', true);
            $('.btn-success').hide()

        } else {
             // TODO: 管理实名信息表单的提交行为
            $('#form-auth').submit(function (event) {
                event.preventDefault();

                var params = {
                    'real_name' : $('#real-name').val(),
                    'id_card' : $('#id-card').val()
                }

                $.ajax({
                    url:'/api/1.0/users/auth',
                    type:'post',
                    data:JSON.stringify(params),
                    contentType:'application/json',
                    headers:{'X-CSRFToken':getCookie('csrf_token')},
                    success:function (response) {
                        if (response.errno == '0'){
                            // successed.
                            showSuccessMsg();
                            // 成功之后,实名认证不可再设置
                            // 关闭修改
                            $('#real-name').attr('disabled', true);
                            $('#id-card').attr('disabled', true);
                            $('.btn-success').hide()
                        } else if (response.errno == '4101') {
                            alert(response.errmsg);
                            location.href = '/';
                        } else {
                            alert(response.errmsg);
                        }
                    }
                    });
                 });
        }
    })

    // TODO: 管理实名信息表单的提交行为
    // $('#form-auth').submit(function (event) {
    //     event.preventDefault();
    //
    //     var params = {
    //         'real_name' : $('#real-name').val(),
    //         'id_card' : $('#id-card').val()
    //     }
    //
    //     $.ajax({
    //         url:'/api/1.0/users/auth',
    //         type:'post',
    //         data:JSON.stringify(params),
    //         contentType:'application/json',
    //         headers:{'X-CSRFToken':getCookie('csrf_token')},
    //         success:function (response) {
    //             if (response.errno == '0'){
    //                 // successed.
    //                 showSuccessMsg()
    //                 // 成功之后,实名认证不可再设置
    //
    //             } else {
    //                 alert(response.errmsg)
    //             }
    //         }
    //     })
    // })
})
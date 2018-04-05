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

$(document).ready(function () {
    // TODO: 在页面加载完毕向后端查询用户的信息

    // TODO: 管理上传用户头像表单的行为
    $('#form-avatar').submit(function (event) {
        event.preventDefault();

        //　使用ajax模拟表单提交
        $(this).ajaxSubmit({
            url:'/api/1.0/users/avatar',
            type:'post',
            headers:{'X-CSRFToken': getCookie('csrf_token')},
            success:function (response) {
                if (response.errno == '0'){
                    // 显示头像
                    $('#user-avatar').attr('src', response.data);
                } else {
                    alert(response.errmsg);
                }
            }
        });
    });

    // TODO: 管理用户名修改的逻辑
    $('#form-name').submit(function (event) {
        event.preventDefault();

        // 提交修改用户名
        // 获取用户输入
        var new_name = $('#user-name').val();

         if (!new_name) {
            alert('请输入新的用户名');
        }
        var params = {
          'name':new_name
        };

        $.ajax({
            url:'/api/1.0/users/name',
            type:'put',
            data:JSON.stringify(params),
            contentType:'application/json',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function (response) {
                if (response.errno == '0'){
                    // 修改成功
                    showSuccessMsg()

                } else {
                    alert(response.errmsg)
                }
            }
        })
    })

});


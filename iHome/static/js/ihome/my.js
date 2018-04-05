function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// TODO: 点击推出按钮时执行的函数
function logout() {
    
}

$(document).ready(function(){

    // TODO: 在页面加载完毕之后去加载个人信息
    $.get('/api/1.0/users',function (response) {
        if (response.errno == "0"){
            // 加载个人信息
            var name = response.data.name;
            var mobile = response.data.mobile;

            $('#user-name').html(name);
            $('#user-mobile').html(mobile);

        } else {
            alert(response.errmsg);
            location.href = '/';
        }
    })
});

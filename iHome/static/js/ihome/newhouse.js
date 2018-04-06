function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TODO: 在页面加载完毕之后获取区域信息
    $.get('/api/1.0/areas', function (response) {
        if (response.errno == '0') {

            $.each(response.data.area_dict_list, function (i, area) {
                $('#area-id').append('<option value="' + area.aid + '">' + area.aname + '</option>');
            });

        } else {
            // $('.form-control').append('<option value="0">' + "没有地区信息" + '</option>>')
            alert(response.errmsg);
        }
    });

    // TODO: 处理房屋基本信息提交的表单数据
    $('#form-house-info').submit(function (event) {
        event.preventDefault();

        // 获取所有input标签内容
        var params = {};
        $(this).serializeArray().map(function (obj) {
            params[obj.name] = obj.value;
        });

        // 特别处理facility复选框,用列表存储所有勾选的值
        var facilities = [];
        // 所有name=facility且勾选中的勾选框
        $(':checkbox:checked[name=facility]').each(function (i, elem) {
            facilities[i] = elem.value;
        });

        params['facility'] = facilities;
        console.log(params);
        // 发送请求传递数据
        $.ajax({
            url: '/api/1.0/houses',
            type: 'post',
            data: JSON.stringify(params),
            contentType: 'application/json',
            headers: {'X-CSRFToken': getCookie('csrf_token')},
            success: function (response) {
                if (response.errno == '0') {
                    // 提交成功
                    // 隐藏房屋信息表单,显示添加图片表单
                    $('#form-house-info').hide();
                    $('#form-house-image').show();

                    // 将房屋的id设置在页面中的隐藏域中
                    $('#house-id').val(response.data.house_id)


                } else if (response.errno == '4101') {
                    alert(response.errmsg)
                    location.href = '/';
                } else {
                    alert(response.errmsg);
                }
            }
        });
    });



    // TODO: 处理图片表单的数据
    $('#form-house-image').submit(function (event) {
        event.preventDefault();

        $(this).ajaxSubmit({
            url:'/api/1.0/houses/image',
            type:'post',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function (response) {
                if (response.errno == '0'){
                    $('.house-image-cons').append('<img src="' + response.data.img_url + '">');
                } else if(response.errno == '4101'){
                    location.href = '/';
                } else {
                    alert(response.errmsg);
                }
            }
        });

    });
});



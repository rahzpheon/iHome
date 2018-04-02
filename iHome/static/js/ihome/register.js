function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}
var imageCodeId = "";
var uuid = "";
var last_uuid = "";
// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {

    // 1. 生成uuid
    uuid = generateUUID();

    // 2. 拼接请求地址
    // 并将last_uuid也拼接进来,第一次为空
    // var url = '/api/1.0/image_code?uuid=' + uuid;
    var url = '/api/1.0/image_code?uuid=' + uuid + '&last_uuid=' + last_uuid;

    // 2-2.将使用过的uuid设为last_uuid
    last_uuid = uuid

    // 3.将生成的url赋值给img标签的src
    $('.image-code>img').attr('src', url)
}

function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    // TODO: 通过ajax方式向后端接口发送请求，让后端发送短信验证码
    var params = {'uuid':uuid,
                'mobile':mobile,
                'imageCode':imageCode};

    var url = '/api/1.0/sms_code';

    $.ajax({
        url:url,
        type:'post',
        data:JSON.stringify(params),
        contentType:'application/json',
        success: function (response) {
            if (response.errno == '0'){
                // 发送成功
                alert(response.errmsg);
            } else {
                // 发送失败
                // 重新添加点击事件
                $('.phonecode-a').attr('onclick', 'sendSMSCode();');
                // 重新生成图片验证码
                generateImageCode();
                // 提示错误信息
                alert(response.errmsg);
            }
        }
    });
}

$(document).ready(function() {
    generateImageCode();  // 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });

    // TODO: 注册的提交(判断参数是否为空)
})
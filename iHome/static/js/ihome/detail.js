function hrefBack() {
    history.go(-1);
}

// 解析提取url中的查询字符串参数
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function swiper() {
    // TODO: 数据加载完毕后,需要设置幻灯片对象，开启幻灯片滚动
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    });
}

$(document).ready(function(){
    // 获取详情页面要展示的房屋编号
    var queryData = decodeQuery();
    var houseId = queryData["id"];

    // TODO: 获取该房屋的详细信息
    $.get('/api/1.0/houses/detail/' + houseId, function (response) {
        if(response.errno == '0'){
            // 使用art-template渲染页面幻灯片
            // 1.生成要渲染的html数据
            var html_swiper = template('house-image-tmpl', {'img_urls':response.data.house.img_urls, 'price':response.data.house.price});
            // 2.使用数据进行渲染
            $('.swiper-container').html(html_swiper);

            // 开启幻灯片
            swiper()

            // 使用art-template渲染房屋信息
            var html_detail = template('house-detail-tmpl', {'house':response.data.house});
            // 2.使用数据进行渲染
            $('.detail-con').html(html_detail);

            // 判断用户身份决定是否展示订房按钮
            if (response.data.house.user_id != response.login_user_id){
                // 显示按钮
                $('.book-house').attr('href', '/api/1.0/booking?hid=' + houseId)
                $('.book-house').show();

            } else {
                $('.book-house').hide();
            }
        } else {
            alert(response.errmsg);
        }
    })

})
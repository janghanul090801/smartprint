$(function () {
    function adjustFooter() {
        var height = $('.active>#showGoods').outerHeight();
        $("#footer").css({'margin-top':height+'px'})
    }
    $('.tab-menu>li>a').click(function () {
        $(this).parent().addClass("active").siblings().removeClass("active");
        adjustFooter();
        return false;
    })

    adjustFooter();
    $(window).resize(adjustFooter());
    document.querySelectorAll('.price').forEach(function(el) {
        const price = el.innerText.replace('원', '').trim();
        el.innerText = price.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + '원';
    });
});
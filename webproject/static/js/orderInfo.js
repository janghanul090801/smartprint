$(function() {
    var total = 0
    changePaymentRequired(true)
    if (list.length) {
      $("#quantity").html(list.length)
      var goodsHtml = ``;
      var cartIdList = ``;
      list.forEach(element => {
          goodsHtml += `<li class="list-group-item d-flex justify-content-between lh-sm">`;
          goodsHtml += `<div>
                          <h6 class="my-0">${element.name}</h6>
                        </div>`;
          goodsHtml += `<span class="text-body-secondary" id="price">${comma(element.price)}원</span></li>`;
          total += parseFloat(element.price)
          cartIdList += `${element.id},`
      });
      goodsHtml += `<li class="list-group-item d-flex justify-content-between">
                      <strong>총합</strong>
                      <strong>${comma(total)}원</strong>
                    </li>`
      $("#showGoods").html(goodsHtml);
      $("#cartId").val(cartIdList.slice(0, -1));
    }else {
        alert('잘못된 페이지 접근입니다.')
        window.history.back()
    }    
    $("#id_shippingWay").on('change', function() {
        if ($(this).val() == '선불') {
            $("#payment").css("display","block")
            changePaymentRequired(true)
        }
        else {
            $("#payment").css("display","none")
            changePaymentRequired(false)
        }
    })
    $("input[name=paymentMethod]").on('change',function() {
        $("#id_creditCardName").toggle(0,function() {
            $(this).attr('required',$(this).css('display') != 'none')
        });
        $("#id_debitCardName").toggle(0,function() {
            $(this).attr('required',$(this).css('display') != 'none')
        });
    })
})

function changePaymentRequired(bool) {
    $("#id_creditCardName").attr('required',bool)
    $("#id_debitCardName").attr('required',bool)
    $("#id_cardNumber").attr('required',bool)
    $("#id_expirationDate").attr('required',bool)
    $("#id_cvv").attr('required',bool)
}
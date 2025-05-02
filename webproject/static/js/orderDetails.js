function setGoods(list, cartList) {
    if (!isEmpty(list)) {
        var showGoodsHtml = ``;
        list.forEach((element) => {
            showGoodsHtml += `<tr><td id="${element.id}">${element.id}</td>`
            showGoodsHtml += `<td>${cartList.find(obj => obj.id === element.product_id).name}</td>`;
            showGoodsHtml += `<td>${element.shippingWay}</td>`;
            showGoodsHtml += `<td>${element.status}</td>`;
            showGoodsHtml += `<td>${cartList.find(obj => obj.id === element.product_id).price}</td>`;
            showGoodsHtml += `<td><button type="button"onclick='orderedCartDelete(this)' value="${element.id}" class="btn btn-outline-dark">주문취소</button></td></tr>`;
            amount += parseFloat(element.price);
        });
        $("#showGoods").html(showGoodsHtml);
    }else {
        $("#showGoods").html(`<tr><td colspan="7"><h3 id="emptyMessage">주문내역이 비었습니다.</h3></td></tr>`)
    }
}

function orderedCartDelete(element){
    let value = $(element).val();
    $(`#${value}`).each(function() {
        $(this).parent().remove();
    });

    $.ajax({
        url : '/order/orderDetails/',
        type:"POST",
        dataType:"json",
        data : {"deleteId":value},
        headers: {
            'X-CSRFToken': getCookie('csrftoken') 
        },
        success : function(response) {
            if (response.list != null){
                setGoods(response.list, cartList)
            }else {
                alert('파일 작업/시안 확인 중인 주문만 취소할 수 있습니다.')
            }
            
        },
        error : function(e) {
            console.log(e);
        }
    })
}

$(function() {
    setGoods(list, cartList)
})
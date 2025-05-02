function setGoods(list) {
    var amount = 0;
    var showGoodsHtml = "";

    if (!isEmpty(list)) {
        list.forEach((element, index) => {
            showGoodsHtml += `
                <tr id="goods" class="table-tr-height">
                    <td><input type="checkbox" name="goodsId" value="${element.id}"></td>
                    <td>${index + 1}</td>
                    <td>${element.name}</td>
                    <td>${element.imgFile}</td>
                    <td>${element.quantity} x ${element.noc}</td>
                    <td>${comma(element.price)}</td>
                    <td>
                        <button type="button" onclick='goodsDelete(this)' value="${element.id}" class="btn btn-outline-dark">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </td>
                </tr>`;
            amount += parseFloat(element.price);
        });
        $("#showGoods").html(showGoodsHtml);
    } else {
        $("#showGoods").html(`
            <tr>
                <td colspan="7"><h3 id="emptyMessage">장바구니가 비었습니다.</h3></td>
            </tr>`
        );
    }
    $("#amount").html(`합계금액 : ${comma(amount)}원`);
}


$(function() {
    setGoods(list)
});

function moveInfo() {
    if (!isEmpty(list)) {
        if (confirm("정말 주문하시겠습니까?")){
            var goodsList = $('input[name=goodsId]').map(function() {
                return $(this).val();
            }).get();
            console.log(goodsList)
            
            $("#goodsList").val(JSON.stringify(goodsList));

            $("#orderCartForm").submit();
        }
    }else {
        alert('장바구니가 비어있습니다');
    }
}

function isChecked(name) {
    var check = document.querySelectorAll(`input[name=${name}]:checked`).length;
    if (check != 0) return true
    else return false
}

function moveCheckedInfo() {
    if (!isEmpty(list)) {
        if (isChecked('goodsId')) {
            if (confirm("정말 주문하시겠습니까?")){
                getCheckedList();
                $("#orderCartForm").submit();
            }
        }else {
            alert("선택된 상품이 없습니다");
        }
    }else {
        alert('장바구니가 비어있습니다');
    }
}

function getCheckedList() {
    var goodsList = $('input[name=goodsId]:checked').map(function() {
        return $(this).val();
    }).get();
    
    $("#goodsList").val(JSON.stringify(goodsList));
}

function goodsDelete(buttonEle) {
    if(confirm("정말 삭제하시겠습니까?")){
        let value = $(buttonEle).val();
        $(`input[value="${value}"]`).each(function() {
            $(this).parent().parent().remove();
        });
        

        $.ajax({
            url : '/order/orderCart/',
            type:"POST",
            dataType:"json",
            data : {"deleteId":value},
            headers: {
                'X-CSRFToken': getCookie('csrftoken') 
            },
            success : function(response) {setGoods(response.goodsList)},
            error : function(e) {
                console.log(e);
            }
        })
    }
}

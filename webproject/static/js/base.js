function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function closeWindow(el) {
    el.css("display","none")
}

function setHeaderGoods(category, goodsList){
    var htmlStr = ``
    goodsList.forEach(el => {
        htmlStr += `<li><a href="/order/submissionForm/${category}/${el.id}" class="goods">${el.name}</a></li>`
    })
    $(`#${category}`).html(htmlStr)
}

$(function() {
    var is_open = false
    $("#showDropdown").click(function() {
        is_open = !is_open
        $(".dropdown-container").css("display",is_open?"none":"flex")
        $(".dropdown-content").css("display",is_open?"none":"block")
    })
    $(".dropdown-content").click(function(event) {
        event.stopPropagation()
    })
    $(".dropdown-container").click(function() {
        $(".dropdown-container").css("display","none")
        $(".dropdown-content").css('display',"none")
        is_open = false
    })
    $('.dropdownMenu>li>a').hover(function () {
        $(this).parent().addClass("active").siblings().removeClass("active");
        return false;
    })
    $("#submit").click(function() {
        var id = $("#id").val()
        var number = $("#lastNumber").val()
    
        numberCheck(id, number)
    })

    $.ajax({
        url: window.location.href,
        method: 'GET',
        success: function(response, textStatus, xhr) {
            var namecardList = JSON.parse(xhr.getResponseHeader('namecardList'));
            var promotionList = JSON.parse(xhr.getResponseHeader('promotionList'));
            var stickerList = JSON.parse(xhr.getResponseHeader('stickerList'));
            var envelopeList = JSON.parse(xhr.getResponseHeader('envelopeList'));
            var bookList = JSON.parse(xhr.getResponseHeader('bookList'));
            var otherList = JSON.parse(xhr.getResponseHeader('otherList'));

            setHeaderGoods('namecard',namecardList)
            setHeaderGoods('promotion',promotionList)
            setHeaderGoods('sticker',stickerList)
            setHeaderGoods('envelope',envelopeList)
            setHeaderGoods('book',bookList)
            setHeaderGoods('other',otherList)
        }
    });
})

function selectAll(selectAll, name) {
    const checkboxes
        = document.getElementsByName(name);

    checkboxes.forEach((checkbox) => {
        checkbox.checked = selectAll.checked;
    })
}

function showWindow(el) {
    $(".number-input").css("display","flex")
    $("#id").val($(el).attr("id"))
    return false
}

function numberCheck(id, number){
    if (number < 1000 || number > 9999) {
        alert('올바른 번호가 아닙니다.');
        return;
    }

    $.ajax({
        url : '/board/quoteInquiry/',
        type:"POST",
        dataType:"json",
        data : {"id":id, "number":number},
        headers: {
            'X-CSRFToken': getCookie('csrftoken') 
        },
        success : function(response) {
            if (response.is_match) {
                $(".number-input").css("display","none")
                $("#lastNumber").val('')
                window.location.href = `/board/quoteView/${id}/`
            }else {
                alert('전화번호 끝자리가 다릅니다.')
            }
        },
        error : function(e) {
            console.log(e);
        }
    })
}

function execDaumPostcode() {
    new daum.Postcode({
        oncomplete: function(data) {
            // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

            // 각 주소의 노출 규칙에 따라 주소를 조합한다.
            // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
            var addr = ''; // 주소 변수
            var extraAddr = ''; // 참고항목 변수

            //사용자가 선택한 주소 타입에 따라 해당 주소 값을 가져온다.
            if (data.userSelectedType === 'R') { // 사용자가 도로명 주소를 선택했을 경우
                addr = data.roadAddress;
            } else { // 사용자가 지번 주소를 선택했을 경우(J)
                addr = data.jibunAddress;
            }

            // 사용자가 선택한 주소가 도로명 타입일때 참고항목을 조합한다.
            if(data.userSelectedType === 'R'){
                // 법정동명이 있을 경우 추가한다. (법정리는 제외)
                // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
                if(data.bname !== '' && /[동|로|가]$/g.test(data.bname)){
                    extraAddr += data.bname;
                }
                // 건물명이 있고, 공동주택일 경우 추가한다.
                if(data.buildingName !== '' && data.apartment === 'Y'){
                    extraAddr += (extraAddr !== '' ? ', ' + data.buildingName : data.buildingName);
                }
                // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
                if(extraAddr !== ''){
                    extraAddr = ' (' + extraAddr + ')';
                }
                // 조합된 참고항목을 해당 필드에 넣는다.
                document.getElementById("extraAddress").value = extraAddr;
            
            } else {
                document.getElementById("extraAddress").value = '';
            }

            // 우편번호와 주소 정보를 해당 필드에 넣는다.
            document.getElementById('postcode').value = data.zonecode;
            document.getElementById("address").value = addr;
            // 커서를 상세주소 필드로 이동한다.
            document.getElementById("detailAddress").focus();
        }
    }).open();
}

function isEmpty(list) {
    if (list.length) {
        return false;
    }
    return true
}

function comma(str) {
    str = String(str);
    return str.replace(/(\d)(?=(?:\d{3})+(?!\d))/g, '$1,');
}
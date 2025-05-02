$(function() {
    var price = parseFloat($("#price").text())
    $("#price").text(comma(price))
    var quantity = $("#id_quantity").val()
    var noc = $("#id_noc").val()
    var paperSizes = [[420,594],[297, 420],[210,297],[148,210],[500,707],[353,500],[250,353],[182,257], [330,245], [300,215],[220,105]]
    
    function popup(){
        $("#popup_layer").css("display","block")
    }
    $(".btn-lg").click(function() {
        popup()
    })
    $("#file").on('change',function(){
        var fileName = $("#file").val();
        $(".file-name").val(fileName);
        $("#add-button").css({
            'background-color':"fa2d2d",
            'color':"#fff"
        })
    });
    $('#submissionForm').on('submit', function(el) {
        var fileInput = $('#file')[0];
        if (fileInput.files.length === 0) {
            alert('파일을 선택해 주세요.');
            el.preventDefault(); 
        }
    });
    function changePrice(){
        if (isNaN(noc)) {
            var newPrice = price * (quantity / unitQuantity); 
        }else {
            var newPrice = price * noc * (quantity / unitQuantity);
        }
        $("#price").text(comma(newPrice))
        $("#priceInput").val(newPrice);
    }
    $("#id_noc").on('input', function() { 
        noc = $(this).val()      
        changePrice()
    })
    $("#id_quantity").on('change',function() {
        quantity = $(this).val()
        changePrice()
    })
    $('#standard').on('change', function() {
        var index = parseInt($(this).val())
        if (index == 10){
            $("#id_width").attr("readonly",false)
            $('#id_height').attr("readonly",false);
            return
        }
        $("#id_width").attr("readonly",true)
        $('#id_height').attr("readonly",true);
        $('#id_width').val(paperSizes[index][0]); 
        $('#id_height').val(paperSizes[index][1]);
    })

})
function closePop() {
    $("#popup_layer").css("display","none")
}

function insertCart() {
    $("#submissionForm").submit();
}

function notLogin() {
    alert('로그인 후 이용 가능합니다.')
    window.location = '/user/login'
}
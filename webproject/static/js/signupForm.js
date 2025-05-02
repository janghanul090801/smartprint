function showEl(el) {
    el.css("display","flex")
}

function isAllChecked(name, totalN) {
    var check = document.querySelectorAll(`input[name=${name}]:checked`).length;
    if (check == totalN) return true
    else return false
}

function setPasswordInput(isOpen) {
    $(".hidden").css('display', isOpen ? 'table-row' : 'none');
    $(".password-input").attr('required', isOpen);
    $("#is-change-password").val(isOpen ? '1' : '0');
}

$(function() {
    $('#signupForm').on('submit', function(el) {
        if (!isAllChecked('terms',2)) {
            alert('약관에 동의해주세요.');
            el.preventDefault(); 
        }
    });
    var isOpen = true
    setPasswordInput(isOpen)

    $('#change-password-btn').on('click', function() {
        isOpen = !isOpen; 
        setPasswordInput(isOpen)
    });
})

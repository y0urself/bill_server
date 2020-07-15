jQuery.fn.extend({
    autoHeight: function() {
        function autoHeight_(element) {
            return jQuery(element)
                .css({
                    'height': 'auto',
                    'overflow-y': 'hidden'
                })
                .height(element.scrollHeight);
        }
        return this.each(function() {
            autoHeight_(this).on('input', function() {
                autoHeight_(this);
            });
        });
    }
});

function checkAppend() {
    var empty = false;
    var i = 0
    $(".form_row").each(function() 
    {
        console.log("Check ..." + i)
        var vendor = '#id_p-'+ i +'-vendor'
        var product_name = '#id_p-'+ i +'-product_name'
        var product_type = '#id_p-'+ i +'-product_type'
        var desc = '#id_p-'+ i +'-desc'
        console.log($(this).find('#id_p-'+ i +'-vendor').val())
        if ($(this).find('#id_p-'+ i +'-vendor').val() == '' &&
            $(this).find('#id_p-'+ i +'-product_name').val() == '' &&
            $(this).find('#id_p-'+ i +'-product_type').val() == '' &&
            $(this).find('#id_p-'+ i +'-desc').val() == ''
        )
        empty = true;
        i++
    });
    if (!empty) {
        $('#id_p-TOTAL_FORMS').val(i)
        var html = $(".form_row:first").get(0).outerHTML.replaceAll('p-0-', 'p-' + i + '-').replace(/value="(.*)" c/g, 'value="" c')
        console.log(html)
        $(".form_row:last").after(html);
    }
}

$(document).ready(function() {
    $('textarea').autoHeight();
    checkAppend()

    $('body').on('input', '.part_input', checkAppend);

    $('body').on('click', '.form_delete', function(e) {
        //TODO Only if one is left :D
        checkAppend()
        
        html = $(this).closest('.form_row').get(0).outerHTML.replace(/value="(.*)" c/g, 'value="" c')
        $(this).closest('.form_row').get(0).outerHTML = html
    });

    $('#id_date').datepicker({
        format: "dd.mm.yyyy",
        weekStart: 1,
        showOtherMonths: true,
        selectOtherMonths: true,
        daysOfWeekHighlighted: "6,0",
        autoclose: true,
        todayHighlight: true,
        changeMonth: true,
        changeYear: true,
        gotoCurrent: true,
        orientation: "bottom"
    });

    $('#id_date').datepicker("setDate", new Date());
});

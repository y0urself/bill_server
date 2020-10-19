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

function incrementIndexOfPart(part) {
    //TODO Only if one is left :D
    var elem = part.find('.part_input')
    
    var index = parseInt(elem.attr('name').replace ( /[^\d.]/g, '' ))
    console.log(index)
    
    var html_str = part.html().split('p-' + index + '-').join('p-' + (index + 1) + '-')
    html_str = html_str.replace(/value="[0-9]+" id/g, 'value="" id')
    part.html(html_str)
}

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
        console.log($(this).find('#id_p-'+ i +'-desc').val())
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
        var frow = $(".form_row:first").clone()
        frow.find('#id_p-0-vendor').val(null)
        frow.find('#id_p-0-product_name').val(null)
        frow.find('#id_p-0-product_type').val(null)
        frow.find('#id_p-0-desc').val(null)
        frow.find('#id_p-0-nprice').val(null)
        frow.find('#id_p-0-date').val(null)
        frow.find('#id_p-0-id').val(null)
        var html_str = frow.html().split('p-0-').join('p-' + i + '-')
        console.log(html_str)
        html_str = html_str.replace(/value="(.*)" c/g, 'value="" c').replace(/value="[0-9]+" id/g, 'value="" id')
        console.log(frow.html(html_str))
        $(".form_row:last").after(frow);

        $('.date_input').datepicker({
            format: "yyyy-mm-dd",
            weekStart: 1,
            showOtherMonths: true,
            selectOtherMonths: true,
            daysOfWeekHighlighted: "5,0",
            autoclose: true,
            todayHighlight: true,
            changeMonth: true,
            changeYear: true,
            gotoCurrent: true,
            orientation: "bottom"
        });
    }
}

$(document).ready(function() {
    $('textarea').autoHeight();

    // Add new form, if no empty form available
    $('body').on('input', '.part_input', checkAppend);

    // DELETE a FORM
    $('body').on('click', '.form_delete', function(e) {
        //TODO Only if one is left :D
        checkAppend()
        
        html = $(this).closest('.form_row').get(0).outerHTML.replace(/value="(.*)" c/g, 'value="" c').replace(/value="[0-9]+" id/g, 'value="" id')
        $(this).closest('.form_row').get(0).outerHTML = html
    });

    // DUPLICATE a FORM
    $('body').on('click', '.form_duplicate', function(e) {
        //TODO Only if one is left :D
        var frow = $(this).closest('.form_row').clone()
        var elem = frow.find('.part_input')
        console.log(elem)
        
        var index = parseInt(elem.attr('name').replace ( /[^\d.]/g, '' ))
        console.log(index)
        
        var html_str = frow.html().split('p-' + index + '-').join('p-' + (index + 1) + '-')
        html_str = html_str.replace(/value="[0-9]+" id/g, 'value="" id')
        frow.html(html_str)
        for(j = index + 1; j < $('#id_p-TOTAL_FORMS').val(); j++) {
            part = $('#parts_table').find('#id_p-'+ j +'-desc').closest('.form_row')
            console.log(part.html())
            incrementIndexOfPart(part)
        }
        $('#id_p-TOTAL_FORMS').val(j + 1)
        $(this).closest('.form_row').after(frow)

        $('.date_input').datepicker({
            format: "yyyy-mm-dd",
            weekStart: 1,
            showOtherMonths: true,
            selectOtherMonths: true,
            daysOfWeekHighlighted: "5,0",
            autoclose: true,
            todayHighlight: true,
            changeMonth: true,
            changeYear: true,
            gotoCurrent: true,
            orientation: "bottom"
        });
    });

    $('#id_b-date').datepicker({
        format: "yyyy-mm-dd",
        weekStart: 1,
        showOtherMonths: true,
        selectOtherMonths: true,
        daysOfWeekHighlighted: "5,0",
        autoclose: true,
        todayHighlight: true,
        changeMonth: true,
        changeYear: true,
        gotoCurrent: true,
        orientation: "bottom"
    });

    $('.date_input').datepicker({
        format: "yyyy-mm-dd",
        weekStart: 1,
        showOtherMonths: true,
        selectOtherMonths: true,
        daysOfWeekHighlighted: "5,0",
        autoclose: true,
        todayHighlight: true,
        changeMonth: true,
        changeYear: true,
        gotoCurrent: true,
        orientation: "bottom"
    });

});

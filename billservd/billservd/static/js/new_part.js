
var url = window.location.pathname.split('/');
window.qid = false;
if (url[url.length - 1] == 'edit_part') {
    window.qid = url[url.length - 2]
    //console.log(window.qid)
    socket.emit('request_part', window.qid)
}
if (url[url.length - 1] == 'duplicate_part') {
    socket.emit('request_part', url[url.length - 2])
}

socket.on('state', function(a) {
    $('#form_name').val(a.name)
    $('#form_parttype').val(a.parttype)
    $('#form_description').val(a.description)
    $('#form_bprice').val(a.bprice.replace('€','').replace(',','.'))
});

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

$(document).ready(function() {
    $('textarea').autoHeight();
    
    $("#form_add").on('click', function(e) {
        var part = {
            name: $('#form_name').val(),
            description: $('#form_description').val(),
            parttype: $('#form_parttype').val(),
            bprice: $('#form_bprice').val().replace(',','.')
        };
        console.log(part.bprice)
        if ($('#deletePart').is(':checked')) {
            socket.emit('delete_part', part);
        } else {
            socket.emit((window.qid == false ? 'new_part' : 'edit_part'), part);
        }
        e.preventDefault();
        return false;
    });
});
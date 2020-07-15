
var url = window.location.pathname.split('/');
window.qid = url[url.length - 1];
// socket.emit('request_part', window.qid)
console.log(window.qid)

// socket.on('state', function(a) {
//     $('#form_name').val(a.name)
//     $('#form_parttype').val(a.parttype)
//     $('#form_description').val(a.description)
//     $('#form_bprice').val(a.bprice.replace('€',''))
//     window.part = a
// });


// function createPDF() {
//     $.get('./'+quizID+'/tex', function(data) {
//         var pdftex = new PDFTeX('/tex/pdftex-worker.js');
//         pdftex.set_TOTAL_MEMORY(1000000).then(function(){
//             var latex_code = data
//     //         pdftex.set_TOTAL_MEMORY(250000)
//             pdftex.compile(latex_code)
//                 .then(function(pdf) {
//                     window.open(pdf)
//                 });
//         });
//     });
// }

$(document).ready(function() {
//     $('#createPDF').on('click', createPDF);
// $('#leave').on('click', function(e) {
//         $('#form_collab').val("");
//         ParsonAPP.joinCollab()
    $('#form_delete').on('click', function() {
        var part = {qid: window.qid}
        socket.emit('delete_part', part)
    });
});
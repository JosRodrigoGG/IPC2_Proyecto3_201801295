M.AutoInit();
$(document).ready(function () {
    $('textarea#textEntrada, textarea#textSalida, textarea#textConsulta').characterCounter();
    $(".datepicker").datepicker({format: "dd-mm-yyyy"});
});
var $rows = $('#table tr');
$('#search').keyup(function() {
    var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
    
    $rows.show().filter(function() {
        var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
        return !~text.indexOf(val);
    }).hide();
});

$('th:contains("テレワーク")').parent("tr").css("background-color", "#a1d8e6");
$('th:contains("会議")').parent("tr").css("background-color", "#f8f4e6");
$('th:contains("外出")').parent("tr").css("background-color", "#fbdac8");

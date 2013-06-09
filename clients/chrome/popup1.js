


$(function() {
    var api = 'http://directory-api.jcnrd.us/search.json';
    $.get(api, {term: 'tchen'}, function(data) {
        $('body').append(data);
    });

    $('#btn-query').on('click', function(e) {
        var term = $('#term').val().trim();
        $('.status').text(term);

        if (term) {

            $.getJSON(api, {term: term}, function(data) {
                var items = [];
                console.log(data);

                $.each(data, function(key, val) {
                    items.push('<li id="' + key + '">' + val + '</li>');
                });

                $('<ul/>', {
                    'class': 'my-new-list',
                    html: items.join('')
                }).appendTo('body');
            });
        }
    });
})
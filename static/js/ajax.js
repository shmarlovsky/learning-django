$(function() {
    $('#id_search').keyup(function() {

            $.ajax({
                    type: "POST",
                    url: "/blog/search/",
                    data: {
                        'search_text' : $('#id_search').val(),
                        'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
                    },
                    success: searchSuccess,
                    dataType: 'html'
                });
        });
});

function searchSuccess(data, textStatus, jqXHR)
{
    $('#search-results').html(data);
}
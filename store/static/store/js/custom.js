$(function() {
	$("#query").autocomplete({
		minLength: 2,
        source : function(requete, reponse){
	    $.ajax({
            url : 'https://fr.openfoodfacts.org/cgi/search.pl?search_terms={requete}&search_simple=1&action=process&json=1',
            dataType : 'json',
            data : {
                name_startsWith : $('#query').val(),
                maxRows : 15
            },

            success : function(donnee){
                reponse($.map(donnee, function(objet){
                    return objet.name;
                }));
            }
        });
        }
	});
});
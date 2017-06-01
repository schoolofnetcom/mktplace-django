$(document).ready(function () {

    $(document).on('click', '#thumbnailML', function () {

        $('#boxThumbnailML').attr('src', $(this).data('img'));

    });
});



// var algolia = algoliasearch('C2JXN1LVCW', '6476d90f1278364f33c94be177786a26');
// var categories = algolia.initIndex('category_index');
//
// categories.search('category_index', searchCallback);
//
// autocomplete("#search", {hint: false}, [
//     {
//         source: autocomplete.sources.hits(categories, {hitsPerPage: 6}),
//         templates: {
//             suggestion: function (suggestion) {
//                 console.log(suggestion);
//                 return suggestion._highlightResult.name.value;
//             }
//         }
//     }
// ]).on('autocomplete:selected', function(event, suggestion, dataset) {
//     window.location.href="/busca/?qs=" + suggestion.slug;
// });
//
//
// function searchCallback(err, content) {
//     if (err) {
//         console.error(err);
//         return;
//     }
//
//     console.log(content);
// }
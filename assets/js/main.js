$(document).ready(function () {

    $(document).on('click', '#thumbnailML', function () {

        $('#boxThumbnailML').attr('src', $(this).data('img'));

    });
});

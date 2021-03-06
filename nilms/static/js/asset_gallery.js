document.addEventListener('DOMContentLoaded', function(e) {
    var galleries = document.querySelectorAll('.asset-gallery');

    for (var i = 0; i < galleries.length; i++) {
        var items = galleries[i].querySelectorAll('.asset-gallery-item');

        for (var ii = 0; ii < items.length; ii++) {
            var item = items[ii];

            item.querySelector('.remove-btn').addEventListener('click', function(e) {
                var asset_id = this.parentNode.getAttribute('data-id');
                var _this = this;

                wget('/api/asset/delete/' + asset_id, function(data) {
                    console.log(data);

                    _this.parentNode.parentNode.removeChild(_this.parentNode);
                });
            });
        }
    }
});

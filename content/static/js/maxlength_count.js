django.jQuery(function() {
    django.jQuery('textarea[maxlength]').each(function(i, textarea) {
        var t = django.jQuery(textarea),
            count = t.parent().find('.maxlength-count')
        if (count.length == 0) {
            count = django.jQuery('<div>', {'class': 'maxlength-count'} ).insertAfter(t)
            t.on({
                keydown: update,
                change: update,
                drop: update,
            })
        }
        function update() {
            var max = Math.round(t.attr('maxlength')), left = max - t.val().length
            count.html(left + ' characters left. (max: ' + max + ')') 
        }
    });
});

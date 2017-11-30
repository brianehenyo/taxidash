(function () {

    var app = {
        isLoading: true,
        visibleCards: {},
        location: [],
        spinner: document.querySelector('.loader'),
        cardTemplate: document.querySelector('.cardTemplate'),
        container: document.querySelector('.main'),
        addDialog: document.querySelector('.dialog-container')
    };

    var selectedTrip = "";

    /*$('#butRefresh').on('click', function () {
        $.ajax({
            type: 'post',
            url: 'refreshtrips/',
            data: {
                'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
            },
            success: function (data) {
                console.log(data.trips);
                // append html to the posts div
                // $('#div').append(data.posts_html);
            },
            error: function (xhr, status, error) {
                // shit happens friends!
            }
        });
    });*/

    //Add event listener for all cards
    trip_cards = $('.card');
    trip_cards.each(function (index) {
        $(this).on("click", function () {
            selectedTrip = $(this).attr('id');
            app.toggleAddDialog(true, $(this).find(".organizer").text(), selectedTrip);
        });
    });

    document.getElementById('butCancel').addEventListener('click', function () {
        // Close the add new city dialog
        app.toggleAddDialog(false);
    });

    app.toggleAddDialog = function (visible, organizer, trip_id) {
        if (visible) {
            $(".dialog-organizer").text(organizer);
            $("#trip_id").val(trip_id);

            if (sessionStorage.getItem('taxidash_user')) {
                $("#txtPassenger").val(sessionStorage.getItem('taxidash_user'));
            }

            $('#butJoin').on('click', function () {
                // Record name as cookie
                var passenger = $("#txtPassenger").val();
                if (!sessionStorage.getItem('taxidash_user')) {
                    sessionStorage.setItem('taxidash_user', passenger);
                } else if (sessionStorage.getItem('taxidash_user') !== passenger) {
                    sessionStorage.setItem('taxidash_user', passenger);
                }

                app.toggleAddDialog(false);
            });

            app.addDialog.classList.add('dialog-container--visible');
        } else {
            app.addDialog.classList.remove('dialog-container--visible');
        }
    };

})();
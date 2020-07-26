jQuery(function($) {
        $(document).on('click', '.up-twitter-button', function ($e) {
            $e.preventDefault();

            $.get(userpress.ajax, {
                'action'		: 'twitter_ajax_login',
                '_ajax_nonce' 	: userpress.nonce
            }, function (response) {
                console.log(response);

                return false;
                /* if error. */
                if (response.error == true) {
                    /* validate user. */
                    if (response.name_null != undefined) {
                        console.log(response.name_null);
                    }
                    /* validate pass. */
                    if (response.email_null != undefined) {
                        console.log(response.email_null);
                    }
                } else {
                    location.reload();
                }
            });
        });
});
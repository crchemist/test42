function ContactViewModel() {
    var self = this;

    self.state = ko.observable('contacts');

    self.show_login_error = ko.observable(false);


    self.user_data = ko.observable();
    self.requests = ko.observable([]);

    self.requests_displayed = false;
    self.anonymous_user = ko.observable(true);
    self.is_logged_in = ko.observable(false);

    self.toggleRequestsDisplay = function() {
        if (self.requests_displayed) {
            // hide requests
            self.requests([]);
            self.requests_displayed = false
        } else {
            $.getJSON('/requests/', function(response) {
                self.requests(response.data);
                self.requests_displayed = true;
            });
        }
    }

    self.showLoginForm = function() {
        location.hash = '#/login';
    }

    $.getJSON('/contact/', function(data) {
        self.user_data(data)
        self.is_logged_in(data.is_logged_in)
        self.anonymous_user(!data.is_logged_in)
        console.log(self.anonymous_user())
    });

    // Client-side routes
    Sammy(function () {
        this.route('get', '#/', function() {
           self.state('contacts')
        });
        this.get('#/login', function() {
           self.state('login-form')
        });

        this.post('#/do-login', function(context) {
            $.ajax({
                type: 'POST',
                url: '/contact/login/',
                data: JSON.stringify({
                    'username': context.params.username,
                    'password': context.params.password}),
                contentType: 'application/json',
                dataType: 'json',
                success: function(data) {
                    location.hash = '/'
                    self.show_login_error(false)
                    if (!data.is_logged_in) {
                        self.show_login_error(true)
                    } else {
                        self.anonymous_user(!data.is_logged_in)
                    }
                },
                error: function(data) {
                    self.show_login_error(true)
                }
            })

        });
    }).run();
}

ko.applyBindings(new ContactViewModel())

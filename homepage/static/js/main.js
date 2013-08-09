function ContactViewModel() {
    var self = this;

    self.state = ko.observable('contacts');

    self.show_login_error = ko.observable(false);


    self.user_data = ko.observable();
    self.requests = ko.observable([]);

    self.requests_displayed = false;
    self.anonymous_user = ko.observable(true);

    self.authenticated_user = ko.computed(function() {
        return !self.anonymous_user();
    })

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

    self.showEditForm = function() {
        location.hash = '#/edit';
    }

    self.showEditForm = function() {
        location.hash = '#/edit';
    }

    self.makeLogout = function() {
        location.hash = '#/do-logout';
    }

    $.getJSON('/contact/', function(data) {
        self.user_data(data)
        self.anonymous_user(!data.is_logged_in)
        console.log('Anonymous user: ' + self.anonymous_user())
    });

    // Client-side routes
    Sammy(function () {
        this.route('get', '#/', function() {
           $.getJSON('/contact/', function(data) {
               self.user_data(data)
               self.anonymous_user(!data.is_logged_in)
               self.state('contacts')
           });
        });
        this.get('#/login', function() {
           self.state('login-form')
        });

        this.get('#/edit', function() {
           self.state('edit-form')
        });

        this.get('#/do-logout', function(context) {
            $.getJSON('/contact/logout', function(response) {
                context.redirect('#/');
            })
        });

        this.post('#/save-user-data', function(context) {
            console.log(context)
            $.ajax({
                type: 'POST',
                url: '/contact/update/',
                data: JSON.stringify(context.params),
                contentType: 'application/json',
                dataType: 'json',
                success: function(data) {
                    location.hash = '#/'
                },
                error: function(data) {
                }
            })

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

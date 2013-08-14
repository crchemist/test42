function ContactViewModel() {
    var self = this;

    self.state = ko.observable('contacts');

    self.show_login_error = ko.observable(false);


    self.user_data = ko.observable();
    self.requests = ko.observable([]);
    self.form_error = ko.observable(false);

    self.requests_displayed = ko.observable(false);
    self.anonymous_user = ko.observable(true);

    self.authenticated_user = ko.computed(function() {
        return !self.anonymous_user();
    })

    self.toggleRequestsDisplay = function() {
        if (self.requests_displayed()) {
            // hide requests
            self.requests([]);
            self.requests_displayed(false)
            location.hash = '#/'
        } else {
            $.getJSON('/requests/', function(response) {
                self.requests(response.data);
                location.hash = '#/requests'
            });
        }
    }

    self.showLoginForm = function() {
        location.hash = '#/login';
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
        self.requests_displayed(false)
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

        this.get('#/requests', function() {
           self.state('requests')
           self.requests_displayed(true);
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
            var fd = new FormData(document.getElementById('contact-edit'))
            $.ajax({
                url: '/contact/update/',
                type: 'POST',
                data: fd,
                contentType: false,
                processData: false,
                success: function(data) {
                    console.log(data)
                    if (data.errors) {
                        self.form_error(true);
                    } else {
                        self.form_error(false);
                        location.hash = '#/';
                    }
                },
                error: function(data) {
                    self.form_error(true);
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

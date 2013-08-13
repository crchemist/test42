function ContactViewModel() {
    var self = this;
    self.user_data = ko.observable();
    self.requests = ko.observable([]);

    self.requests_displayed = ko.observable(false);

    self.toggleRequestsDisplay = function() {
        if (self.requests_displayed()) {
            // hide requests
            self.requests([]);
            self.requests_displayed(false)
        } else {
            $.getJSON('/requests/', function(response) {
                self.requests(response.data);
                self.requests_displayed(true);
            });
        }
    }

    $.getJSON('/contact/', function(data) {
        self.user_data(data)
    });


}

ko.applyBindings(new ContactViewModel())

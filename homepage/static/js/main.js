function ContactViewModel() {
    var self = this;
    self.user_data = ko.observable();

    $.getJSON('/contact/', function(data) {
        self.user_data(data)
    });
}

ko.applyBindings(new ContactViewModel())

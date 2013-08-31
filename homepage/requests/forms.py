from django import forms


class RequestVoteForm(forms.Form):
    request_id = forms.IntegerField()
    action = forms.TypedChoiceField(coerce=int,
                                    choices=(((1, 'up'),(-1, 'down'))))

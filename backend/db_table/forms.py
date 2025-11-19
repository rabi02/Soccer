
from db_table.models import *
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# from django.contrib.auth.forms import ReadOnlyPasswordHashField


class AffiliateUserForm(forms.ModelForm):
    name = forms.CharField(label='YOUR NAME',widget=forms.TextInput(attrs={'size': '50'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'size': '50'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'size': '50'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    # name.widget.attrs.update(size='70')
    # email.widget.attrs.update(size='70')
    # phone.widget.attrs.update(size='70')
    # country.widget.attrs.update(size='70')
    password.widget.attrs.update(size='50')
    confirm_password.widget.attrs.update(size='50')

    class Meta:
        model = AffiliateUser
        fields = ["name", "email", "phone", "country", "password", "confirm_password"]

    def clean(self):
        super(AffiliateUserForm, self).clean()
        pass1 = self.cleaned_data.get("password")
        confirm_pass1 = self.cleaned_data.get("confirm_password")

        if pass1 and confirm_pass1 and pass1 != confirm_pass1:
            raise forms.ValidationError("Password don't match. Please enter again.")
        else:
            pass
    #
    # def save(self, commit=True):
    #     user = super(AffiliateUserForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data.get("password"))
    #
    #     if commit:
    #         user.save()
    #     return user


# class AffiliateChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField(label=("Password"),
#                                          help_text=("""Django does not stores password in readable form,
#                                          So you cannot see this user's password, but you can change the password
#                                          using <a href=\"../password/\">this form</a>."""))
#
#     class Meta:
#         model = AffiliateUser
#         # fields = ('email', 'password')
#
#     def clean_password(self):
#         return self.initial["password"]

class AffiliateChangeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'size': '50'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'size': '50'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    # is_active = forms.BooleanField(initial=False)
    class Meta:
        model = AffiliateUser
        fields = ["name", "email", "phone", "country"]

# RANKING_CHOICES = (
#     ("1", "Ranking 1"),
#     ("2", "Ranking 2"),
#     ("3", "Ranking 3"),
#     ("4", "Ranking 4"),
# )
# class MatchRankingForm(forms.ModelForm):
#     ranking = forms.ChoiceField(
#         label="Ranking", choices=RANKING_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
#     )
#     min_value = forms.CharField(label="min_value", widget=forms.NumberInput(attrs={"class": "form-control"}))
#     max_value = forms.CharField(label="max_value", widget=forms.NumberInput(attrs={"class": "form-control"}))
#
#     class Meta:
#         model = MatchRanking
#         fields = ["ranking", "min_value", "max_value"]


RANKING_CHOICES = (
    ("1", "Ranking 1"),
    ("2", "Ranking 2"),
    ("3", "Ranking 3"),
    ("4", "Ranking 4"),
)
class MatchRankingForm(forms.ModelForm):
    ranking = forms.CharField(
        label="Ranking",  widget=forms.TextInput(attrs={"class": "form-control"})
    )
    min_value = forms.CharField(label="min_value", widget=forms.NumberInput(attrs={"class": "form-control"}))
    max_value = forms.CharField(label="max_value", widget=forms.NumberInput(attrs={"class": "form-control"}))

    class Meta:
        model = MatchRankings
        fields = ["ranking", "min_value", "max_value"]


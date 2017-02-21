# -*- coding: utf-8 -*-
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.db.utils import OperationalError

class NewUserForm(forms.ModelForm):
    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'password', 'email',)


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('show_name',)

class SubscriptionChallengeForm(forms.ModelForm):
    # choices = forms.ChoiceField(label="Challenge",)
    class Meta:
        model = Challenge
        fields = ('id', 'title')

class LoginUserForm(forms.ModelForm):
    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password',)


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('show_name',)

class EditChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ('title', 'is_open', 'start_date', 'stop_date')


class ManageUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ManageMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('show_name', 'role')

class ManageChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ('title', 'is_open', 'start_date', 'stop_date',
                  'subs_start_date', 'subs_stop_date', 'subm_start_date',
                  'subm_stop_date')

class AddUserForm(forms.ModelForm):
    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'password', 'email',)


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('show_name', 'role')

class SubmitMovieForm(forms.ModelForm):
    file_movie = forms.FileField(label="Votre vidéo")
    class Meta:
        model = Movie
        exclude = ('challenge', 'associated_key', 'movie_url', 'published',
                   'submit_date')


class VoteNotesForm(forms.ModelForm):
    class Meta:
        model = Vote
        exclude = ('id_jury', 'id_movie', 'id_challenge', 'comment')


class VoteCommentForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('comment',)

class SubscribeChallengeForm(forms.Form):
    try:
        challenges = [(c.id, c.title) for c in Challenge.objects.filter(is_open=True)]
    except OperationalError:
        challenges = []

    list_challenge = forms.MultipleChoiceField(choices=challenges, \
                                            widget=forms.CheckboxSelectMultiple(),
                                            label="Choisissez le(s) challenge(s)")

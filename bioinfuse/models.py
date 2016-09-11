# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.dateformat import DateFormat
from django.utils.timezone import now
from django.utils.safestring import mark_safe
import markdown

notes = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10')
)

# extends table User for table Member
class Member(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    show_name = models.CharField("Nom affiché", max_length=50, null=True)
    list_role = (
        ('C', 'Concurrent'),
        ('J', 'Jury'),
        ('A', 'Admin')
    )
    role = models.CharField("Rôle", max_length=1, choices=list_role, default='C')
    associated_key = models.CharField("Clé associée", max_length=50, null=True)

    def __unicode__(self):
        return self.user.username

# table challenge
class Challenge(models.Model):
    title = models.CharField("Titre", max_length=100)
    is_open = models.BooleanField("Ouvert", default=False)
    start_date = models.DateTimeField("Date de début", default=now)
    stop_date = models.DateTimeField("Date de fin", default=now)
    subs_start_date = models.DateTimeField("Date de début d'inscription", default=now)
    subs_stop_date = models.DateTimeField("Date de fin d'inscription", default=now)
    subm_start_date = models.DateTimeField("Date de début de soumission", default=now)
    subm_stop_date = models.DateTimeField("Date de fin de soumission", default=now)

    def __unicode__(self):
        return self.title

# table AssociatedKey, will create key associated to a BioInfuse member
class AssociatedKey(models.Model):
    candidate = models.ForeignKey(Member)
    challenge = models.ForeignKey(Challenge)
    associated_key = models.CharField("Clé d'association", max_length=50)

    def __unicode__(self):
        return self.associated_key

# table Movie
class Movie(models.Model):
    challenge = models.ForeignKey(Challenge)
    associated_key = models.OneToOneField(AssociatedKey, unique=True)
    title = models.CharField("Titre", max_length=120,
                             help_text="Ce titre sera aussi utilisé sur "
                                       "notre compte DailyMotion")
    movie_url = models.URLField("Lien vers la vidéo", max_length=200, null=True)
    description = models.TextField("Description",
                                   help_text="Cette description sera aussi "
                                             "utilisée sur notre compte "
                                             "DailyMotion")
    submit_date = models.DateTimeField("Date de soumission",
                                       help_text="La date doit être insérée "
                                                 "sous forme jj/mm/aaaa "
                                                 "hh:mm:ss",
                                       default=now)
    published = models.BooleanField("Publié", default=False)

    def __unicode__(self):
        return self.title

# table Article
class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User)
    content = models.TextField()
    creation_date = models.DateTimeField()
    edit_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def content_markdown(self):
        return mark_safe(markdown.markdown(self.content))

# table Page
class Page(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User)
    content = models.TextField()
    published = models.BooleanField(default=False)
    creation_date = models.DateTimeField(default=now)
    edit_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def content_markdown(self):
        return mark_safe(markdown.markdown(self.content))



class Vote(models.Model):
    id_movie = models.ForeignKey(Movie)
    id_jury = models.ForeignKey(Member)
    id_challenge = models.ForeignKey(Challenge)
    global_note = models.CharField("Globale", max_length=2, choices=notes, default='0')
    artistic_note = models.CharField("Artistique", max_length=2, choices=notes, default='0')
    originality_note = models.CharField("Originalité du sujet", max_length=2, choices=notes, default='0')
    investment_note = models.CharField("Moyens investis", max_length=2, choices=notes, default='0')
    take_home_message_note = models.CharField("Take-home message", max_length=2, choices=notes, default='0')
    understandable_note = models.CharField("Compréhensible par la cible", max_length=2, choices=notes, default='0')
    scientific_note = models.CharField("Scientifique", max_length=2, choices=notes, default='0')
    captive_interest_note = models.CharField("Captive l'intérêt", max_length=2, choices=notes, default='0')
    rigorous_note = models.CharField("Rigueur scientifique", max_length=2, choices=notes, default='0')
    comment = models.TextField("Votre commentaire :")

    def __unicode__(self):
        return self.id_jury

    def comment_markdown(self):
        return mark_safe(markdown.markdown(self.comment))

#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
File to test how to upload a movie into Dailymotion, not used by BioInfuse app
"""
import os
import sys
sys.path.append(os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'jebif.settings'
import django
django.setup()
from bioinfuse.models import Movie
from parameters import *
import dailymotion
import argparse

parser = argparse.ArgumentParser(description="Take uploaded movie in the "
                                             "server and upload it into "
                                             "Dailymotion.")
parser.add_argument('-m', '--movie', required=True,
                    help="Movie file to upload on Dailymotion")
parser.add_argument('-i', '--id', required=True,
                    help="Movie id on our database to use in Dailymotion "
                         "request.")
args = vars(parser.parse_args())

movie = args['movie']
id_movie = args['id']

print(movie, id_movie)

d = dailymotion.Dailymotion()
d.set_grant_type('password', api_key=API_KEY,
                 api_secret=API_SECRET, scope=['manage_videos'],
                 info={'username': USERNAME, 'password': PASSWORD})

q_movie = Movie.objects.get(id=id_movie)
url = d.upload(movie)
movie = d.post('/me/videos',
               {'url': url, 'title': q_movie.title,
                'published': 'true', 'channel': 'tech',
                'private': 'true',
                'description': q_movie.description})
print(movie)
list = d.get('/videos', {'fields': 'user,id,title, url,', 'owner': owner, 'private': 1})['list']
for l in list:
    if l['id'] == movie['id']:
        url = d.get('/video/' + l['id'], {'fields': 'title,description,url'})['url']
        print(url)
        q_movie.movie_url = url
        q_movie.save()
        print("Champ Movie mis à jour pour la vidéo %d" % q_movie.id)

print("Vidéo uploadée")

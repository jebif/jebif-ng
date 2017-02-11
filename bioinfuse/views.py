# -*- coding: utf-8 -*-
from django import get_version
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from bioinfuse.models import *
from bioinfuse.forms import *
import datetime
import dailymotion
from bioinfuse.parameters import *
import re
from django.db.utils import OperationalError

def generate_key(length):
    """
        Returns random key for BioInfuse member in challenge

        length - length of the random key

        Used in subscribe() and subscribe_challenge()
    """
    import random
    return "".join([random.choice("abcdefghijklmnopqrstuvwxyz012"
                                "3456789!@#$%^&*(-_=+)")
                    for i in range(length)])

def base(request):
    """
        Define common variables to use in HTML views

        request - html page requested *.html
    """
    try:
        total_member = Member.objects.count()
        total_challenger = Member.objects.filter(role='C').count()
        total_jury = Member.objects.filter(role='J').count()
        total_admin = Member.objects.filter(role='A').count()
        total_movie = Movie.objects.count()
        pages = Page.objects.filter(published=True).order_by('title')
        challenge = Challenge.objects.filter(is_open=True).order_by('stop_date')
    except OperationalError:
        total_member = 0
        total_challenger = 0
        total_jury = 0
        total_admin = 0
        total_movie = 0
        pages = None
        challenge = []
    context = {
        'version': get_version(),
        'total_member': total_member,
        'total_challenger': total_challenger,
        'total_jury': total_jury,
        'total_admin': total_admin,
        'total_movie': total_movie,
        'pages': pages,
    }
    if request.user.id != None:
        member_id = request.user.id
        context['member'] = Member.objects.get(user=member_id)
    if len(challenge) > 0:
        challenge = challenge[0]
        context['challenge'] = challenge
        today = datetime.datetime.now().strftime('%s')
        context['today'] = today
        subm_start = challenge.subm_start_date.strftime('%s')
        subm_stop = challenge.subm_stop_date.strftime('%s')
        context['subm_start'] = subm_start
        context['subm_stop'] = subm_stop
        if today > subm_start and today < subm_stop:
            context['submit_ok'] = True
        else:
            context['submit_ok'] = False
    else:
        context['challenge.is_open'] = False
        context['submit_ok'] = False
    return context

def home(request):
    """
        Nothing yet on a/, redirection to a/bioinfuse

        request - redirect from a/ to a/bioinfuse
    """
    return HttpResponseRedirect(reverse('bioinfuse:index'))

def index(request):
    """
        Show BioInfuse home page

        request - html page requested home.html
    """
    context = base(request)
    return render(request, "home.html", context)

def subscribe(request):
    """
        Subscription for new BioInfuse member

        request - html page requested subscribe.html
    """
    registered = False
    context = base(request)
    try:
        challenge = Challenge.objects.filter(is_open=True).order_by('stop_date')[0]
    except OperationalError:
        challenge = []
    if request.method == 'GET':
        user_form = NewUserForm()
        subs_form = SubscriptionForm()
    else:
        user_form = NewUserForm(request.POST)
        subs_form = SubscriptionForm(request.POST)

        if user_form.is_valid() and subs_form.is_valid():
            # register new user
            user = user_form.save()
            user.set_password(user.password)  # use set_password to hash enter password
            user_member = user.id
            user.save()
            show_name = subs_form.cleaned_data['show_name']
            # register new member
            member = subs_form.save(commit=False)
            member.user = user
            member.save()
            # generate associated key for new member
            key = generate_key(50)
            member_key = AssociatedKey.objects.create(candidate=member,
                                                      challenge=challenge,
                                                      associated_key=key)
            member_key.save()
            member = Member.objects.get(user=user_member)
            member.associated_key = member_key.associated_key
            member.save()
            registered = True
            context['show_name'] = show_name

    context['user_form'] = user_form
    context['subs_form'] = subs_form
    context['registered'] = registered

    return render(request, "subscribe.html", context)


def login(request):
    """
        Login page

        request - html page requested registration/login.html
    """
    context = base(request)
    if request.method == 'GET':
        user_form = LoginUserForm()
    else:
        user_form = LoginUserForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data["username"]
            password = user_form.cleaned_data["password"]
            user = authenticate(username=username,
                                password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('bioinfuse:index'))
                else:
                    context['error_msg'] = "Le compte n'est pas actif."
            else:
                context['error_msg'] = "Le compte n'existe pas."

    context['user_form'] = user_form

    return render(request, "registration/login.html", context)

def edit_profile(request, member):
    """
        Where BioInfuse member can change profile

        request - html page requested edit_profile.html
        member  - BioInfuse Member id

        ToDo - Allow BioInfuse to change password and delete account
    """
    context = base(request)
    get_member = Member.objects.get(user=member)
    get_user = User.objects.get(id=member)
    if request.method == 'GET':
        user_form = EditUserForm({'first_name': get_user.first_name,
                             'last_name': get_user.last_name,
                             'email': get_user.email})
        member_form = EditProfileForm({'show_name': get_member.show_name})
    else:
        user_form = EditUserForm(request.POST)
        member_form = EditProfileForm(request.POST)

        if user_form.is_valid() and member_form.is_valid():
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            email = user_form.cleaned_data['email']
            show_name = member_form.cleaned_data['show_name']
            # update page
            get_user.first_name = first_name
            get_user.last_name = last_name
            get_user.email = email
            get_user.save()
            get_member.show_name = show_name
            get_member.save()
            return HttpResponseRedirect(reverse('bioinfuse:index'))
    context['profile_id'] = get_member.user.id
    context['user_form'] = user_form
    context['member_form'] = member_form
    return render(request, "edit_profile.html", context)

def subscribe_challenge(request, member):
    """
        Where existing BioInfuse member can subscribe to a new challenge

        request - html page requested subscribe_challenge.html
        member  - BioInfuse Member id
    """
    context = base(request)
    member = Member.objects.get(user=member)
    try:
        challenges = Challenge.objects.filter(is_open=True)
    except OperationalError:
        challenges = []
    if request.method == 'GET' and len(challenges) > 0:
        # context['challenges'] = challenges
        challenge_form = SubscribeChallengeForm()
        print(challenge_form)
    else:
        challenge_form = SubscribeChallengeForm(request.POST)
        challenges = request.POST
        list_challenge = challenges.getlist("list_challenge")
        # from list_challenge, add user on each challenge
        for c in list_challenge:
            challenge = Challenge.objects.get(id=c)
            # only subscribe member if AssociatedKey not exists for the selected
            # challenge
            if len(AssociatedKey.objects.filter(candidate=member,
                                             challenge=challenge)) == 0:
                key = generate_key(50)
                member_key = AssociatedKey.objects.create(candidate=member,
                                                            challenge=challenge,
                                                            associated_key=key)
                member_key.save()
                member.associated_key = member_key.associated_key
                member.save()
        # once form is submitted, redirect member to index
        return HttpResponseRedirect(reverse('bioinfuse:index'))

    context['challenge_form'] = challenge_form
    context['role'] = member.role
    return render(request, "subscribe_challenge.html", context)

def list_members(request):
    """
        Show all BioInfuse members in adminstration panel

        request - html page requested manage_members.html
    """
    context = base(request)
    members = Member.objects.all()
    if request.user.id:
        role = Member.objects.get(user=request.user.id).role
    else:
        role = 'I'
    context['members'] = members
    context['role'] = role
    return render(request, "manage_members.html", context)

def edit_member(request, member):
    """
        Where BioInfuse member (role 'A') can change BioInfuse member data,
        like 'role'

        request - html page requested edit_member.html
        member  - BioInfuse Member id
    """
    context = base(request)
    get_member = Member.objects.get(user=member)
    changed_member = get_member
    get_user = User.objects.get(id=member)
    if request.user.id:
        role = Member.objects.get(user=request.user.id).role
    else:
        role = 'I'
    if request.method == 'GET':
        user_form = ManageUserForm({'first_name': get_user.first_name,
                                  'last_name': get_user.last_name,
                                  'email': get_user.email})
        member_form = ManageMemberForm({'show_name': get_member.show_name,
                                       'role': get_member.role})
    else:
        user_form = ManageUserForm(request.POST)
        member_form = ManageMemberForm(request.POST)

        if user_form.is_valid() and member_form.is_valid():
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            email = user_form.cleaned_data['email']
            show_name = member_form.cleaned_data['show_name']
            member_role = member_form.cleaned_data['role']
            # update page
            get_user.first_name = first_name
            get_user.last_name = last_name
            get_user.email = email
            get_user.save()
            get_member.show_name = show_name
            get_member.role = member_role
            get_member.save()
            return HttpResponseRedirect(reverse('bioinfuse:manage_members'))
    context['role'] = role
    context['changed_member'] = changed_member
    context['user_form'] = user_form
    context['member_form'] = member_form
    return render(request, "edit_member.html", context)

# HTML page to submit a movie
# Add a visual like a file uploading image?
def submit_movie(request, member):
    """
        Where BioInfuse member (role 'C') send a movie.

        request - html page requested submit_movie.html
        member  - BioInfuse Member id
    """
    def upload_movie(movie_id, file_name):
        """
            Use Dailymotion API to send a movie.

            movie_id  - BioInfuse Movie id
            file_name - file path to the submitted movie file, temporary
        """
        d = dailymotion.Dailymotion()
        d.set_grant_type('password', api_key=API_KEY,
                         api_secret=API_SECRET, scope=['manage_videos'],
                         info={'username': USERNAME, 'password': PASSWORD})
        q_movie = Movie.objects.get(id=movie_id)
        url = d.upload(file_name)
        movie = d.post('/me/videos',
                       {'url': url, 'title': q_movie.title,
                        'published': 'true', 'channel': 'tech',
                        'private': 'true',
                        'description': q_movie.description})
        """
        WARNING: the below part is wrong. The actual URL stored in DB is not in
                 an embedding format! Need to retrieve the embed_url field from
                 Dailymotion
        """
        q_movie.movie_url = 'http://www.dailymotion.com/video/' + \
                            str(movie['id'])
        q_movie.save()

    context = base(request)
    try:
        role = Member.objects.get(user=member).role
        member = Member.objects.get(user=member)
        challenge = Challenge.objects.filter(is_open=True).order_by('stop_date')[0]
    except OperationalError:
        role = ""
        member = None
        challenge = []
    is_submit = False
    if request.method == 'GET':
        submit_movie_form = SubmitMovieForm({'submit_date': now()})
    else:
        submit_movie_form = SubmitMovieForm(request.POST, request.FILES)

        if submit_movie_form.is_valid():
            title = submit_movie_form.cleaned_data['title']
            description = submit_movie_form.cleaned_data['description']
            file_movie = request.FILES['file_movie']
            sub_date = now() # don't remove it, necessary in submit_date fields!
            name = file_movie.temporary_file_path()
            associated_key = AssociatedKey.objects.get(
                associated_key=member.associated_key)
            register_movie = Movie.objects.create(challenge=challenge,
                                                  associated_key=associated_key,
                                                  title=title,
                                                  description=description,
                                                  submit_date=sub_date)
            register_movie.save()
            m_id = Movie.objects.get(challenge=challenge,
                                     associated_key=associated_key,
                                     submit_date=sub_date).id
            upload_movie(m_id, name)
            is_submit = True

    context['submit_movie_form'] = submit_movie_form
    context['role'] = role
    context['is_submit'] = is_submit
    return render(request, "submit_movie.html", context)

# HTML page to show, pages are created in Django admin
def show_page(request, page):
    """
        Show page created by Django admin, like Rules

        request - html page requested show_page.html
        page    - BioInfuse Page id
    """
    context = base(request)
    try:
        page = Page.objects.get(id=page)
    except:
        page = {}
    context['page'] = page

    return render(request, "show_page.html", context)

# HTML page to list all movies submitted in BioInfuse app
def list_movies(request):
    """
        Show all movies on administration panel

        request - html page requested manage_notes.html
    """
    context = base(request)
    movies = Movie.objects.all()
    context['movies'] = movies
    if request.user.id:
        role = Member.objects.get(user=request.user.id).role
    else:
        role = 'I'
    for i in range(0, len(movies)):
        if Vote.objects.filter(id_movie=movies[i].id):
            evaluation = Vote.objects.get(id_movie=movies[i].id, \
                                          user=request.user.id)
            movies[i].note = int(evaluation.global_note)
            movies[i].note += int(evaluation.artistic_note)
            movies[i].note += int(evaluation.originality_note)
            movies[i].note += int(evaluation.investment_note)
            movies[i].note += int(evaluation.take_home_message_note)
            movies[i].note += int(evaluation.understandable_note)
            movies[i].note += int(evaluation.scientific_note)
            movies[i].note += int(evaluation.captive_interest_note)
            movies[i].note += int(evaluation.rigorous_note)
            movies[i].comment = evaluation.comment
        else:
            movies[i].note = '-'
            movies[i].comment = '-'
    context['role'] = role
    return render(request, "manage_notes.html", context)

# HTML page for Jury when a movie need to be evaluated
def add_notes(request, movie_id):
    """
        Where a BioInfuse Member (role 'J') can evaluate a BioInfuse Movie

        request  - html page requested add_notes.html
        movie_id - BioInfuse Movie id
    """
    context = base(request)
    context['movie_id'] = movie_id
    movie = Movie.objects.get(id=movie_id)
    #challenge = Challenge.objects.get(movie=movie)
    """
    WARNING: the below part is a fix. The actual URL stored in DB is not in
             an embedding format! Miss embed/ before video/
    """
    d = dailymotion.Dailymotion()
    d.set_grant_type('password', api_key=API_KEY,
                     api_secret=API_SECRET, scope=['manage_videos'],
                     info={'username': USERNAME, 'password': PASSWORD})
    daily_id = re.sub(r'http:\/\/www.dailymotion.com\/video\/', '', movie.movie_url)
    movie_url = d.get('/video/' + daily_id, {'fields': 'embed_url'})['embed_url']
    if request.user.id:
        role = Member.objects.get(user=request.user.id).role
    else:
        role = 'I'
    if request.method == 'GET':
        try:
            votes = Vote.objects.get(id_movie=movie_id)
            notes_form = VoteNotesForm({'global_note': votes.global_note,
                                        'artistic_note': votes.artistic_note,
                                        'originality_note': votes.originality_note,
                                        'investment_note': votes.investment_note,
                                        'take_home_message_note': votes.take_home_message_note,
                                        'understandable_note': votes.understandable_note,
                                        'scientific_note': votes.scientific_note,
                                        'captive_interest_note': votes.captive_interest_note,
                                        'rigorous_note': votes.rigorous_note})
            comment_form = VoteCommentForm({'comment': votes.comment})
        except:
            notes_form = VoteNotesForm()
            comment_form = VoteCommentForm()
    else:
        notes_form = VoteNotesForm(request.POST)
        comment_form = VoteCommentForm(request.POST)
        if notes_form.is_valid() and comment_form.is_valid() and role == 'J':
            membre = Member.objects.get(user=request.user.id)
            comment = comment_form.cleaned_data['comment']
            global_note = notes_form.cleaned_data['global_note']
            artistic = notes_form.cleaned_data['artistic_note']
            originality = notes_form.cleaned_data['originality_note']
            investment = notes_form.cleaned_data['investment_note']
            take_home_message = notes_form.cleaned_data['take_home_message_note']
            understandable = notes_form.cleaned_data['understandable_note']
            scientific = notes_form.cleaned_data['scientific_note']
            captive = notes_form.cleaned_data['captive_interest_note']
            rigorous = notes_form.cleaned_data['rigorous_note']
            submit_notes = Vote.objects.create(id_jury=membre,
                                               id_challenge=movie.challenge,
                                               id_movie=movie,
                                               global_note=global_note,
                                               artistic_note=artistic,
                                               originality_note=originality,
                                               investment_note=investment,
                                               take_home_message_note=take_home_message,
                                               understandable_note=understandable,
                                               scientific_note=scientific,
                                               captive_interest_note=captive,
                                               rigorous_note=rigorous,
                                               comment=comment)
            submit_notes.save()

            return HttpResponseRedirect(reverse('bioinfuse:manage_notes'))

    context['role'] = role
    context['movie_url'] = movie_url
    context['movie_desc'] = movie.description
    context['notes_form'] = notes_form
    context['comment_form'] = comment_form
    return render(request, "add_notes.html", context)

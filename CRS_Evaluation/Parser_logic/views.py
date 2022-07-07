import os
from urllib import parse as urlparse
import pandas as pd
import string
import traceback
import random
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from Parser_logic.Dialogue_Parsing import Dialogue_Parsing
from Parser_logic.decorators import timer
from django.utils.datastructures import MultiValueDictKeyError
from CRS_Evaluation.firebase_sdk import firebase_sdk
from CRS_Evaluation.settings import TOTAL_FRAGMENTS
import firebase_admin
from firebase_admin import db
import time
import requests

"""
Variables declaration
"""
R1 = ""
R2 = ""
R3 = ""
H1 = ""
H2 = ""
H3 = ""

START_TIME = 0
END_TIME = 0
FRAGMENT_No= 0
OBJ_DIALOG_PARSER  = None
dialogue_to_show = None
QUESTIONAIRE_TIME_START = 0
TOTAL_STUDY_TIME_START = 0
TOTAL_FEDBACK_TIME_START = 0
DIALOG_ID = 0

"""
view for index.html page
"""
@timer
def home(request):
    try:
        request.session['total_study_time'] = time.time()
        request.session['home_page_start_time'] = time.time()
        request.session['RANDOM_NUMBER'] = random.randint(3, 8)
        print('i am at home....')
        session = requests.Session()
        url =  request.GET
        if len(url) > 0 :
            token = url['q']
            request.session['group'] = token
            print(token)
        else:
            request.session['group'] = 'Null'

        return render(request, "index.html", {"results": {}})

    except Exception as excError:
            return render(request, "error.html", {"error": excError})


"""
view for error.html page
"""
def error(request):
    return render(request, "error.html", {})


"""
view for rating.html page, where 10 dialogs situations are shown
"""
@timer
def ratings(request):
    try:
        if request.method == 'POST':
            form_data= {}
            if 'rating1' in request.POST:
                temp_list = ['o','d','k']
                # collecting user inputs shown in a dialog situation
                index1 = temp_list.index(request.POST.get('h1', ''))+1
                form_data['rating'+str(index1)] =  request.POST.get('rating1', 0)
                form_data['response'+str(index1)] = request.POST.get('response1', '')

                index2 = temp_list.index(request.POST.get('h2', ''))+1
                form_data['rating'+str(index2)] = request.POST.get('rating2', 0)
                form_data['response'+str(index2)] = request.POST.get('response2', '')

                index3 = temp_list.index(request.POST.get('h3', ''))+1
                form_data['rating'+str(index3)] = request.POST.get('rating3', 0)
                form_data['response'+str(index3)] = request.POST.get('response3', '')

               #fetching a data for the next dialog situation
                global OBJ_DIALOG_PARSER
                if OBJ_DIALOG_PARSER is not None:
                    form_data['frag_num'] = request.session['FRAGMENT_No']
                    form_data['dialog_ID'] = request.session['DIALOG_ID']
                    form_data['cookie_value'] = request.COOKIES['csrftoken']
                    request.session['END_TIME'] = time.time()
                    form_data['duration'] = request.session['END_TIME'] - request.session['START_TIME']
                    form_data['fragment'] = request.session['dialogue_frament']
                    save_data(form_data)
                    print( 'the randome number is ' + str(request.session['RANDOM_NUMBER']))
                    if int(request.session['FRAGMENT_No']) == request.session['RANDOM_NUMBER']:
                        request = display_rating_page_attention_check(request)
                        return render(request, "ratings.html", {"dlg_fragment": request.session['dialogue_frament'], "response1": request.session['r1'], 'h1':request.session['h1'],"response2":request.session['r2'], 'h2':request.session['h2'],"response3":request.session['r3'], 'h3':request.session['h3'], 'fgnum':request.session['FRAGMENT_No']})
                    if request.session['FRAGMENT_No'] >= TOTAL_FRAGMENTS:
                        request.session['FRAGMENT_No'] = 0
                        return redirect("questionnaire.html", {"results": {}})
                    request = display_rating_page(request)
                    return render(request, "ratings.html", {"dlg_fragment": request.session['dialogue_frament'], "response1": request.session['r1'], 'h1':request.session['h1'],"response2":request.session['r2'], 'h2':request.session['h2'],"response3":request.session['r3'], 'h3':request.session['h3'], 'fgnum':request.session['FRAGMENT_No']})
                else:
                    request = display_rating_page(request)
                    return render(request, "ratings.html", {"dlg_fragment": request.session['dialogue_frament'], "response1": request.session['r1'], 'h1':request.session['h1'],"response2":request.session['r2'], 'h2':request.session['h2'],"response3":request.session['r3'], 'h3':request.session['h3'], 'fgnum':request.session['FRAGMENT_No']})
            #show rating page for the first dialog situation
            elif request.POST.get('readit', 1):
                request = display_rating_page(request,fragment_no =0)
                return render(request, "ratings.html", {"dlg_fragment": request.session['dialogue_frament'], "response1": request.session['r1'], 'h1':request.session['h1'],"response2":request.session['r2'], 'h2':request.session['h2'],"response3":request.session['r3'], 'h3':request.session['h3'], 'fgnum':request.session['FRAGMENT_No']})
    except Exception:
            traceback.print_exc()
            return render(request, "error.html", {})

"""
A function to retrieve and compute dialog situation (fragment) and corresponding responses.
The dialog situation, and the corresponding responses by three different systems then will be shown on ratings.html
"""
def display_rating_page(request,fragment_no = None):
    if fragment_no == 0:
        request.session['FRAGMENT_No'] = 0
        request.session['home_page_end_time'] = time.time()
    global OBJ_DIALOG_PARSER
    if OBJ_DIALOG_PARSER == None:
        OBJ_DIALOG_PARSER = Dialogue_Parsing()
    request.session['dialogue_to_show'], request.session['DIALOG_ID'] = OBJ_DIALOG_PARSER.show_fragment(request)
    request.session['our_sentence'] = OBJ_DIALOG_PARSER.show_our_sentence(request.session['dialogue_to_show'])
    request.session['deep_crs_sentence'] = OBJ_DIALOG_PARSER.show_deep_crs_sentence(request.session['dialogue_to_show'])
    request.session['kbrd_sentence'] = OBJ_DIALOG_PARSER.show_kbrd_sentence(request.session['dialogue_to_show'])
    request.session['SENTENCE_LIST'] = []
    request.session['SENTENCE_LIST'].append(request.session['our_sentence'] + '$o')
    request.session['SENTENCE_LIST'].append(request.session['deep_crs_sentence'] + '$d')
    request.session['SENTENCE_LIST'].append(request.session['kbrd_sentence'] + '$k')
    request = randomise_sentences(request)
    request.session['dialogue_frament'] = request.session['dialogue_to_show'][1:len(request.session['dialogue_to_show'])]
    request.session['FRAGMENT_No'] = request.session['FRAGMENT_No'] + 1
    request.session['START_TIME'] = time.time()
    return request


"""
A function to display the attention check between thrid and 8th number, randomly computed.
This attention check is hardcoded and can be modified independent of the evaluated system responses.
"""
def display_rating_page_attention_check(request,fragment_no = None):
    if fragment_no == 0:
        request.session['FRAGMENT_No'] = 0
        request.session['home_page_end_time'] = time.time()
    global OBJ_DIALOG_PARSER
    if OBJ_DIALOG_PARSER == None:
        OBJ_DIALOG_PARSER = Dialogue_Parsing()
    request.session['dialogue_to_show'], request.session['DIALOG_ID'] = OBJ_DIALOG_PARSER.show_fragment_attention_check(request)
    print(" this is an attention check trial" + str(request.session['FRAGMENT_No']))
    request.session['our_sentence'] = 'I am reading this carefully, and I give a rating of "Meaningless" to all three responses here, "The Godfather (1972)"'
    request.session['deep_crs_sentence'] = 'What kind of movies are you looking for?'
    request.session['kbrd_sentence'] = 'I would recommend "Hangover (2010)"'
    # print(deep_crs_sentence)
    request.session['SENTENCE_LIST'] = []
    request.session['SENTENCE_LIST'].append(request.session['our_sentence'] + '$o')
    request.session['SENTENCE_LIST'].append(request.session['deep_crs_sentence'] + '$d')
    request.session['SENTENCE_LIST'].append(request.session['kbrd_sentence'] + '$k')
    request = randomise_sentences(request)
    request.session['dialogue_frament'] = request.session['dialogue_to_show'][1:len(request.session['dialogue_to_show'])]
    request.session['FRAGMENT_No'] = request.session['FRAGMENT_No'] + 1
    request.session['START_TIME'] = time.time()
    return request


"""
Function to randomize the position of the three responses shown on the rating page.
"""
def randomise_sentences(request):
    index_list = []
    n = random.randint(0, len(request.session['SENTENCE_LIST']) - 1)
    request.session['r1'],request.session['h1'] = request.session['SENTENCE_LIST'][n].split('$')
    index_list.append(n)
    while len(index_list) < 3:
        n1 = random.randint(0, 2)
        if n1 not in index_list:
            request.session['r2'],request.session['h2'] = request.session['SENTENCE_LIST'][n1].split('$')
            index_list.append(n1)
            n2 = int(3 - (n +n1))
            request.session['r3'],request.session['h3'] = request.session['SENTENCE_LIST'][n2].split('$')
            break
        else:
            continue
    return request


"""
A view page to show and collect the user inputs for the demographic features of the participants.
"""
@timer
def question(request):
    try:
        if request.method == 'POST':
            questionair_data={}
            if 'gender' in request.POST:
                questionair_data['gender'] = request.POST.get('gender','')
                questionair_data['age'] = request.POST.get('age','')
                questionair_data['movies_watched'] = request.POST.get('movies_watched','')
                questionair_data['english_level'] = request.POST.get('english_level','')
                questionair_data['education_level'] = request.POST.get('education_level','')
                questionair_data['userId'] = request.COOKIES['csrftoken']
                questionair_data['movie_crs'] = request.POST.get('movie_crs','')
                questionair_data['other_domain_crs'] = request.POST.get('other_domain_crs','')
                end_time = time.time()
                total_questionaire_time = end_time - request.session['questionaire_start_time']
                questionair_data['questionaire_time'] = total_questionaire_time
                save_questionair_data(questionair_data)

                global TOTAL_FEDBACK_TIME_START
                TOTAL_FEDBACK_TIME_START = time.time()
                return redirect("feedback.html", {"results": {}})
        request.session['questionaire_start_time'] = time.time()
        return render(request,"questionnaire.html", {"results": {}})
    except Exception:
        traceback.print_exc()
        return redirect("error.html", {})

"""
A view function to show and collect the user inputs on the feedback page shown after demographic page.
"""
@timer
def feedback(request):
    try:
        if request.method == 'POST':
            questionair_data={}
            if 'dlg_initiation' in request.POST:
                questionair_data['dlg_initiation'] = request.POST.get('dlg_initiation','')
                questionair_data['dlg_realistic'] = request.POST.get('dlg_realistic','')
                questionair_data['dlg_humans'] = request.POST.get('dlg_humans','')
                questionair_data['chatbot_useful'] = request.POST.get('chatbot_useful','')
                questionair_data['attention_hit'] = request.POST.get('attention_hit','')
                questionair_data['crs_usuage'] = request.POST.get('crs_usuage','')
                questionair_data['userId'] = request.COOKIES['csrftoken']
                questionair_data['remarks'] = request.POST.get('remarks','')
                questionair_data['group'] = request.session['group']
                questionair_data['home_page_time'] = request.session['home_page_end_time']- request.session['home_page_start_time']
                end_time = time.time()
                Total_feedback_time = end_time - request.session['feedback_start_time']
                Total_study_time = end_time - request.session['total_study_time']
                questionair_data['Total_Study_Time'] = Total_study_time
                questionair_data['Feedback_time'] = Total_feedback_time
                hit_code = show_hitcode()
                questionair_data['hitcode'] = hit_code
                save_feedback_data(questionair_data)
                return render(request,"confirmation.html", {"hitcode": hit_code})
        request.session['feedback_start_time'] = time.time()
        return render(request,"feedback.html", {"results": {}})
    except Exception:
        traceback.print_exc()
        return redirect("error.html", {})

"""
A view page to show the data collection policy, informed consent including terms and conditions, etc.
This link to this page is shown in the very first page (index.html), where instructions for conducting the study are mentioned. 
"""
@timer
def terms(request):
    try:
        return render(request,"terms.html", {"results": {}})
    except Exception:
        traceback.print_exc()
        return redirect("error.html", {})


## A function to compute and show the unique hit code and is shown when the user has completed the study successfully.
def show_hitcode():
    # generating random strings
    N = 6
    code = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
    return str(code)

"""
A view page that mentions the greeting message and hit code after the successful completion of the study.
In case of crowedsource based studies, participants can use this hit code to get their credits.
"""
@timer
def confirmation(request):
    try:
        if 'hitcode' in request.POST:
            return redirect("index.html", {"results": {}})
        else:
            return redirect(request,"index.html", {"results": {}})
    except Exception:
        traceback.print_exc()
        return redirect("error.html", {})

"""
A view page to show the error message in case of anything goes wrong during the study.
"""
@timer
def error(request):
    return render(request, "error.html", {})


"""
Methods to set the cookies for unique users.
"""

def setcookie(request):
    cookieid = str(randomString(10))
    response = HttpResponse("Cookie Set")
    response.set_cookie('CRS_study_user', cookieid)
    return response


def getcookie(request):
    cookie  = request.COOKIES['CRS_study_user']
    return HttpResponse("The user is @: "+  cookie);


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


"""
A method to store the ratings, responses, dialog situation, etc. into the database provided by the participants.
"""
def save_data(data_dict):
    if data_dict:
        rate1 = data_dict['rating1']
        rate2 = data_dict['rating2']
        rate3 = data_dict['rating3']
        response1 = data_dict['response1']
        response2 = data_dict['response2']
        response3 = data_dict['response3']
        user_id = data_dict['cookie_value']
        time = data_dict['duration']
        fragment = data_dict['fragment']
        dialog_ID  = data_dict['dialog_ID']

        frag_num = data_dict['frag_num']

        firebase_admin = firebase_sdk()
        ref = db.reference('CRS_Study/'+user_id+'/'+ str(frag_num) +'/')
        ref.set({
                        'Our_response':response1,
                        'Deep_crs_response':response2,
                        'Kbrd_response':response3,
                        'Our_rating':rate1,
                        'Deep_crs_rating':rate2,
                        'Kbrd_rating':rate3,
                        'Time':time,
                        'Dialog_ID':dialog_ID,
                        'Fragment':fragment
        })



"""
A method to store the demographic data provided by the participants regarding the questionnaire page into the database.
"""
def save_questionair_data(data_dict):
    if data_dict:
        gender = data_dict['gender']
        age = data_dict['age']
        movies_watched = data_dict['movies_watched']
        english_level = data_dict['english_level']
        education_level = data_dict['education_level']
        movie_crs = data_dict['movie_crs']
        other_domain_crs = data_dict['other_domain_crs']
        user_id = data_dict['userId']
        questionaire_time = data_dict['questionaire_time']
        print('printing demographic data into databse......')

        firebase_admin = firebase_sdk()
        ref = db.reference('CRS_Study/'+user_id+'/'+ str('Questionnaire') +'/' +str('Demographic'))
        ref.set({
                        'Gender':gender,
                        'Age':age,
                        'Movies_watched':movies_watched,
                        'English_level':english_level,
                        'Education_level':education_level,
                        'Movie_crs': movie_crs,
                        'Other_domain_crs': other_domain_crs,
                        'Total_questionaire_time':questionaire_time,
        })

        print('data saved..............######')
    else:
        print('data not saved..............######')

"""
A method to store the input data provided by the participants regarding the feedback page into the database.
"""
def save_feedback_data(data_dict):
    if data_dict:
        dlg_initiation = data_dict['dlg_initiation']
        dlg_realistic = data_dict['dlg_realistic']
        dlg_humans = data_dict['dlg_humans']
        chatbot_useful = data_dict['chatbot_useful']
        crs_usuage = data_dict['crs_usuage']
        remarks = data_dict['remarks']
        user_id = data_dict['userId']
        study_time = data_dict['Total_Study_Time']
        feedback_time = data_dict['Feedback_time']
        home_page_time = data_dict['home_page_time']
        attention_hit = data_dict['attention_hit']
        hitcode = data_dict['hitcode']
        group = data_dict['group']
        print('printing feedback data into databse......')

        firebase_admin = firebase_sdk()
        ref = db.reference('CRS_Study/'+user_id+'/'+ str('Questionnaire') +'/' +str('Feedback'))
        ref.set({
                        'Dlg_initiation':dlg_initiation,
                        'Dlg_realistic':dlg_realistic,
                        'Remarks':remarks,
                        'Home_page_time':home_page_time,
                        'Attention_hit':attention_hit,
                        'Hitcode':hitcode,
                        'Chatbot_useful':chatbot_useful,
                        'Crs_usuage':crs_usuage,
                        'Dlg_humans': dlg_humans,
                        'Total_study_time' :study_time,
                        'Total_feedback_time':feedback_time,
                        'Group' : group
        })

        print('data saved..............######')
    else:
        print('data not saved..............######')

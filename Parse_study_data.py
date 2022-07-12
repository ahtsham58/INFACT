import pandas as pd
import os
import json
import re


class filter_studies:

    def __init__(self):
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        self.valid = True

    #to filter and export results of all valid trials
    def parse_study_data(self, filename):
            trial_data_sheet = pd.DataFrame()

            cols = ['user_ID','valid','hitcode','kgsf_rating','kgsf_response','kbrd_rating','kbrd_response','our_rating','our_response','dialog_id','trial_time','fragment']
            demo_cols = ['user_ID','age','education','english','gender','movie_crs','other_crs','movies_watched']
            feedback_cols = ['user_ID','Total_demopage_time','Total_feedback_time','Total_study_time','home_page_time','attention_hit','chatbot_useful','crs_usuage','dlg_humans','dlg_initiation','dlg_realistic','group','remarks']
            with open(filename, 'r') as myfile:
                data=myfile.read()
            data_obj = json.loads(data)
            data_array = data_obj['CRS_Study']
            trial_data_list =[]
            invalid_study = []
            valid_demographic =[]
            valid_feedback = []
            valid_feedback = []
            for node_key in data_array.__iter__():
                is_valid_study_list= []
                trials = data_array[node_key]
                is_valid  = self.check_if_test_pass(trials)
                #only for valid studies
                if is_valid:
                    #demo, feedback = self.parse_questionnaire(trials)
                    for trial_index in trials:
                        # handle questionnaire here
                        if trial_index == 'Questionnaire':
                            try:
                                demographic = trials[trial_index]['Demographic']
                                feedback = trials[trial_index]['Feedback']
                                valid_demographic.append({'user_ID':node_key,'age':demographic['age'],'education':demographic['education_level'],'english':demographic['english_level'],'gender':demographic['gender'],'movie_crs':demographic['movie_crs'],'other_crs':demographic['other_domain_crs'],'movies_watched':demographic['movies_watched']})
                                try:
                                    valid_feedback.append({'user_ID':node_key,'Total_demopage_time':demographic['Total_questionaire_time'],'Total_feedback_time':feedback['Total_feedback_time'],'Total_study_time':feedback['Total_study_time'],'home_page_time':feedback['home_page_time'],'attention_hit':feedback['attention_hit'],
                                                       'chatbot_useful':feedback['chatbot_useful'],'crs_usuage':feedback['crs_usuage'],'dlg_humans':feedback['dlg_humans'],'dlg_initiation':feedback['dlg_initiation'],'dlg_realistic':feedback['dlg_realistic'],'group':feedback['group'],'remarks':feedback['remarks']})
                                except KeyError:
                                    valid_feedback.append({'user_ID':node_key,'Total_demopage_time':demographic['Total_questionaire_time'],'Total_feedback_time':feedback['Total_feedback_time'],'Total_study_time':feedback['Total_study_time'],'home_page_time':feedback['home_page_time'],'attention_hit':feedback['attention_hit'],
                                                       'chatbot_useful':feedback['chatbot_useful'],'crs_usuage':feedback['crs_usuage'],'dlg_humans':feedback['dlg_humans'],'dlg_initiation':feedback['dlg_initiation'],'dlg_realistic':feedback['dlg_realistic'],'group':'Null','remarks':feedback['remarks']})
                            except:
                                print('exception here')
                        #Handle trials here
                        else:
                            try:
                                feedback = trials['Questionnaire']['Feedback']
                                trial = trials[trial_index]
                                #DISCARD ATTENTION CHECK SITUATION
                                if int(trial['Dialog_ID']) == 6 and trial['Deep_crs_response'].strip()== 'What kind of movies are you looking for?' and trial['Our_response'].strip() == 'I am reading this carefully, and I give a rating of "Meaningless" to all three responses here, "The Godfather (1972)"':
                                    continue
                                valid= 'Yes'
                                trial_data_list.append({'user_ID':node_key,'valid':valid,'hitcode':feedback['hitcode'], 'kgsf_rating':int(trial['Deep_crs_rating']),'kgsf_response':trial['Deep_crs_response'],'kbrd_rating':int(trial['Kbrd_rating']),'kbrd_response':trial['Kbrd_response'],
                                                         'our_rating':int(trial['Our_rating']),'our_response':trial['Our_response'],'dialog_id':int(trial['Dialog_ID']),'trial_time':trial['Time'],'fragment':trial['Fragment']})
                            except:
                                print('exception')
                #invalid studies is handled here
                else:
                    try:
                        for trial_index in trials:
                            if trial_index == 'Questionnaire':
                                # handle questionnaire here
                                continue
                            feedback = trials['Questionnaire']['Feedback']
                            trial = trials[trial_index]
                            valid ='No'
                            invalid_study.append({'user_ID':node_key,'valid':valid,'hitcode':feedback['hitcode'],'kgsf_rating':int(trial['Deep_crs_rating']),'kgsf_response':trial['Deep_crs_response'],'kbrd_rating':int(trial['Kbrd_rating']),'kbrd_response':trial['Kbrd_response'],
                                                     'our_rating':int(trial['Our_rating']),'our_response':trial['Our_response'],'dialog_id':int(trial['Dialog_ID']),'trial_time':trial['Time'],'fragment':trial['Fragment']})
                    except:
                        print('execption')
            df_sheet_valid = pd.DataFrame(trial_data_list,columns=cols)
            df_sheet_invalid = pd.DataFrame(invalid_study,columns=cols)
            demo_sheet_valid = pd.DataFrame(valid_demographic,columns=demo_cols)
            feedback_sheet_valid = pd.DataFrame(valid_feedback,columns = feedback_cols)
            return df_sheet_valid,df_sheet_invalid, demo_sheet_valid, feedback_sheet_valid


    def parse_questionnaire(self, trails):
        demographic = trails['Questionnaire']['Demographic']
        feedback = trails['Questionnaire']['Feedback']
        return demographic, feedback

    #Verifying attention check situation
    def check_if_test_pass(self,trials):
        try:
            self.valid = False
            for trial_index in trials:
                if trial_index == 'Questionnaire':
                    # handle questionnaire here
                    continue
                trial = trials[trial_index]
                if int(trial['Dialog_ID']) == 6 and trial['Deep_crs_response'].strip()== 'What kind of movies are you looking for?' and trial['Our_response'].strip() == 'I am reading this carefully, and I give a rating of "Meaningless" to all three responses here, "The Godfather (1972)"':
                    if int(trial['Our_rating']) < 3:
                        self.valid= True
                        break

            return self.valid
        except:
            print('exception accured here')

if __name__ == '__main__':
    obj = filter_studies()
    file_name = obj.PATH + '\\crsframework-export.json'
    valid_results, invalid_results, demo_sheet_valid, feedback_sheet_valid = obj.parse_study_data(file_name)
    valid_results.to_excel(obj.PATH +'\\valid_study_data.xlsx')
    demo_sheet_valid.to_excel(obj.PATH+ '\\valid_demographic_data.xlsx')
    feedback_sheet_valid.to_excel(obj.PATH+'\\valid_feedback_data.xlsx')
    invalid_results.to_excel(obj.PATH+'\\invalid_study_data.xlsx')

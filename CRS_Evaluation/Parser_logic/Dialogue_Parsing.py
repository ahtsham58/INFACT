import random
from CRS_Evaluation.settings import settings_dir
from CRS_Evaluation.settings import PROJECT_ROOT
from CRS_Evaluation.settings import DATA_ROOT
from CRS_Evaluation.settings import INPUT_DIALOGUE_FILENAME
from CRS_Evaluation.settings import OUR_SYSTEM_FILENAME
from CRS_Evaluation.settings import DEEP_CRS_SYSTEM_FILENAME
from CRS_Evaluation.settings import KBRD_SYSTEM_FILENAME
import re
import string
import os

class Dialogue_Parsing:
    def __init__(self):
        self.path_to_input_file = os.path.join(DATA_ROOT,INPUT_DIALOGUE_FILENAME)
        self.path_to_our_system = os.path.join(DATA_ROOT,OUR_SYSTEM_FILENAME)
        self.path_to_deep_crs_system = os.path.join(DATA_ROOT,DEEP_CRS_SYSTEM_FILENAME)
        self.path_to_kbrd_system = os.path.join(DATA_ROOT,KBRD_SYSTEM_FILENAME)
        self.redial_dialogues = []
        self.our_dialogues = []
        self.deep_crs_dialogues = []
        self.kbrd_dialogues = []
        self.sessionID = None
        self.dialog_ID = 0
        self.fragment_number = 0
        if len(self.redial_dialogues) < 1:
            self.redial_dialogues = self.read_dialogs(self.path_to_input_file)
        if len(self.our_dialogues) < 1:
            self.our_dialogues = self.read_dialogs(self.path_to_our_system)
        if len(self.deep_crs_dialogues) < 1:
            self.deep_crs_dialogues = self.read_dialogs(self.path_to_deep_crs_system)
        if len(self.kbrd_dialogues) < 1:
            self.kbrd_dialogues = self.read_dialogs(self.path_to_kbrd_system)

    """
    A mathod to read the systems' dialogs from the files.
    Note that each dialog must be indicated with 'CONVERSATION:' keyword followed by the unique number of conversation
    """
    def read_dialogs(self, path_to_input_file):
            is_visited = False
            dialogues = []
            dialog = []
            with open(path_to_input_file, 'r', encoding='utf-8') as input:
                for line in input:
                    if not line.strip(): continue
                    if 'CONVERSATION:' in line and is_visited:
                        dialogues.append(dialog)
                        dialog = []
                        dialog.append(line)
                        is_visited = False
                    else:
                        dialog.append(line)
                        is_visited = True
            dialogues.append(dialog)
            return dialogues

    """
    A method to compute and randomly select the dialog situation (fragment).
    Note that, a 'user' or 'seeker' utterance must be initiated as 'USER:' in the dialogs 
    """
    def show_fragment(self, request):
        is_seeker_initiative = False
        dialog = None
        dialog_id = None
        if len(self.redial_dialogues) > 0:
            n = random.randint(0, len(self.redial_dialogues) - 1)
            dialog = self.redial_dialogues[n] ## select the dialog randomly from the set of dialogs

            if dialog[1].__contains__('USER:'):
                is_seeker_initiative= True
            dialog_id  = int(dialog[0].split(':')[1])  ## parse the dialgo ID mentioned in the selected conversation


            # compute the dailog fragment size, so that the dialog situation always ends with a 'USER:' utterance
            if is_seeker_initiative:
                n1 = 0   #avoid first sentence + add offset if required
                n2 = random.randrange(n1+3, len(dialog) - 1,2)
                n2 = n2-1
                dialog = dialog[n1:n2]
                return dialog, dialog_id
            else:
                if len(dialog)%2 == 0:
                    n1 = 0
                    n2 = random.randrange(n1+3, len(dialog)-1 ,2)
                    dialog = dialog[n1:n2]
                    print('GT initiaitve   .....' + str(n2))
                    return dialog, dialog_id
                else:
                    n1 = 0
                    n2 = random.randrange(n1+3, len(dialog)-3 ,2)
                    dialog = dialog[n1:n2]
                    print('GT initiaitve   .....' + str(n2))
                    return dialog, dialog_id

        else:
            print("Unable to read the file containing dialog conversations between a human-user and the human-recommender")
            return dialog, dialog_id


    """
    A method to compute the dailog fragment and responses from the input dataset in order to show an attention check.
    Note that, in our current implementation, we created another attention check situation, manually crafted in views.py file, e.g., see method 'display_rating_page_attention_check'.
    """
    def show_fragment_attention_check(self, request):
        is_seeker_initiative = False
        if len(self.redial_dialogues) > 0:
            #get a randome dialogue
            n = random.randint(0, len(self.redial_dialogues) - 1)
            dialog = self.redial_dialogues[5]
            if dialog[1].__contains__('USER:'):
                is_seeker_initiative= True
            dialog_id  = int(dialog[0].split(':')[1])

            print(str(dialog_id) + ' dialog number ...................')
            #get a randomised fragment
            n1 = 0
            n2 = 2
            dialog = dialog[n1:n2]
            print(*dialog)
            return dialog, dialog_id


    """
    Once the dialog fragment is slected, now its time to retrieve the corresponding system's response based on the selected dialog fragment
    Note that 'our' means for one of the three systems
    """
    def show_our_sentence(self,dialog):
        is_seeker_initiative = False
        #print(*dialog)
        dialog_num = int(dialog[0].split(':')[1])-1
        #print('the dialogue number is .......' + str(dialog_num))
        our_sentence = ''
        if len(self.our_dialogues) > 0:
            if dialog[1].__contains__('USER:'):
                is_seeker_initiative = True

            if is_seeker_initiative:
                sentences_offset = len(dialog)+ int(len(dialog)/2)-1
                our_sentence = self.our_dialogues[dialog_num][sentences_offset]
            else:
                sentences_offset = len(dialog)+ int(len(dialog)/2) -1
                our_sentence = self.our_dialogues[dialog_num][sentences_offset]
        print('our sentence is ......' + our_sentence)
        return our_sentence.strip()

    """
    A method to retrieve the corresponding system's response based on the selected dialog fragment
    Note that 'deepcrs' means for one of the three systems
    """
    def show_deep_crs_sentence(self,dialog):
        is_seeker_initiative = False
        dialog_num = int(dialog[0].split(':')[1]) -1
        #print('the deep crs dialogue number is .......' + str(dialog_num))
        #print(*dialog)
        deep_crs_sentence = ''
        if len(self.deep_crs_dialogues) > 0:
            if dialog[1].__contains__('USER:'):
                is_seeker_initiative = True

             # get next generated sentences  on seeker query
            if is_seeker_initiative:
                sentences_offset = len(dialog)+ int(len(dialog)/2)
                #print('the deep crs sentences offset is .......' + str(sentences_offset))
                #print(self.deep_crs_dialogues[dialog_num])
                deep_crs_sentence = self.deep_crs_dialogues[dialog_num][sentences_offset]

            # get next generated sentences
            else:
                sentences_offset = len(dialog)+ int(len(dialog)/2) +1
                #print(self.deep_crs_dialogues[dialog_num])
                deep_crs_sentence = self.deep_crs_dialogues[dialog_num][sentences_offset]

        if deep_crs_sentence and deep_crs_sentence.__contains__('GENERATED'):
                p = re.compile("T=1:(.*)").search(str(deep_crs_sentence))
                temp_line= p.group(1)
                m=re.compile('<s>(.*?)</s>').search(temp_line)
                deep_crs_sentence = m.group(1)
        print('Deep CRS sentence is ......' + deep_crs_sentence)
        return deep_crs_sentence.strip()


    """
    A method to retrieve the corresponding system's response based on the selected dialog fragment
    Note that 'kbrd' means for one of the three systems
    """
    def show_kbrd_sentence(self,dialog):
        is_seeker_initiative = False
        dialog_num = int(dialog[0].split(':')[1]) -1
        #print('the deep crs dialogue number is .......' + str(dialog_num))
        #print(*dialog)
        kbrd_sentence = ''
        if len(self.kbrd_dialogues) > 0:
            if dialog[1].__contains__('USER:'):
                is_seeker_initiative = True

            if is_seeker_initiative:
                sentences_offset = len(dialog)+ int(len(dialog)/2)
                kbrd_sentence = self.kbrd_dialogues[dialog_num][sentences_offset]

            else:
                sentences_offset = len(dialog)+ int(len(dialog)/2) +1
                kbrd_sentence = self.kbrd_dialogues[dialog_num][sentences_offset]

        print('kbrd sentence is ......' + kbrd_sentence)
        return kbrd_sentence.strip()

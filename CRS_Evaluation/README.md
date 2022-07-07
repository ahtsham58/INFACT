 # Source Code Description
 Here we mention the overview of the directories and their underlying script or data files. 

## CRS_Evaluation
 In this directory, we have files related to the website configurations, settings, and Firebase (database) integeration.  For example,
 
 1. The file named 'firebase-SDK.json' contains the SDK of your Firebase cloud account, thereby the sepecific database-project details, e.g., in our case, it is 'CRS_Evaluation'. You may export these details from the Firebase platfrom directly. 
 
 2. The file 'firebase-sdk.py' basically connects web application to your firebased project that is created to store data.
 
 3. The file 'settings.py' contains configurations for the INFACT framework. For example, time-zone, paths to the resource files, total No. of dialogs to evaluate (TOTAL_DIALOGUES), total No. of dialog situations (TOTAL_FRAGMENTS) for one participant, language, etc.
 
 4. In addition, we have a few more files related to the internal Django settings and URLs.
 
 
 ## Parser_logic
 In this directory, we have mianly three files that are important to know.

1. The file named 'Dialogue_Parsing.py' contains code for the: (i) selection and computation of dialog situation size on loading the rating page. Basically, the dialog situation is fetched from the file containing conversations form the test set of the ReDial dataset (ii) retrieve their corresponding responses from the files containing  dialogs and responses generated with different CRS, for example in this case, we have KBRD, KGSF, CRB-CRS.

2. The file named 'views.py' contains the views for each template page shown to the user, e.g., index.html, ratings.html, etc.

3. Finally, we have a list of all the URLs for pages implemented in the INFACT application linked with their respective views.

## Resources:
In this directory, we have evaluation data for dialogs to be assessed and their corresponding responses generated with a particular CRS. For example

1. The file named 'dialogue_data.txt' contains dialogs betweens a human-user and recommender collected in the context of the ReDial dataset.

2. The remaining files contain the conversations along with their systen generated responses produced using a specific CRS as a baseline, like KBRD, KGSF, etc. 

## Templates
In this directory, we have html/css scripts for all the web-pages used in the application.

In addition, at this root directory, we have more files, like

1. 'db.sqlite3', which can be used in case of integerating sqlite database with the application. Note that, in default case, we are using cloud database, i.e., Firebase.

2. 'manage.py' is the very first point where application starts its execution either it is hosted on the localhost or server.
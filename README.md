# INFACT: An Online Human Evaluation Framework for Conversational Recommendation

This repository contains complete source code of the INFACT framework, which is developed to facilitate the user-centric evaluation studies of dialog systems, conversational recommender systems, and related domains.

## Installation

Basically, To run the project on localhost, first you need to create and activate a virtual environment for your Django project. Therefore, please follow the below commands sequentially  

```bash
cd CRS_Evaluation
python3 -m pip install --upgrade pip
pip3 install requirement.txt
pip3 install virtualenv
```
To verify the installation of virtual environment library, use
```bash
which virtualenv
```

Now, create a virtual environment for the INFACT framework using

```bash
virtualenv venv
```
Activate your venv
```bash
source ./venv/bin/activate
```
After this command, you should be able to see venv as a virtual environment created in your command promt.

Once you create and activate your virtual environment, to run the localhost, use
```bash
python3 manage.py runserv
```

Once your localhost server is ready, hit this [URL]( http://127.0.0.1:8000/ ) in a browser and experience the wonders
```bash
 http://127.0.0.1:8000/
```

## How to parse the JSON data collected with this study?

The Python script named _**'Parse_study_data.py'**_ can be used to parse the complete data into MS excel sheets.

INPUT: JSON study data

OUTPUT: Separate excel sheets for valid, invalid rating scores, demographic, and feedback questionnaires.

## Helpful links
You may have a look at the below links in case of abbration in activating the virtual environment

[Install Django using virtualenv](https://help.dreamhost.com/hc/en-us/articles/215317948-Install-Django-using-virtualenv)

[Configure a virtual environment in PyCharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)

[Create a virtual environment in PyCharm terminal](https://www.codegrepper.com/code-examples/shell/create+a+virtual+environment+python+pycharm)



## **Citation**
```
@InProceedings{manzoor2022infact,
  title={INFACT: An Online Human Evaluation Framework for Conversational Recommendation},
  author={Manzoor, Ahtsham and Jannach, Dietmar},
  booktitle={KaRS Workshop at RecSys '22},
  address = {Seattle, USA},
  year={2022},
  keywords = {Conversational Recommender Systems, user-centric studies, evaluation, dialog systems},
}
```


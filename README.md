# TextAnalyzer
This project provides a Django-based RESTful API for analyzing Spanish text. 
It utilizes spaCy for natural language processing and DeepL for translation. 
Users can register, log in, analyze text, and view their analysis logs.


## Installation
Clone the repository: <br>
git clone https://github.com/megiihoxha/text_analyzer_app.git <br>
cd text_analyzer_app


## Set up a virtual environment:
python -m venv venv <br>
source venv/bin/activate

## Install the required packages:
pip install -r requirements.txt


## Apply database migrations:
python manage.py migrate


## Run the development server:
python manage.py runserver

# Soccer
AI-Powered Soccer Match Prediction and Betting Model.

This AI-driven betting model is designed to generate predictions and betting odds for upcoming soccer matches across global leagues. Leveraging classification algorithms and predictive models such as XGBoost, Decision Trees, Poisson Distribution, and ELO Rating, the system achieves over 70% prediction accuracy.

AI-Powered Soccer Match Prediction and Betting Model
Seamless CSV Import from Any Source
To further enhance precision, the model is continuously trained with sentiment analysis data related to teams, players, and match conditions.

Key components of the system include:
--------------------------------------

Predictive analytics for match outcomes, win/draw/loss probabilities, and bettingAn AWS-based data warehouse that ingests and processes raw data from multiple sourcesStorage of processed and structured data in a Data Lakehouse architecture
This platform serves as a comprehensive solution for bettors, analysts, and fans seeking data-driven insights and predictions in the world of soccer

Technology :
python,Django,Datbrics,Fast API,PGSQL


install  requirement.txt  
Pip install -r requirement.txt
then run python manage.py runserver 
Run AI Model
uvicorn main:app --host 0.0.0.0 --port 8008

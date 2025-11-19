# import uvicorn
# import validators
# import joblib
import validators
# import datetime
import json
from typing import List
import pandas as pd
from scipy.stats import poisson
from fastapi import FastAPI, UploadFile, File
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fractions import Fraction
import numpy  as np
import pickle
import datetime
import time
import requests

with open('xgb_model_epl.pkl', 'rb') as f:
    model1 = pickle.load(f)
    
with open('xgb_model_bundesliga.pkl', 'rb') as f:
    model2 = pickle.load(f)

with open('xgb_model_italy.pkl', 'rb') as f:
    model3 = pickle.load(f)
with open('xgb_model_france.pkl', 'rb') as f:
    model4 = pickle.load(f)

with open('xgb_model_laliga.pkl', 'rb') as f:
    model5 = pickle.load(f)



sportsradar_clubelo_mapping = [
          {
            "sportsradar_competitor_id": "sr:competitor:2814",
            "sportsradar_competitor_short_name": "Espanyol",
            "clubelo_team_name": "Espanyol",
            "betfair_team_name": "Espanyol",
            "poisson_team name": "Espanol"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2816",
            "sportsradar_competitor_short_name": "Real Betis",
            "clubelo_team_name": "Betis",
            "betfair_team_name": "Betis",
            "poisson_team name": "Betis"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2817",
            "sportsradar_competitor_short_name": "Barcelona",
            "clubelo_team_name": "Barcelona",
            "betfair_team_name": "Barcelona",
            "poisson_team name": "Barcelona"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2818",
            "sportsradar_competitor_short_name": "Vallecano",
            "clubelo_team_name": "Rayo Vallecano",
            "betfair_team_name": "Rayo Vallecano",
            "poisson_team name": "Vallecano"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2819",
            "sportsradar_competitor_short_name": "Villarreal",
            "clubelo_team_name": "Villarreal",
            "betfair_team_name": "Villarreal",
            "poisson_team name": "Villarreal"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2820",
            "sportsradar_competitor_short_name": "Osasuna",
            "clubelo_team_name": "Osasuna",
            "betfair_team_name": "Osasuna",
            "poisson_team name": "Osasuna"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2821",
            "sportsradar_competitor_short_name": "Celta Vigo",
            "clubelo_team_name": "Celta",
            "betfair_team_name": "Celta Vigo",
            "poisson_team name": "Celta"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2824",
            "sportsradar_competitor_short_name": "Real Sociedad",
            "clubelo_team_name": "Sociedad",
            "betfair_team_name": "Real Sociedad",
            "poisson_team name": "Sociedad"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2825",
            "sportsradar_competitor_short_name": "Bilbao",
            "clubelo_team_name": "Bilbao",
            "betfair_team_name": "Athletic Bilbao",
            "poisson_team name": "Ath Bilbao"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2826",
            "sportsradar_competitor_short_name": "Mallorca",
            "clubelo_team_name": "Mallorca",
            "betfair_team_name": "Mallorca",
            "poisson_team name": "Mallorca"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2828",
            "sportsradar_competitor_short_name": "Valencia",
            "clubelo_team_name": "Valencia",
            "betfair_team_name": "Valencia",
            "poisson_team name": "Valencia"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2829",
            "sportsradar_competitor_short_name": "Real Madrid",
            "clubelo_team_name": "Real Madrid",
            "betfair_team_name": "Real Madrid",
            "poisson_team name": "Real Madrid"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2831",
            "sportsradar_competitor_short_name": "Valladolid",
            "clubelo_team_name": "Valladolid",
            "betfair_team_name": "Valladolid",
            "poisson_team name": "Valladolid"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2833",
            "sportsradar_competitor_short_name": "Sevilla",
            "clubelo_team_name": "Sevilla",
            "betfair_team_name": "Sevilla",
            "poisson_team name": "Sevilla"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2836",
            "sportsradar_competitor_short_name": "Atletico",
            "clubelo_team_name": "Atletico",
            "betfair_team_name": "Atletico Madrid",
            "poisson_team name": "Ath Madrid"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2846",
            "sportsradar_competitor_short_name": "Elche",
            "clubelo_team_name": "Elche",
            "betfair_team_name": "Elche",
            "poisson_team name": "Elche"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2858",
            "sportsradar_competitor_short_name": "Almeria",
            "clubelo_team_name": "Almeria",
            "betfair_team_name": "Almeria",
            "poisson_team name": "Almeria"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2859",
            "sportsradar_competitor_short_name": "Getafe",
            "clubelo_team_name": "Getafe",
            "betfair_team_name": "Getafe",
            "poisson_team name": "Getafe"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:4488",
            "sportsradar_competitor_short_name": "Cadiz",
            "clubelo_team_name": "Cadiz",
            "betfair_team_name": "Cadiz",
            "poisson_team name": "Cadiz"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:24264",
            "sportsradar_competitor_short_name": "Girona",
            "clubelo_team_name": "Girona",
            "betfair_team_name": "Girona",
            "poisson_team name": "Girona"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1641",
            "sportsradar_competitor_short_name": "Marseille",
            "clubelo_team_name": "Marseille",
            "betfair_team_name": "Marseille",
            "poisson_team name": "Marseille"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1642",
            "sportsradar_competitor_short_name": "Montpellier",
            "clubelo_team_name": "Montpellier",
            "betfair_team_name": "Montpellier",
            "poisson_team name": "Montpellier"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1643",
            "sportsradar_competitor_short_name": "Lille",
            "clubelo_team_name": "Lille",
            "betfair_team_name": "Lille",
            "poisson_team name": "Lille"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1644",
            "sportsradar_competitor_short_name": "PSG",
            "clubelo_team_name": "Paris SG",
            "betfair_team_name": "Paris St-G",
            "poisson_team name": "Paris SG"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1646",
            "sportsradar_competitor_short_name": "Auxerre",
            "clubelo_team_name": "Auxerre",
            "betfair_team_name": "Auxerre",
            "poisson_team name": "Auxerre"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1647",
            "sportsradar_competitor_short_name": "Nantes",
            "clubelo_team_name": "Nantes",
            "betfair_team_name": "Nantes",
            "poisson_team name": "Nantes"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1648",
            "sportsradar_competitor_short_name": "Lens",
            "clubelo_team_name": "Lens",
            "betfair_team_name": "Lens",
            "poisson_team name": "Lens"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1649",
            "sportsradar_competitor_short_name": "Lyon",
            "clubelo_team_name": "Lyon",
            "betfair_team_name": "Lyon",
            "poisson_team name": "Lyon"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1652",
            "sportsradar_competitor_short_name": "Troyes",
            "clubelo_team_name": "Troyes",
            "betfair_team_name": "ESTAC Troyes",
            "poisson_team name": "Troyes"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1653",
            "sportsradar_competitor_short_name": "Monaco",
            "clubelo_team_name": "Monaco",
            "betfair_team_name": "Monaco",
            "poisson_team name": "Monaco"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1656",
            "sportsradar_competitor_short_name": "Lorient",
            "clubelo_team_name": "Lorient",
            "betfair_team_name": "Lorient",
            "poisson_team name": "Lorient"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1658",
            "sportsradar_competitor_short_name": "Stade Rennes",
            "clubelo_team_name": "Rennes",
            "betfair_team_name": "Rennes",
            "poisson_team name": "Rennes"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1659",
            "sportsradar_competitor_short_name": "Strasbourg Alsace",
            "clubelo_team_name": "Strasbourg",
            "betfair_team_name": "Strasbourg",
            "poisson_team name": "Strasbourg"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1660",
            "sportsradar_competitor_short_name": "AC Ajaccio",
            "clubelo_team_name": "Ajaccio",
            "betfair_team_name": "AC Ajaccio",
            "poisson_team name": "Ajaccio"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1661",
            "sportsradar_competitor_short_name": "Nice",
            "clubelo_team_name": "Nice",
            "betfair_team_name": "Nice",
            "poisson_team name": "Nice"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1680",
            "sportsradar_competitor_short_name": "Clermont Foot",
            "clubelo_team_name": "Clermont",
            "betfair_team_name": "Clermont",
            "poisson_team name": "Clermont"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1681",
            "sportsradar_competitor_short_name": "Toulouse",
            "clubelo_team_name": "Toulouse",
            "betfair_team_name": "Toulouse",
            "poisson_team name": "Toulouse"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1682",
            "sportsradar_competitor_short_name": "Reims",
            "clubelo_team_name": "Reims",
            "betfair_team_name": "Reims",
            "poisson_team name": "Reims"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1684",
            "sportsradar_competitor_short_name": "Angers",
            "clubelo_team_name": "Angers",
            "betfair_team_name": "Angers",
            "poisson_team name": "Angers"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:1715",
            "sportsradar_competitor_short_name": "Stade Brest 29",
            "clubelo_team_name": "Brest",
            "betfair_team_name": "Brest",
            "poisson_team name": "Brest"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:3",
            "sportsradar_competitor_short_name": "Wolverhampton",
            "clubelo_team_name": "Wolves",
            "betfair_team_name": "Wolves",
            "poisson_team name": "Wolves"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:7",
            "sportsradar_competitor_short_name": "Crystal Palace",
            "clubelo_team_name": "Crystal Palace",
            "betfair_team_name": "Crystal Palace",
            "poisson_team name": "Crystal Palace"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:14",
            "sportsradar_competitor_short_name": "Nottingham",
            "clubelo_team_name": "Forest",
            "betfair_team_name": "Nottm Forest",
            "poisson_team name": "Nottingham"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:17",
            "sportsradar_competitor_short_name": "Man City",
            "clubelo_team_name": "Man City",
            "betfair_team_name": "Man City",
            "poisson_team name": "Man City"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:30",
            "sportsradar_competitor_short_name": "Brighton",
            "clubelo_team_name": "Brighton",
            "betfair_team_name": "Brighton",
            "poisson_team name": "Brighton"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:31",
            "sportsradar_competitor_short_name": "Leicester",
            "clubelo_team_name": "Leicester",
            "betfair_team_name": "Leicester",
            "poisson_team name": "Leicester"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:33",
            "sportsradar_competitor_short_name": "Tottenham",
            "clubelo_team_name": "Tottenham",
            "betfair_team_name": "Tottenham ",
            "poisson_team name": "Tottenham"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:34",
            "sportsradar_competitor_short_name": "Leeds United",
            "clubelo_team_name": "Leeds",
            "betfair_team_name": "Leeds",
            "poisson_team name": "Leeds"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:35",
            "sportsradar_competitor_short_name": "Man Utd",
            "clubelo_team_name": "Man United",
            "betfair_team_name": "Man Utd",
            "poisson_team name": "Man United"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:37",
            "sportsradar_competitor_short_name": "West Ham",
            "clubelo_team_name": "West Ham",
            "betfair_team_name": "West Ham",
            "poisson_team name": "West Ham"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:38",
            "sportsradar_competitor_short_name": "Chelsea",
            "clubelo_team_name": "Chelsea",
            "betfair_team_name": "Chelsea",
            "poisson_team name": "Chelsea"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:39",
            "sportsradar_competitor_short_name": "Newcastle",
            "clubelo_team_name": "Newcastle",
            "betfair_team_name": "Newcastle ",
            "poisson_team name": "Newcastle"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:40",
            "sportsradar_competitor_short_name": "Aston Villa",
            "clubelo_team_name": "Aston Villa",
            "betfair_team_name": "Aston Villa",
            "poisson_team name": "Aston Villa"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:42",
            "sportsradar_competitor_short_name": "Arsenal",
            "clubelo_team_name": "Arsenal",
            "betfair_team_name": "Arsenal",
            "poisson_team name": "Arsenal"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:43",
            "sportsradar_competitor_short_name": "Fulham",
            "clubelo_team_name": "Fulham",
            "betfair_team_name": "Fulham",
            "poisson_team name": "Fulham"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:44",
            "sportsradar_competitor_short_name": "Liverpool",
            "clubelo_team_name": "Liverpool",
            "betfair_team_name": "Liverpool",
            "poisson_team name": "Liverpool"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:45",
            "sportsradar_competitor_short_name": "Southampton",
            "clubelo_team_name": "Southampton",
            "betfair_team_name": "Southampton",
            "poisson_team name": "Southampton"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:48",
            "sportsradar_competitor_short_name": "Everton",
            "clubelo_team_name": "Everton",
            "betfair_team_name": "Everton ",
            "poisson_team name": "Everton"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:50",
            "sportsradar_competitor_short_name": "Brentford",
            "clubelo_team_name": "Brentford",
            "betfair_team_name": "Brentford",
            "poisson_team name": "Brentford"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:60",
            "sportsradar_competitor_short_name": "Bournemouth",
            "clubelo_team_name": "Bournemouth",
            "betfair_team_name": "Bournemouth",
            "poisson_team name": "Bournemouth"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2685",
            "sportsradar_competitor_short_name": "Bologna",
            "clubelo_team_name": "Bologna",
            "betfair_team_name": "Bologna",
            "poisson_team name": "Bologna"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2686",
            "sportsradar_competitor_short_name": "Atalanta",
            "clubelo_team_name": "Atalanta",
            "betfair_team_name": "Atalanta",
            "poisson_team name": "Atalanta"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2687",
            "sportsradar_competitor_short_name": "Juventus",
            "clubelo_team_name": "Juventus",
            "betfair_team_name": "Juventus",
            "poisson_team name": "Juventus"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2689",
            "sportsradar_competitor_short_name": "Lecce",
            "clubelo_team_name": "Lecce",
            "betfair_team_name": "Lecce",
            "poisson_team name": "Lecce"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2692",
            "sportsradar_competitor_short_name": "Milan",
            "clubelo_team_name": "Milan",
            "betfair_team_name": "AC Milan",
            "poisson_team name": "Milan"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2693",
            "sportsradar_competitor_short_name": "Fiorentina",
            "clubelo_team_name": "Fiorentina",
            "betfair_team_name": "Fiorentina",
            "poisson_team name": "Fiorentina"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2695",
            "sportsradar_competitor_short_name": "Udinese",
            "clubelo_team_name": "Udinese",
            "betfair_team_name": "Udinese",
            "poisson_team name": "Udinese"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2696",
            "sportsradar_competitor_short_name": "Torino",
            "clubelo_team_name": "Torino",
            "betfair_team_name": "Torino",
            "poisson_team name": "Torino"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2697",
            "sportsradar_competitor_short_name": "Inter",
            "clubelo_team_name": "Inter",
            "betfair_team_name": "Inter",
            "poisson_team name": "Inter"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2699",
            "sportsradar_competitor_short_name": "Lazio",
            "clubelo_team_name": "Lazio",
            "betfair_team_name": "Lazio",
            "poisson_team name": "Lazio"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2701",
            "sportsradar_competitor_short_name": "Hellas Verona",
            "clubelo_team_name": "Verona",
            "betfair_team_name": "Verona",
            "poisson_team name": "Verona"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2702",
            "sportsradar_competitor_short_name": "Roma",
            "clubelo_team_name": "Roma",
            "betfair_team_name": "Roma",
            "poisson_team name": "Roma"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2705",
            "sportsradar_competitor_short_name": "Empoli",
            "clubelo_team_name": "Empoli",
            "betfair_team_name": "Empoli",
            "poisson_team name": "Empoli"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2710",
            "sportsradar_competitor_short_name": "Salernitana",
            "clubelo_team_name": "Salernitana",
            "betfair_team_name": "Salernitana",
            "poisson_team name": "Salernitana"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2711",
            "sportsradar_competitor_short_name": "Sampdoria",
            "clubelo_team_name": "Sampdoria",
            "betfair_team_name": "Sampdoria",
            "poisson_team name": "Sampdoria"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2714",
            "sportsradar_competitor_short_name": "Napoli",
            "clubelo_team_name": "Napoli",
            "betfair_team_name": "Napoli",
            "poisson_team name": "Napoli"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2729",
            "sportsradar_competitor_short_name": "Monza",
            "clubelo_team_name": "Monza",
            "betfair_team_name": "AC Monza",
            "poisson_team name": "Monza"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2735",
            "sportsradar_competitor_short_name": "Spezia",
            "clubelo_team_name": "Spezia",
            "betfair_team_name": "Spezia",
            "poisson_team name": "Spezia"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2761",
            "sportsradar_competitor_short_name": "Cremonese",
            "clubelo_team_name": "Cremonese",
            "betfair_team_name": "US Cremonese",
            "poisson_team name": "Cremonese"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2793",
            "sportsradar_competitor_short_name": "Sassuolo",
            "clubelo_team_name": "Sassuolo",
            "betfair_team_name": "Sassuolo",
            "poisson_team name": "Sassuolo"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2524",
            "sportsradar_competitor_short_name": "Wolfsburg",
            "clubelo_team_name": "Wolfsburg",
            "betfair_team_name": "Wolfsburg",
            "poisson_team name": "Wolfsburg"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2527",
            "sportsradar_competitor_short_name": "M'gladbach",
            "clubelo_team_name": "Gladbach",
            "betfair_team_name": "Mgladbach",
            "poisson_team name": "M'gladbach"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2528",
            "sportsradar_competitor_short_name": "Hertha",
            "clubelo_team_name": "Hertha",
            "betfair_team_name": "Hertha Berlin",
            "poisson_team name": "Hertha"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2530",
            "sportsradar_competitor_short_name": "Schalke",
            "clubelo_team_name": "Schalke",
            "betfair_team_name": "Schalke 04",
            "poisson_team name": "Schalke 04"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2534",
            "sportsradar_competitor_short_name": "Bremen",
            "clubelo_team_name": "Werder",
            "betfair_team_name": "Werder Bremen",
            "poisson_team name": "Werder Bremen"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2538",
            "sportsradar_competitor_short_name": "Freiburg",
            "clubelo_team_name": "Freiburg",
            "betfair_team_name": "Freiburg",
            "poisson_team name": "Freiburg"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2542",
            "sportsradar_competitor_short_name": "Bochum",
            "clubelo_team_name": "Bochum",
            "betfair_team_name": "Bochum",
            "poisson_team name": "Bochum"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2547",
            "sportsradar_competitor_short_name": "Union Berlin",
            "clubelo_team_name": "Union Berlin",
            "betfair_team_name": "Union Berlin",
            "poisson_team name": "Union Berlin"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2556",
            "sportsradar_competitor_short_name": "Mainz",
            "clubelo_team_name": "Mainz",
            "betfair_team_name": "Mainz",
            "poisson_team name": "Mainz"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2569",
            "sportsradar_competitor_short_name": "Hoffenheim",
            "clubelo_team_name": "Hoffenheim",
            "betfair_team_name": "Hoffenheim",
            "poisson_team name": "Hoffenheim"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2600",
            "sportsradar_competitor_short_name": "Augsburg",
            "clubelo_team_name": "Augsburg",
            "betfair_team_name": "Augsburg",
            "poisson_team name": "Augsburg"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2671",
            "sportsradar_competitor_short_name": "1. FC Cologne",
            "clubelo_team_name": "Koeln",
            "betfair_team_name": "FC Koln",
            "poisson_team name": "FC Koln"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2672",
            "sportsradar_competitor_short_name": "B. Munich",
            "clubelo_team_name": "Bayern",
            "betfair_team_name": "Bayern Munich",
            "poisson_team name": "Bayern Munich"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2673",
            "sportsradar_competitor_short_name": "Dortmund",
            "clubelo_team_name": "Dortmund",
            "betfair_team_name": "Dortmund",
            "poisson_team name": "Dortmund"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2674",
            "sportsradar_competitor_short_name": "Frankfurt",
            "clubelo_team_name": "Frankfurt",
            "betfair_team_name": "Eintracht Frankfurt",
            "poisson_team name": "Ein Frankfurt"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2677",
            "sportsradar_competitor_short_name": "Stuttgart",
            "clubelo_team_name": "Stuttgart",
            "betfair_team_name": "Stuttgart",
            "poisson_team name": "Stuttgart"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:2681",
            "sportsradar_competitor_short_name": "Leverkusen",
            "clubelo_team_name": "Leverkusen",
            "betfair_team_name": "Leverkusen",
            "poisson_team name": "Leverkusen"
          },
          {
            "sportsradar_competitor_id": "sr:competitor:36360",
            "sportsradar_competitor_short_name": "Leipzi",
            "clubelo_team_name": "RB Leipzig",
            "betfair_team_name": "RB Leipzig",
            "poisson_team name": "RB Leipzig"
          }
        ]

teams = [
      {
        "name": "sr:competitor:2814",
        "dbname": "Espanol"
      },
      {
        "name": "sr:competitor:2816",
        "dbname": "Betis"
      },
      {
        "name": "sr:competitor:2817",
        "dbname": "Barcelona"
      },
      {
        "name": "sr:competitor:2818",
        "dbname": "Vallecano"
      },
      {
        "name": "sr:competitor:2819",
        "dbname": "Villarreal"
      },
      {
        "name": "sr:competitor:2820",
        "dbname": "Osasuna"
      },
      {
        "name": "sr:competitor:2821",
        "dbname": "Celta"
      },
      {
        "name": "sr:competitor:2824",
        "dbname": "Sociedad"
      },
      {
        "name": "sr:competitor:2825",
        "dbname": "Ath Bilbao"
      },
      {
        "name": "sr:competitor:2826",
        "dbname": "Mallorca"
      },
      {
        "name": "sr:competitor:2828",
        "dbname": "Valencia"
      },
      {
        "name": "sr:competitor:2829",
        "dbname": "Real Madrid"
      },
      {
        "name": "sr:competitor:2831",
        "dbname": "Valladolid"
      },
      {
        "name": "sr:competitor:2833",
        "dbname": "Sevilla"
      },
      {
        "name": "sr:competitor:2836",
        "dbname": "Ath Madrid"
      },
      {
        "name": "sr:competitor:2846",
        "dbname": "Elche"
      },
      {
        "name": "sr:competitor:2858",
        "dbname": "Almeria"
      },
      {
        "name": "sr:competitor:2859",
        "dbname": "Getafe"
      },
      {
        "name": "sr:competitor:4488",
        "dbname": "Cadiz"
      },
      {
        "name": "sr:competitor:24264",
        "dbname": "Girona"
      },
      {
        "name": "sr:competitor:1641",
        "dbname": "Marseille"
      },
      {
        "name": "sr:competitor:1642",
        "dbname": "Montpellier"
      },
      {
        "name": "sr:competitor:1643",
        "dbname": "Lille"
      },
      {
        "name": "sr:competitor:1644",
        "dbname": "Paris SG"
      },
      {
        "name": "sr:competitor:1646",
        "dbname": "Auxerre"
      },
      {
        "name": "sr:competitor:1647",
        "dbname": "Nantes"
      },
      {
        "name": "sr:competitor:1648",
        "dbname": "Lens"
      },
      {
        "name": "sr:competitor:1649",
        "dbname": "Lyon"
      },
      {
        "name": "sr:competitor:1652",
        "dbname": "Troyes"
      },
      {
        "name": "sr:competitor:1653",
        "dbname": "Monaco"
      },
      {
        "name": "sr:competitor:1656",
        "dbname": "Lorient"
      },
      {
        "name": "sr:competitor:1658",
        "dbname": "Rennes"
      },
      {
        "name": "sr:competitor:1659",
        "dbname": "Strasbourg"
      },
      {
        "name": "sr:competitor:1660",
        "dbname": "Ajaccio"
      },
      {
        "name": "sr:competitor:1661",
        "dbname": "Nice"
      },
      {
        "name": "sr:competitor:1680",
        "dbname": "Clermont"
      },
      {
        "name": "sr:competitor:1681",
        "dbname": "Toulouse"
      },
      {
        "name": "sr:competitor:1682",
        "dbname": "Reims"
      },
      {
        "name": "sr:competitor:1684",
        "dbname": "Angers"
      },
      {
        "name": "sr:competitor:1715",
        "dbname": "Brest"
      },
      {
        "name": "sr:competitor:3",
        "dbname": "Wolves"
      },
      {
        "name": "sr:competitor:7",
        "dbname": "Crystal Palace"
      },
      {
        "name": "sr:competitor:14",
        "dbname": "Nottingham"
      },
      {
        "name": "sr:competitor:17",
        "dbname": "Man City"
      },
      {
        "name": "sr:competitor:30",
        "dbname": "Brighton"
      },
      {
        "name": "sr:competitor:31",
        "dbname": "Leicester"
      },
      {
        "name": "sr:competitor:33",
        "dbname": "Tottenham"
      },
      {
        "name": "sr:competitor:34",
        "dbname": "Leeds"
      },
      {
        "name": "sr:competitor:35",
        "dbname": "Man United"
      },
      {
        "name": "sr:competitor:37",
        "dbname": "West Ham"
      },
      {
        "name": "sr:competitor:38",
        "dbname": "Chelsea"
      },
      {
        "name": "sr:competitor:39",
        "dbname": "Newcastle"
      },
      {
        "name": "sr:competitor:40",
        "dbname": "Aston Villa"
      },
      {
        "name": "sr:competitor:42",
        "dbname": "Arsenal"
      },
      {
        "name": "sr:competitor:43",
        "dbname": "Fulham"
      },
      {
        "name": "sr:competitor:44",
        "dbname": "Liverpool"
      },
      {
        "name": "sr:competitor:45",
        "dbname": "Southampton"
      },
      {
        "name": "sr:competitor:48",
        "dbname": "Everton"
      },
      {
        "name": "sr:competitor:50",
        "dbname": "Brentford"
      },
      {
        "name": "sr:competitor:60",
        "dbname": "Bournemouth"
      },
      {
        "name": "sr:competitor:2685",
        "dbname": "Bologna"
      },
      {
        "name": "sr:competitor:2686",
        "dbname": "Atalanta"
      },
      {
        "name": "sr:competitor:2687",
        "dbname": "Juventus"
      },
      {
        "name": "sr:competitor:2689",
        "dbname": "Lecce"
      },
      {
        "name": "sr:competitor:2692",
        "dbname": "Milan"
      },
      {
        "name": "sr:competitor:2693",
        "dbname": "Fiorentina"
      },
      {
        "name": "sr:competitor:2695",
        "dbname": "Udinese"
      },
      {
        "name": "sr:competitor:2696",
        "dbname": "Torino"
      },
      {
        "name": "sr:competitor:2697",
        "dbname": "Inter"
      },
      {
        "name": "sr:competitor:2699",
        "dbname": "Lazio"
      },
      {
        "name": "sr:competitor:2701",
        "dbname": "Verona"
      },
      {
        "name": "sr:competitor:2702",
        "dbname": "Roma"
      },
      {
        "name": "sr:competitor:2705",
        "dbname": "Empoli"
      },
      {
        "name": "sr:competitor:2710",
        "dbname": "Salernitana"
      },
      {
        "name": "sr:competitor:2711",
        "dbname": "Sampdoria"
      },
      {
        "name": "sr:competitor:2714",
        "dbname": "Napoli"
      },
      {
        "name": "sr:competitor:2729",
        "dbname": "Monza"
      },
      {
        "name": "sr:competitor:2735",
        "dbname": "Spezia"
      },
      {
        "name": "sr:competitor:2761",
        "dbname": "Cremonese"
      },
      {
        "name": "sr:competitor:2793",
        "dbname": "Sassuolo"
      },
      {
        "name": "sr:competitor:2524",
        "dbname": "Wolfsburg"
      },
      {
        "name": "sr:competitor:2527",
        "dbname": "M'gladbach"
      },
      {
        "name": "sr:competitor:2528",
        "dbname": "Hertha"
      },
      {
        "name": "sr:competitor:2530",
        "dbname": "Schalke 04"
      },
      {
        "name": "sr:competitor:2534",
        "dbname": "Werder Bremen"
      },
      {
        "name": "sr:competitor:2538",
        "dbname": "Freiburg"
      },
      {
        "name": "sr:competitor:2542",
        "dbname": "Bochum"
      },
      {
        "name": "sr:competitor:2547",
        "dbname": "Union Berlin"
      },
      {
        "name": "sr:competitor:2556",
        "dbname": "Mainz"
      },
      {
        "name": "sr:competitor:2569",
        "dbname": "Hoffenheim"
      },
      {
        "name": "sr:competitor:2600",
        "dbname": "Augsburg"
      },
      {
        "name": "sr:competitor:2671",
        "dbname": "FC Koln"
      },
      {
        "name": "sr:competitor:2672",
        "dbname": "Bayern Munich"
      },
      {
        "name": "sr:competitor:2673",
        "dbname": "Dortmund"
      },
      {
        "name": "sr:competitor:2674",
        "dbname": "Ein Frankfurt"
      },
      {
        "name": "sr:competitor:2677",
        "dbname": "Stuttgart"
      },
      {
        "name": "sr:competitor:2681",
        "dbname": "Leverkusen"
      },
      {
        "name": "sr:competitor:36360",
        "dbname": "RB Leipzig"
      }
    ]

app = FastAPI()

class DataInput(BaseModel):
    competition_id: str
    ht_form_points: int
    at_form_points: int
    ht_avg_shot_on_target: float
    at_avg_shot_on_target: float
    ht_elo_rating: float
    at_elo_rating: float

class UploadString(BaseModel):
	Url: str

class EplDataInput(BaseModel):

    team_1_form_points: int
    team_2_form_points: int
    team_1_avg_shot_on_target: float
    team_2_avg_shot_on_target: float
    team_1_elo_rating: float
    team_2_elo_rating: float
    team_1_form_points_nine: float
    team_2_form_points_nine: float
    team_1_form_points_eight : float
    team_2_form_points_eight : float
    team_1_form_points_seven : float
    team_2_form_points_seven : float
    team_1_avg_shot_on_target_nine : float
    team_2_avg_shot_on_target_nine : float
    team_1_avg_shot_on_target_eight : float
    team_2_avg_shot_on_target_eight : float
    team_1_avg_shot_on_target_seven : float
    team_2_avg_shot_on_target_seven: float
    team_1_elo_rating_nine : float
    team_2_elo_rating_nine  : float
    team_1_elo_rating_eight : float
    team_2_elo_rating_eight : float
    team_1_elo_rating_seven : float
    team_2_elo_rating_seven : float

class FranceDataInput(BaseModel):

    team_1_form_points: int
    team_2_form_points: int
    team_1_avg_shot_on_target: float
    team_2_avg_shot_on_target: float
    team_1_elo_rating: float
    team_2_elo_rating: float
    team_1_form_points_nine: float
    team_2_form_points_nine: float
    team_1_form_points_eight : float
    team_2_form_points_eight : float
    team_1_form_points_seven : float
    team_2_form_points_seven : float
    team_1_avg_shot_on_target_nine : float
    team_2_avg_shot_on_target_nine : float
    team_1_avg_shot_on_target_eight : float
    team_2_avg_shot_on_target_eight : float
    team_1_avg_shot_on_target_seven : float
    team_2_avg_shot_on_target_seven: float
    team_1_elo_rating_nine : float
    team_2_elo_rating_nine  : float
    team_1_elo_rating_eight : float
    team_2_elo_rating_eight : float
    team_1_elo_rating_seven : float
    team_2_elo_rating_seven : float

class GermanyDataInput(BaseModel):

    team_1_form_points: int
    team_2_form_points: int
    team_1_avg_shot_on_target: float
    team_2_avg_shot_on_target: float
    team_1_elo_rating: float
    team_2_elo_rating: float
    team_1_form_points_nine: float
    team_2_form_points_nine: float
    team_1_form_points_eight : float
    team_2_form_points_eight : float
    team_1_form_points_seven : float
    team_2_form_points_seven : float
    team_1_avg_shot_on_target_nine : float
    team_2_avg_shot_on_target_nine : float
    team_1_avg_shot_on_target_eight : float
    team_2_avg_shot_on_target_eight : float
    team_1_avg_shot_on_target_seven : float
    team_2_avg_shot_on_target_seven: float
    team_1_elo_rating_nine : float
    team_2_elo_rating_nine  : float
    team_1_elo_rating_eight : float
    team_2_elo_rating_eight : float
    team_1_elo_rating_seven : float
    team_2_elo_rating_seven : float

class ItalyDataInput(BaseModel):

    team_1_form_points: int
    team_2_form_points: int
    team_1_avg_shot_on_target: float
    team_2_avg_shot_on_target: float
    team_1_elo_rating: float
    team_2_elo_rating: float
    team_1_form_points_nine: float
    team_2_form_points_nine: float
    team_1_form_points_eight : float
    team_2_form_points_eight : float
    team_1_form_points_seven : float
    team_2_form_points_seven : float
    team_1_avg_shot_on_target_nine : float
    team_2_avg_shot_on_target_nine : float
    team_1_avg_shot_on_target_eight : float
    team_2_avg_shot_on_target_eight : float
    team_1_avg_shot_on_target_seven : float
    team_2_avg_shot_on_target_seven: float
    team_1_elo_rating_nine : float
    team_2_elo_rating_nine  : float
    team_1_elo_rating_eight : float
    team_2_elo_rating_eight : float
    team_1_elo_rating_seven : float
    team_2_elo_rating_seven : float

class LaligaDataInput(BaseModel):

    team_1_form_points: int
    team_2_form_points: int
    team_1_elo_rating: float
    team_2_elo_rating: float
    team_1_form_points_sin: float
    team_2_form_points_sin: float
    team_1_form_points_tan: float
    team_2_form_points_tan: float
    team_1_form_points_cos : float
    team_2_form_points_cos : float
    team_1_form_points_cos_seven : float
    team_2_form_points_cos_seven : float
    team_1_form_points_cos_nine : float
    team_2_form_points_cos_nine : float
    team_1_form_points_tan_seven : float
    team_2_form_points_tan_seven : float
    team_1_form_points_tan_nine : float
    team_2_form_points_tan_nine : float
    team_1_elo_rating_sin : float
    team_2_elo_rating_sin : float
    team_1_elo_rating_tan : float
    team_2_elo_rating_tan : float
    team_1_elo_rating_cos : float
    team_2_elo_rating_cos : float
    team_1_elo_rating_cos_seven : float
    team_2_elo_rating_cos_seven : float
    team_1_elo_rating_cos_nine : float
    team_2_elo_rating_cos_nine : float
    team_1_elo_rating_tan_seven : float
    team_2_elo_rating_tan_seven : float
    team_1_elo_rating_tan_nine : float
    team_2_elo_rating_tan_nine : float

class UpdatePoisson(BaseModel):
    name: List[dict] = []

class Team(BaseModel):
    HomeTeam: List[str]
    AwayTeam: List[str]

class LastUpdatedTeam(BaseModel):
    HomeTeam: str
    AwayTeam: str

class EloRatingID(BaseModel):
  competitor_id: str

class CompetitorData(BaseModel):
  competitor_id: str
  competition_id: str

trials = 10000

def fiveYearsBackdate():
    Previous_Date = datetime.datetime.today() - datetime.timedelta(days=5*365)
    Previous_Date_Formatted = Previous_Date.strftime ('%Y-%m-%d')
    return str(Previous_Date_Formatted)

def get_score(home, away):
    matches = pd.read_csv('poisson_data_soccer.csv')
    matches['Date'] =  pd.to_datetime(matches['Date'], infer_datetime_format=True)
    date = fiveYearsBackdate()
    matches=matches[matches["Date"]>date]
    h2h = matches.groupby(['HomeTeam', 'AwayTeam']).mean()
    try:
        # head to head results in last 5 seasons
        home_mean = h2h.loc[(home, away)][0]
        away_mean = h2h.loc[(home, away)][1]

        # simulate score by random sampling from parametrized Poisson distribution
        home_scores = poisson.rvs(home_mean, size=trials).astype(str)
        away_scores = poisson.rvs(away_mean, size=trials).astype(str)

        scores = pd.DataFrame(data={'home':home_scores, 'away':away_scores})
        scores['totalgoals'] = scores['home'].astype(int) + scores['away'].astype(int)
        scores['result'] = scores['home'] + '-' + scores['away']
        under_2_5_goals =scores[scores['totalgoals']<2.5]
        under_2_5_goals_probability = round(under_2_5_goals.count()[2] / trials * 100, 1)
        under_2_5_odds = round(100/under_2_5_goals_probability, 2)
        over_2_5_goals_probability = 100 - under_2_5_goals_probability
        over_2_5_odds = round(100/over_2_5_goals_probability, 2)
        predictions = scores['result'].value_counts()
        probability = round(predictions / trials * 100, 1)
        
        return predictions.index[0], probability[0], under_2_5_goals_probability, under_2_5_odds, over_2_5_goals_probability, over_2_5_odds

  
    # except (KeyError,IndexError, TypeError):
    #   # return NA for teams with no head to head record in last 5 seasons        
    #   return "N/A-N/A",0,0,0,0,0
    except (IndexError, TypeError):
        # return NA for teams with no head to head record in last 5 seasons        
        return "N/A-N/A",0,0,0,0,0

def get_score_1(home, away):
    matches = pd.read_csv('poisson_data_soccer.csv')
    matches['Date'] =  pd.to_datetime(matches['Date'], infer_datetime_format=True)
    date = fiveYearsBackdate()
    matches=matches[matches["Date"]>date]
    h2h = matches.groupby(['HomeTeam', 'AwayTeam']).mean()
    try:
        # head to head results in last 5 seasons
        home_mean = h2h.loc[(home, away)][0]
        away_mean = h2h.loc[(home, away)][1]

        # simulate score by random sampling from parametrized Poisson distribution
        home_scores = poisson.rvs(home_mean, size=trials).astype(str)
        away_scores = poisson.rvs(away_mean, size=trials).astype(str)

        scores = pd.DataFrame(data={'home':home_scores, 'away':away_scores})
        scores['totalgoals'] = scores['home'].astype(int) + scores['away'].astype(int)
        scores['result'] = scores['home'] + '-' + scores['away']
        under_2_5_goals =scores[scores['totalgoals']<2.5]
        under_2_5_goals_probability = round(under_2_5_goals.count()[2] / trials * 100, 1)
        under_2_5_odds = round(100/under_2_5_goals_probability, 2)
        over_2_5_goals_probability = 100 - under_2_5_goals_probability
        over_2_5_odds = round(100/over_2_5_goals_probability, 2)
        predictions = scores['result'].value_counts()
        probability = round(predictions / trials * 100, 1)
        
        return predictions.index[0], probability[0], under_2_5_goals_probability, under_2_5_odds, over_2_5_goals_probability, over_2_5_odds

  
    # except (KeyError,IndexError, TypeError):
    #   # return NA for teams with no head to head record in last 5 seasons        
    #   return "N/A-N/A",0,0,0,0,0
    except (KeyError, IndexError, TypeError):
        # return NA for teams with no head to head record in last 5 seasons        
        return "N/A-N/A",0,0,0,0,0

def get_asian_handicap(new):
    ht_handicap = []
    at_handicap = []
    try:
        ht_score = int(new[0])
        at_score = int(new[1])
        if ht_score > at_score:
            ht_handicap.extend([0,-0.25,-0.5])
            at_handicap.extend([0,0.25,0.5])
            if ht_score - at_score >= 2:
                ht_handicap.extend([-0.75,-1,-1.25,-1.5])
                at_handicap.extend([0.75,1,1.25,1.5])
            if ht_score - at_score >= 3:
                ht_handicap.extend([-1.75,-2])
                at_handicap.extend([1.75,2])
        elif at_score > ht_score:
            at_handicap.extend([0,-0.25,-0.5])
            ht_handicap.extend([0,0.25,0.5])
            if at_score - ht_score >= 2:
                at_handicap.extend([-0.75,-1,-1.25,-1.5])
                ht_handicap.extend([0.75,1,1.25,1.5])
            if at_score - ht_score >= 3:
                at_handicap.extend([-1.75,-2])
                ht_handicap.extend([1.75,2])
        else:
            ht_handicap.extend([0])
            at_handicap.extend([0,0.25,0.5,0.75,1,1.25,1.5,1.75,2])

        return ht_handicap, at_handicap
    except (TypeError, ValueError):
        return new[0], new[1]

def data_processing(DataInput):
    modified_data ={
        "team_1_form_points": DataInput.ht_form_points,
        "team_2_form_points": DataInput.at_form_points,
        "team_1_avg_shot_on_target": DataInput.ht_avg_shot_on_target,
        "team_2_avg_shot_on_target": DataInput.at_avg_shot_on_target,
        "team_1_elo_rating": DataInput.ht_elo_rating,
        "team_2_elo_rating": DataInput.at_elo_rating,
        "team_1_form_points_nine": DataInput.ht_form_points**9,
        "team_2_form_points_nine": DataInput.at_form_points**9,
        "team_1_form_points_eight": DataInput.ht_form_points**8,
        "team_2_form_points_eight": DataInput.at_form_points**8,
        "team_1_form_points_seven": DataInput.ht_form_points**7,
        "team_2_form_points_seven": DataInput.at_form_points**7,
        "team_1_avg_shot_on_target_nine": DataInput.ht_avg_shot_on_target**9,
        "team_2_avg_shot_on_target_nine": DataInput.at_avg_shot_on_target**9,
        "team_1_avg_shot_on_target_eight": DataInput.ht_avg_shot_on_target**8,
        "team_2_avg_shot_on_target_eight": DataInput.at_avg_shot_on_target**8,
        "team_1_avg_shot_on_target_seven": DataInput.ht_avg_shot_on_target**7,
        "team_2_avg_shot_on_target_seven": DataInput.at_avg_shot_on_target**7,
        "team_1_elo_rating_nine": DataInput.ht_elo_rating**9,
        "team_2_elo_rating_nine": DataInput.at_elo_rating**9,
        "team_1_elo_rating_eight": DataInput.ht_elo_rating**8,
        "team_2_elo_rating_eight": DataInput.at_elo_rating**8,
        "team_1_elo_rating_seven": DataInput.ht_elo_rating**7,
        "team_2_elo_rating_seven": DataInput.at_elo_rating**7
    }
    return modified_data

def data_processing_la_liga(DataInput):
    modified_data ={
        "team_1_form_points": DataInput.ht_form_points,
        "team_2_form_points": DataInput.at_form_points,
        "team_1_elo_rating": DataInput.ht_elo_rating,
        "team_2_elo_rating": DataInput.at_elo_rating,
        "team_1_form_points_sin":np.sin(DataInput.ht_form_points),
        "team_2_form_points_sin":np.sin(DataInput.at_form_points),
        "team_1_form_points_tan":np.tan(DataInput.ht_form_points),  
        "team_2_form_points_tan":np.tan(DataInput.ht_form_points),
        "team_1_form_points_cos":np.cos(DataInput.ht_form_points),
        "team_2_form_points_cos":np.cos(DataInput.at_form_points),
        "team_1_form_points_cos_seven":np.cos(DataInput.ht_form_points)**7,
        "team_2_form_points_cos_seven":np.cos(DataInput.at_form_points)**7,
        "team_1_form_points_cos_nine":np.cos(DataInput.ht_form_points)**9,
        "team_2_form_points_cos_nine":np.cos(DataInput.at_form_points)**9,
        "team_1_form_points_tan_seven":np.tan(DataInput.ht_form_points)**7,
        "team_2_form_points_tan_seven":np.tan(DataInput.ht_form_points)**7,
        "team_1_form_points_tan_nine":np.tan(DataInput.ht_form_points)**9,
        "team_2_form_points_tan_nine":np.tan(DataInput.ht_form_points)**9,
        "team_1_elo_rating_sin":np.sin(DataInput.ht_elo_rating),
        "team_2_elo_rating_sin":np.sin(DataInput.at_elo_rating),
        "team_1_elo_rating_tan":np.tan(DataInput.ht_elo_rating),
        "team_2_elo_rating_tan":np.tan(DataInput.at_elo_rating),
        "team_1_elo_rating_cos":np.cos(DataInput.ht_elo_rating),
        "team_2_elo_rating_cos":np.cos(DataInput.at_elo_rating),
        "team_1_elo_rating_cos_seven":np.cos(DataInput.ht_elo_rating)**7,
        "team_2_elo_rating_cos_seven":np.cos(DataInput.at_elo_rating)**7,
        "team_1_elo_rating_cos_nine":np.cos(DataInput.ht_elo_rating)**9,
        "team_2_elo_rating_cos_nine":np.cos(DataInput.at_elo_rating)**9,
        "team_1_elo_rating_tan_seven":np.tan(DataInput.ht_elo_rating)**7,
        "team_2_elo_rating_tan_seven":np.tan(DataInput.at_elo_rating)**7,
        "team_1_elo_rating_tan_nine":np.tan(DataInput.ht_elo_rating)**9,
        "team_2_elo_rating_tan_nine":np.tan(DataInput.at_elo_rating)**9
    }
    return modified_data

def read_format_df(date):
    try:
        url = "http://api.clubelo.com/"+ date
        time.sleep(5)
        df1 =pd.read_csv(url)
        df1["Date"] = date
        cols = ["Date","Club","Elo"]
        df1 = df1[cols]
        return df1
    except:
        url = "http://api.clubelo.com/"+ date
        time.sleep(5)
        df1 =pd.read_csv(url)
        df1["Date"] = date
        cols = ["Date","Club","Elo"]
        df1 = df1[cols]
        return df1

def elomaping_sportsradar_clubelo(key=None):
    todaydate=datetime.datetime.today().strftime('%Y-%m-%d')
    # print(todaydate)
    try:
        df = pd.DataFrame(sportsradar_clubelo_mapping)
        dict_arr=df.set_index('sportsradar_competitor_id').T.to_dict('dict')
        df1=read_format_df(todaydate)
        data=[]
        for key in list(dict_arr.keys()):
            try:
                linear_data = {'sportsradar_competitor_id':key,
                           'sportsradar_competitor_short_name':dict_arr[key]['sportsradar_competitor_short_name'],
                          'clubelo_team_name':dict_arr[key]['clubelo_team_name'],
                            'betfair_team_name':dict_arr[key]['betfair_team_name'],
                           'elo_rating':float(df1[df1['Club']==dict_arr[key]['clubelo_team_name']]['Elo'])}
            except:
                linear_data = {'sportsradar_competitor_id':key,
                           'sportsradar_competitor_short_name':dict_arr[key]['sportsradar_competitor_short_name'],
                          'clubelo_team_name':dict_arr[key]['clubelo_team_name'],
                            'betfair_team_name':dict_arr[key]['betfair_team_name'],
                           'elo_rating':None}
            data.append(linear_data)
        return data  
    except:
        pass

def elo_ratings_by_competition_process(competitor_id):
    todaydate=datetime.datetime.today().strftime('%Y-%m-%d')
    with open('elo_dataset.json', 'r') as f:
        team_data = json.load(f)
    if todaydate == team_data["date"]:
      for team in team_data["elo_data"]:
        if team["sportsradar_competitor_id"] == str(competitor_id):
          modified_data = team
          return {"data": modified_data}
      return {"data": None}
    else:
      elo_data = elomaping_sportsradar_clubelo()
      data1 = {
          "date": todaydate,
          "elo_data": elo_data
      }
      with open("elo_dataset.json", 'w') as f:
        f.write(json.dumps(data1, indent=2))
      for team in elo_data:
        if team["sportsradar_competitor_id"] == str(competitor_id):
          modified_data = team
          return {"data": modified_data}
      return {"data": None}

@app.post("/soccer_prediction")
async def soccer_prediction_list(data: DataInput):
    info_data = data_processing(data)
    processed_info_data = EplDataInput.parse_obj(info_data)
    received = pd.DataFrame(jsonable_encoder(processed_info_data), index=[0])
    cols_new = ['team_1_form_points', 'team_2_form_points',
       'team_1_avg_shot_on_target', 'team_2_avg_shot_on_target',
       'team_1_elo_rating', 'team_2_elo_rating', 'team_1_form_points_nine',
       'team_2_form_points_nine', 'team_1_form_points_eight',
       'team_2_form_points_eight', 'team_1_form_points_seven',
       'team_2_form_points_seven', 'team_1_avg_shot_on_target_nine',
       'team_2_avg_shot_on_target_nine', 'team_1_avg_shot_on_target_eight',
       'team_2_avg_shot_on_target_eight', 'team_1_avg_shot_on_target_seven',
       'team_2_avg_shot_on_target_seven', 'team_1_elo_rating_nine',
       'team_2_elo_rating_nine', 'team_1_elo_rating_eight',
       'team_2_elo_rating_eight', 'team_1_elo_rating_seven',
       'team_2_elo_rating_seven']
    received = received[cols_new]
    if data.competition_id == "sr:competition:17":
        pred_name = model1.predict(received)[0]
        Prob = model1.predict_proba(received) * 100
        probability_percent = {
            "away_win": round(Prob.tolist()[0][0], 2),
            "draw": round(Prob.tolist()[0][1], 2),
            "home_win": round(Prob.tolist()[0][2], 2)
        }
        decimal_odds = {
            "away_odds": round(100/Prob.tolist()[0][0], 2),
            "draw_odds": round(100/Prob.tolist()[0][1], 2),
            "home_odds": round(100/Prob.tolist()[0][2], 2)
        }
        fractional_odds = {
            "away_odds": str(Fraction(round(100/Prob.tolist()[0][0], 2) - 1).limit_denominator()),
            "draw_odds": str(Fraction(round(100/Prob.tolist()[0][1], 2) - 1).limit_denominator()),
            "home_odds": str(Fraction(round(100/Prob.tolist()[0][2], 2) - 1).limit_denominator())
        }
        american_odds = {}
        if decimal_odds["home_odds"] >= 2.00:
            american_odds["home_odds"] = round((decimal_odds["home_odds"] - 1)*100)
        else:
            try:
                american_odds["home_odds"] = round((-100)/(decimal_odds["home_odds"] - 1))
            except ZeroDivisionError:
                american_odds["home_odds"] = 0
        if decimal_odds["draw_odds"] >= 2.00:
            american_odds["draw_odds"] = round((decimal_odds["draw_odds"] - 1)*100)
        else:
            try:
                american_odds["draw_odds"] = round((-100)/(decimal_odds["draw_odds"] - 1))
            except ZeroDivisionError:
                american_odds["draw_odds"] = 0
        if decimal_odds["away_odds"] >= 2.00:
            american_odds["away_odds"] = round((decimal_odds["away_odds"] - 1)*100)
        else:
            try:
                american_odds["away_odds"] = round((-100)/(decimal_odds["away_odds"] - 1))
            except ZeroDivisionError:
                american_odds["away_odds"] = 0
        return {"prediction": pred_name,
                "probability_percent": probability_percent,
                "predicted_decimal_odds": decimal_odds,
                "predicted_fractional_odds": fractional_odds,
                "predicted_american_odds": american_odds

                }
    elif data.competition_id == "sr:competition:35":
        pred_name = model2.predict(received)[0]
        Prob = model2.predict_proba(received) * 100
        probability_percent = {
            "away_win": round(Prob.tolist()[0][0], 2),
            "draw": round(Prob.tolist()[0][1], 2),
            "home_win": round(Prob.tolist()[0][2], 2)
        }
        decimal_odds = {
            "away_odds": round(100/Prob.tolist()[0][0], 2),
            "draw_odds": round(100/Prob.tolist()[0][1], 2),
            "home_odds": round(100/Prob.tolist()[0][2], 2)
        }
        fractional_odds = {
            "away_odds": str(Fraction(round(100/Prob.tolist()[0][0], 2) - 1).limit_denominator()),
            "draw_odds": str(Fraction(round(100/Prob.tolist()[0][1], 2) - 1).limit_denominator()),
            "home_odds": str(Fraction(round(100/Prob.tolist()[0][2], 2) - 1).limit_denominator())
        }
        american_odds = {}
        if decimal_odds["home_odds"] >= 2.00:
            american_odds["home_odds"] = round((decimal_odds["home_odds"] - 1)*100)
        else:
            try:
                american_odds["home_odds"] = round((-100)/(decimal_odds["home_odds"] - 1))
            except ZeroDivisionError:
                american_odds["home_odds"] = 0
        if decimal_odds["draw_odds"] >= 2.00:
            american_odds["draw_odds"] = round((decimal_odds["draw_odds"] - 1)*100)
        else:
            try:
                american_odds["draw_odds"] = round((-100)/(decimal_odds["draw_odds"] - 1))
            except ZeroDivisionError:
                american_odds["draw_odds"] = 0
        if decimal_odds["away_odds"] >= 2.00:
            american_odds["away_odds"] = round((decimal_odds["away_odds"] - 1)*100)
        else:
            try:
                american_odds["away_odds"] = round((-100)/(decimal_odds["away_odds"] - 1))
            except ZeroDivisionError:
                american_odds["away_odds"] = 0
        return {"prediction": pred_name,
                "probability_percent": probability_percent,
                "predicted_decimal_odds": decimal_odds,
                "predicted_fractional_odds": fractional_odds,
                "predicted_american_odds": american_odds

                }
    elif data.competition_id == "sr:competition:34":
        pred_name = model4.predict(received)[0]
        Prob = model4.predict_proba(received) * 100
        probability_percent = {
            "away_win": round(Prob.tolist()[0][0], 2),
            "draw": round(Prob.tolist()[0][1], 2),
            "home_win": round(Prob.tolist()[0][2], 2)
        }
        decimal_odds = {
            "away_odds": round(100/Prob.tolist()[0][0], 2),
            "draw_odds": round(100/Prob.tolist()[0][1], 2),
            "home_odds": round(100/Prob.tolist()[0][2], 2)
        }
        fractional_odds = {
            "away_odds": str(Fraction(round(100/Prob.tolist()[0][0], 2) - 1).limit_denominator()),
            "draw_odds": str(Fraction(round(100/Prob.tolist()[0][1], 2) - 1).limit_denominator()),
            "home_odds": str(Fraction(round(100/Prob.tolist()[0][2], 2) - 1).limit_denominator())
        }
        american_odds = {}
        if decimal_odds["home_odds"] >= 2.00:
            american_odds["home_odds"] = round((decimal_odds["home_odds"] - 1)*100)
        else:
            try:
                american_odds["home_odds"] = round((-100)/(decimal_odds["home_odds"] - 1))
            except ZeroDivisionError:
                american_odds["home_odds"] = 0
        if decimal_odds["draw_odds"] >= 2.00:
            american_odds["draw_odds"] = round((decimal_odds["draw_odds"] - 1)*100)
        else:
            try:
                american_odds["draw_odds"] = round((-100)/(decimal_odds["draw_odds"] - 1))
            except ZeroDivisionError:
                american_odds["draw_odds"] = 0
        if decimal_odds["away_odds"] >= 2.00:
            american_odds["away_odds"] = round((decimal_odds["away_odds"] - 1)*100)
        else:
            try:
                american_odds["away_odds"] = round((-100)/(decimal_odds["away_odds"] - 1))
            except ZeroDivisionError:
                american_odds["away_odds"] = 0
        return {"prediction": pred_name,
                "probability_percent": probability_percent,
                "predicted_decimal_odds": decimal_odds,
                "predicted_fractional_odds": fractional_odds,
                "predicted_american_odds": american_odds

                }
    elif data.competition_id == "sr:competition:23":
        pred_name = model3.predict(received)[0]
        Prob = model3.predict_proba(received) * 100
        probability_percent = {
            "away_win": round(Prob.tolist()[0][0], 2),
            "draw": round(Prob.tolist()[0][1], 2),
            "home_win": round(Prob.tolist()[0][2], 2)
        }
        decimal_odds = {
            "away_odds": round(100/Prob.tolist()[0][0], 2),
            "draw_odds": round(100/Prob.tolist()[0][1], 2),
            "home_odds": round(100/Prob.tolist()[0][2], 2)
        }
        fractional_odds = {
            "away_odds": str(Fraction(round(100/Prob.tolist()[0][0], 2) - 1).limit_denominator()),
            "draw_odds": str(Fraction(round(100/Prob.tolist()[0][1], 2) - 1).limit_denominator()),
            "home_odds": str(Fraction(round(100/Prob.tolist()[0][2], 2) - 1).limit_denominator())
        }
        american_odds = {}
        if decimal_odds["home_odds"] >= 2.00:
            american_odds["home_odds"] = round((decimal_odds["home_odds"] - 1)*100)
        else:
            try:
                american_odds["home_odds"] = round((-100)/(decimal_odds["home_odds"] - 1))
            except ZeroDivisionError:
                american_odds["home_odds"] = 0
        if decimal_odds["draw_odds"] >= 2.00:
            american_odds["draw_odds"] = round((decimal_odds["draw_odds"] - 1)*100)
        else:
            try:
                american_odds["draw_odds"] = round((-100)/(decimal_odds["draw_odds"] - 1))
            except ZeroDivisionError:
                american_odds["draw_odds"] = 0
        if decimal_odds["away_odds"] >= 2.00:
            american_odds["away_odds"] = round((decimal_odds["away_odds"] - 1)*100)
        else:
            try:
                american_odds["away_odds"] = round((-100)/(decimal_odds["away_odds"] - 1))
            except ZeroDivisionError:
                american_odds["away_odds"] = 0
        return {"prediction": pred_name,
                "probability_percent": probability_percent,
                "predicted_decimal_odds": decimal_odds,
                "predicted_fractional_odds": fractional_odds,
                "predicted_american_odds": american_odds

                }
    else:
      info_data = data_processing_la_liga(data)
      processed_info_data = LaligaDataInput.parse_obj(info_data)
      received = pd.DataFrame(jsonable_encoder(processed_info_data), index=[0])
      cols_new = ['team_1_form_points', 'team_2_form_points', 'team_1_elo_rating',
         'team_2_elo_rating', 'team_1_form_points_sin', 'team_2_form_points_sin',
         'team_1_form_points_tan', 'team_2_form_points_tan',
         'team_1_form_points_cos', 'team_2_form_points_cos',
         'team_1_form_points_cos_seven', 'team_2_form_points_cos_seven',
         'team_1_form_points_cos_nine', 'team_2_form_points_cos_nine',
         'team_1_form_points_tan_seven', 'team_2_form_points_tan_seven',
         'team_1_form_points_tan_nine', 'team_2_form_points_tan_nine',
         'team_1_elo_rating_sin', 'team_2_elo_rating_sin',
         'team_1_elo_rating_tan', 'team_2_elo_rating_tan',
         'team_1_elo_rating_cos', 'team_2_elo_rating_cos',
         'team_1_elo_rating_cos_seven', 'team_2_elo_rating_cos_seven',
         'team_1_elo_rating_cos_nine', 'team_2_elo_rating_cos_nine',
         'team_1_elo_rating_tan_seven', 'team_2_elo_rating_tan_seven',
         'team_1_elo_rating_tan_nine', 'team_2_elo_rating_tan_nine']
      received = received[cols_new]
      pred_name = model5.predict(received)[0]
      Prob = model5.predict_proba(received) * 100
      probability_percent = {
          "away_win": round(Prob.tolist()[0][0], 2),
          "draw": round(Prob.tolist()[0][1], 2),
          "home_win": round(Prob.tolist()[0][2], 2)
      }
      decimal_odds = {
            "away_odds": round(100/Prob.tolist()[0][0], 2),
            "draw_odds": round(100/Prob.tolist()[0][1], 2),
            "home_odds": round(100/Prob.tolist()[0][2], 2)
      }
      fractional_odds = {
            "away_odds": str(Fraction(round(100/Prob.tolist()[0][0], 2) - 1).limit_denominator()),
            "draw_odds": str(Fraction(round(100/Prob.tolist()[0][1], 2) - 1).limit_denominator()),
            "home_odds": str(Fraction(round(100/Prob.tolist()[0][2], 2) - 1).limit_denominator())
      }
      american_odds = {}
      if decimal_odds["home_odds"] >= 2.00:
        american_odds["home_odds"] = round((decimal_odds["home_odds"] - 1)*100)
      else:
        try:
          american_odds["home_odds"] = round((-100)/(decimal_odds["home_odds"] - 1))
        except ZeroDivisionError:
          american_odds["home_odds"] = 0
      if decimal_odds["draw_odds"] >= 2.00:
        american_odds["draw_odds"] = round((decimal_odds["draw_odds"] - 1)*100)
      else:
        try:
          american_odds["draw_odds"] = round((-100)/(decimal_odds["draw_odds"] - 1))
        except ZeroDivisionError:
          american_odds["draw_odds"] = 0
      if decimal_odds["away_odds"] >= 2.00:
        american_odds["away_odds"] = round((decimal_odds["away_odds"] - 1)*100)
      else:
        try:
          american_odds["away_odds"] = round((-100)/(decimal_odds["away_odds"] - 1))
        except ZeroDivisionError:
          american_odds["away_odds"] = 0
      return {"prediction": pred_name,
      "probability_percent": probability_percent,
      "predicted_decimal_odds": decimal_odds,
      "predicted_fractional_odds": fractional_odds,
      "predicted_american_odds": american_odds
      }

@app.post("/Germany_Bundesliga")
async def Germany_Bundesliga(data: DataInput):
    info_data = data_processing(data)
    processed_info_data = GermanyDataInput.parse_obj(info_data)
    received = pd.DataFrame(jsonable_encoder(processed_info_data), index=[0])
    cols_new = ['team_1_form_points', 'team_2_form_points',
       'team_1_avg_shot_on_target', 'team_2_avg_shot_on_target',
       'team_1_elo_rating', 'team_2_elo_rating', 'team_1_form_points_nine',
       'team_2_form_points_nine', 'team_1_form_points_eight',
       'team_2_form_points_eight', 'team_1_form_points_seven',
       'team_2_form_points_seven', 'team_1_avg_shot_on_target_nine',
       'team_2_avg_shot_on_target_nine', 'team_1_avg_shot_on_target_eight',
       'team_2_avg_shot_on_target_eight', 'team_1_avg_shot_on_target_seven',
       'team_2_avg_shot_on_target_seven', 'team_1_elo_rating_nine',
       'team_2_elo_rating_nine', 'team_1_elo_rating_eight',
       'team_2_elo_rating_eight', 'team_1_elo_rating_seven',
       'team_2_elo_rating_seven']
    received = received[cols_new]
    pred_name = model2.predict(received)[0]
    Prob = model2.predict_proba(received) * 100
    probability_percent = {
        "away_win": round(Prob.tolist()[0][0], 2),
        "draw": round(Prob.tolist()[0][1], 2),
        "home_win": round(Prob.tolist()[0][2], 2)
    }
    decimal_odds = {
        "away_odds": round(100/Prob.tolist()[0][0], 2),
        "draw_odds": round(100/Prob.tolist()[0][1], 2),
        "home_odds": round(100/Prob.tolist()[0][2], 2)
    }
    fractional_odds = {
        "away_odds": str(Fraction(round(100/Prob.tolist()[0][0], 2) - 1).limit_denominator()),
        "draw_odds": str(Fraction(round(100/Prob.tolist()[0][1], 2) - 1).limit_denominator()),
        "home_odds": str(Fraction(round(100/Prob.tolist()[0][2], 2) - 1).limit_denominator())
    }
    american_odds = {}
    if decimal_odds["home_odds"] >= 2.00:
        american_odds["home_odds"] = round((decimal_odds["home_odds"] - 1)*100)
    else:
        try:
            american_odds["home_odds"] = round((-100)/(decimal_odds["home_odds"] - 1))
        except ZeroDivisionError:
            american_odds["home_odds"] = 0
    if decimal_odds["draw_odds"] >= 2.00:
        american_odds["draw_odds"] = round((decimal_odds["draw_odds"] - 1)*100)
    else:
        try:
            american_odds["draw_odds"] = round((-100)/(decimal_odds["draw_odds"] - 1))
        except ZeroDivisionError:
            american_odds["draw_odds"] = 0
    if decimal_odds["away_odds"] >= 2.00:
        american_odds["away_odds"] = round((decimal_odds["away_odds"] - 1)*100)
    else:
        try:
            american_odds["away_odds"] = round((-100)/(decimal_odds["away_odds"] - 1))
        except ZeroDivisionError:
            american_odds["away_odds"] = 0
    
    
    return {'prediction': pred_name,
			'probability_percent': probability_percent,
			"predicted_decimal_odds": decimal_odds,
			"predicted_fractional_odds": fractional_odds,
			"predicted_american_odds": american_odds

			}
    
@app.post("/Italy_series")
async def Italy_series_A(data: DataInput):
    
    info_data = data_processing(data)
    processed_info_data = ItalyDataInput.parse_obj(info_data)
    received = pd.DataFrame(jsonable_encoder(processed_info_data), index=[0])
    cols_new = ['team_1_form_points', 'team_2_form_points',
       'team_1_avg_shot_on_target', 'team_2_avg_shot_on_target',
       'team_1_elo_rating', 'team_2_elo_rating', 'team_1_form_points_nine',
       'team_2_form_points_nine', 'team_1_form_points_eight',
       'team_2_form_points_eight', 'team_1_form_points_seven',
       'team_2_form_points_seven', 'team_1_avg_shot_on_target_nine',
       'team_2_avg_shot_on_target_nine', 'team_1_avg_shot_on_target_eight',
       'team_2_avg_shot_on_target_eight', 'team_1_avg_shot_on_target_seven',
       'team_2_avg_shot_on_target_seven', 'team_1_elo_rating_nine',
       'team_2_elo_rating_nine', 'team_1_elo_rating_eight',
       'team_2_elo_rating_eight', 'team_1_elo_rating_seven',
       'team_2_elo_rating_seven']
    received = received[cols_new]
    pred_name = model3.predict(received)[0]
    Prob = model3.predict_proba(received) * 100
    probability_percent = {
        "away_win": round(Prob.tolist()[0][0], 2),
        "draw": round(Prob.tolist()[0][1], 2),
        "home_win": round(Prob.tolist()[0][2], 2)
    }
    decimal_odds = {
        "away_odds": round(100/Prob.tolist()[0][0], 2),
        "draw_odds": round(100/Prob.tolist()[0][1], 2),
        "home_odds": round(100/Prob.tolist()[0][2], 2)
    }
    fractional_odds = {
        "away_odds": str(Fraction(round(100/Prob.tolist()[0][0], 2) - 1).limit_denominator()),
        "draw_odds": str(Fraction(round(100/Prob.tolist()[0][1], 2) - 1).limit_denominator()),
        "home_odds": str(Fraction(round(100/Prob.tolist()[0][2], 2) - 1).limit_denominator())
    }
    american_odds = {}
    if decimal_odds["home_odds"] >= 2.00:
        american_odds["home_odds"] = round((decimal_odds["home_odds"] - 1)*100)
    else:
        try:
            american_odds["home_odds"] = round((-100)/(decimal_odds["home_odds"] - 1))
        except ZeroDivisionError:
            american_odds["home_odds"] = 0
    if decimal_odds["draw_odds"] >= 2.00:
        american_odds["draw_odds"] = round((decimal_odds["draw_odds"] - 1)*100)
    else:
        try:
            american_odds["draw_odds"] = round((-100)/(decimal_odds["draw_odds"] - 1))
        except ZeroDivisionError:
            american_odds["draw_odds"] = 0
    if decimal_odds["away_odds"] >= 2.00:
        american_odds["away_odds"] = round((decimal_odds["away_odds"] - 1)*100)
    else:
        try:
            american_odds["away_odds"] = round((-100)/(decimal_odds["away_odds"] - 1))
        except ZeroDivisionError:
            american_odds["away_odds"] = 0
    
    
    return {'prediction': pred_name,
			'probability_percent': probability_percent,
			"predicted_decimal_odds": decimal_odds,
			"predicted_fractional_odds": fractional_odds,
			"predicted_american_odds": american_odds

			}
    

@app.post("/France_ligue")
async def France_ligue_1(data: DataInput):
    info_data = data_processing(data)
    processed_info_data = FranceDataInput.parse_obj(info_data)
    received = pd.DataFrame(jsonable_encoder(processed_info_data), index=[0])
    cols_new = ['team_1_form_points', 'team_2_form_points',
       'team_1_avg_shot_on_target', 'team_2_avg_shot_on_target',
       'team_1_elo_rating', 'team_2_elo_rating', 'team_1_form_points_nine',
       'team_2_form_points_nine', 'team_1_form_points_eight',
       'team_2_form_points_eight', 'team_1_form_points_seven',
       'team_2_form_points_seven', 'team_1_avg_shot_on_target_nine',
       'team_2_avg_shot_on_target_nine', 'team_1_avg_shot_on_target_eight',
       'team_2_avg_shot_on_target_eight', 'team_1_avg_shot_on_target_seven',
       'team_2_avg_shot_on_target_seven', 'team_1_elo_rating_nine',
       'team_2_elo_rating_nine', 'team_1_elo_rating_eight',
       'team_2_elo_rating_eight', 'team_1_elo_rating_seven',
       'team_2_elo_rating_seven']
    received = received[cols_new]
    pred_name = model4.predict(received)[0]
    Prob = model4.predict_proba(received) * 100
    probability_percent = {
        "away_win": round(Prob.tolist()[0][0], 2),
        "draw": round(Prob.tolist()[0][1], 2),
        "home_win": round(Prob.tolist()[0][2], 2)
    }
    decimal_odds = {
        "away_odds": round(100/Prob.tolist()[0][0], 2),
        "draw_odds": round(100/Prob.tolist()[0][1], 2),
        "home_odds": round(100/Prob.tolist()[0][2], 2)
    }
    fractional_odds = {
        "away_odds": str(Fraction(round(100/Prob.tolist()[0][0], 2) - 1).limit_denominator()),
        "draw_odds": str(Fraction(round(100/Prob.tolist()[0][1], 2) - 1).limit_denominator()),
        "home_odds": str(Fraction(round(100/Prob.tolist()[0][2], 2) - 1).limit_denominator())
    }
    american_odds = {}
    if decimal_odds["home_odds"] >= 2.00:
        american_odds["home_odds"] = round((decimal_odds["home_odds"] - 1)*100)
    else:
        try:
            american_odds["home_odds"] = round((-100)/(decimal_odds["home_odds"] - 1))
        except ZeroDivisionError:
            american_odds["home_odds"] = 0
    if decimal_odds["draw_odds"] >= 2.00:
        american_odds["draw_odds"] = round((decimal_odds["draw_odds"] - 1)*100)
    else:
        try:
            american_odds["draw_odds"] = round((-100)/(decimal_odds["draw_odds"] - 1))
        except ZeroDivisionError:
            american_odds["draw_odds"] = 0
    if decimal_odds["away_odds"] >= 2.00:
        american_odds["away_odds"] = round((decimal_odds["away_odds"] - 1)*100)
    else:
        try:
            american_odds["away_odds"] = round((-100)/(decimal_odds["away_odds"] - 1))
        except ZeroDivisionError:
            american_odds["away_odds"] = 0
    
    
    return {'prediction': pred_name,
			'probability_percent': probability_percent,
			"predicted_decimal_odds": decimal_odds,
			"predicted_fractional_odds": fractional_odds,
			"predicted_american_odds": american_odds

			}
   
@app.post('/poisson_prediction')
def get_poisson_prediction(data: Team):
    home_teams = data.HomeTeam
    away_teams = data.AwayTeam
    for team in teams:
        if home_teams == [team["name"]]:
            home_teams = [str(team["dbname"])]
        if away_teams == [team["name"]]:
            away_teams =[str(team["dbname"])]

    if len(home_teams)==len(away_teams):
        try:
            week1 = pd.DataFrame(data={'Home':home_teams, 'Away':away_teams})
            week1['data'] = week1.apply(lambda x: get_score(x.Home, x.Away), axis=1)
            week1['Predictions'] = week1['data'].values[0][0]
            new = week1['Predictions'].str.split("-", n = 1, expand = True)
            week1['Home_score'] = new[0]
            week1['Away_score'] = new[1]
            week1['Probability'] = week1['data'].values[0][1]
            week1['under_2_5_goals_probability'] = week1['data'].values[0][2]
            week1['under_2_5_odds'] = week1['data'].values[0][3]
            week1['over_2_5_goals_probability'] = week1['data'].values[0][4]
            week1['over_2_5_odds'] = week1['data'].values[0][5]
            ht_handicap,at_handicap = get_asian_handicap(new)
            week1['home_handicap'] = ' '.join(map(str, ht_handicap))
            week1['away_handicap'] = ' '.join(map(str, at_handicap))
            week1.drop("data", axis=1, inplace=True)

        # return Response(content = week1.to_json(orient = 'records'))
            return json.loads(week1.to_json(orient = 'records'))
        except KeyError:
            week1 = pd.DataFrame(data={'Home':home_teams, 'Away':away_teams})
            week1['data'] = week1.apply(lambda x: get_score_1(x.Away, x.Home), axis=1)
            week1['Predictions'] = week1['data'].values[0][0]
            new = week1['Predictions'].str.split("-", n = 1, expand = True)
            week1['Home_score'] = new[1]
            week1['Away_score'] = new[0]
            week1['Predictions'] = week1['Home_score'] + "-" + week1['Away_score']
            week1['Probability'] = week1['data'].values[0][1]
            week1['under_2_5_goals_probability'] = week1['data'].values[0][2]
            week1['under_2_5_odds'] = week1['data'].values[0][3]
            week1['over_2_5_goals_probability'] = week1['data'].values[0][4]
            week1['over_2_5_odds'] = week1['data'].values[0][5]
            ht_handicap,at_handicap = get_asian_handicap(new)
            week1['home_handicap'] = ' '.join(map(str, ht_handicap))
            week1['away_handicap'] = ' '.join(map(str, at_handicap))
            week1.drop("data", axis=1, inplace=True)

        # return Response(content = week1.to_json(orient = 'records'))
            return json.loads(week1.to_json(orient = 'records'))
        except IndexError:
            return {"no results available"}
    else:
        return {"no results available"}

col1 = ["Date","HomeTeam","AwayTeam","FTHG","FTAG"]

@app.post("/uploadcsv_poisson/")
def upload_csv(data_file: UploadString):
    counter = 0
    if validators.url(data_file.Url):
        df = pd.read_csv(data_file.Url)
        col2 = df.columns.values.tolist()
        for ele in col1:
            if ele in col2:
                counter += 1
            else:
                return {
                "status": 406,
                "message": "csv file link has not distinct columns that are similar to the train dataset; please send required csv file link with valid columns",
                "required_columns": col1
                }
        if counter == len(col1):
            df = df[col1]
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values(by="Date")
            train_df = pd.read_csv('poisson_data_soccer.csv')
            merge_df = pd.concat([train_df,df])
            merge_df = merge_df.sort_values(by="Date")
            merge_df.to_csv('poisson_data_soccer.csv',index=False)
            return {
                "status": 200,
                "message": "csv file is uploaded successfully",
                "filename": data_file.Url,
                "filelength": len(df)
                }
        else:
            return {
                "status": 406,
                "message": "csv file link has not distinct columns that are similar to the train dataset; please send required csv file link with valid columns",
                "required_columns": col1
                }

    else:
        return {
            "status": 406,
            "message": "valid csv file link is not uploaded; please send required csv file link"
        }


        

@app.post("/updatepoisson/")
def updatePoisson(data: UpdatePoisson):
    df = pd.DataFrame(data.name)
    df.date = pd.to_datetime(df.date)
    df.drop_duplicates(inplace=True)
    df.rename(columns = {"team1_name":"HomeTeam", "team2_name":"AwayTeam","country":"Country", "league_name":"League","date":"Date"}, inplace = True)
    cols = ["Date","HomeTeam","AwayTeam","FTHG","FTAG"]
    df = df[cols]
    for index, row in df.iterrows():
        for team in teams:
            if row["HomeTeam"] == team["name"]:
                df.at[index, 'HomeTeam'] = str(team["dbname"])
            if row["AwayTeam"] == team["name"]:
                df.at[index, 'AwayTeam'] = str(team["dbname"])

    df = df.sort_values(by='Date')
    df.reset_index(drop=True, inplace=True)
    hdf = pd.read_csv('poisson_data_soccer.csv')
    hdf.Date = pd.to_datetime(hdf.Date)
    hdf = pd.concat([hdf,df], ignore_index=True)
    hdf = hdf.sort_values(by='Date')
    if hdf.duplicated().sum()==0:
        hdf.to_csv('poisson_data_soccer.csv',index=False)
    else:
        hdf.drop_duplicates(inplace=True)
        hdf.to_csv('poisson_data_soccer.csv',index=False)
    return {'msg': 'success'}



@app.get("/sortpoisson/")
def sort_poisson():
    hdf = pd.read_csv('poisson_data_soccer.csv')
    hdf.Date = pd.to_datetime(hdf.Date)
    hdf = hdf.sort_values(by='Date')
    hdf.to_csv('poisson_data_soccer.csv',index=False)
    return {'msg': 'success'}


@app.post("/lastupdateddate/")
def last_updated_date(data: LastUpdatedTeam):
    home_team = data.HomeTeam
    away_team = data.AwayTeam
    for team in teams:
        if home_team == team["name"]:
            home_team = str(team["dbname"])
        if away_team == team["name"]:
            away_team =str(team["dbname"])

    hdf = pd.read_csv('poisson_data_soccer.csv')
    hdf = hdf[(hdf["HomeTeam"]==home_team)&(hdf["AwayTeam"]==away_team)]
    if len(hdf)==0:
        return {"last_updated_date": "Not Found","HomeTeam": home_team,"AwayTeam": away_team}
    else:
        last_date=hdf.tail(1).Date.values[0]
        return {"last_updated_date": last_date,"HomeTeam": home_team,"AwayTeam": away_team}


@app.get("/elo_rating_data/")
def elo_ratings():
    todaydate=datetime.datetime.today().strftime('%Y-%m-%d')
    with open('elo_dataset.json', 'r') as f:
        team_data = json.load(f)
    if todaydate == team_data["date"]:
        return {"data": team_data["elo_data"]}
    else:
        elo_data = elomaping_sportsradar_clubelo()
        data = {
            "date": todaydate,
            "elo_data": elo_data
        }
        with open("elo_dataset.json", 'w') as f:
            f.write(json.dumps(data, indent=2))
        return {"data": elo_data}

@app.post("/elo_rating_data/")
def elo_ratings_by_competition(data: EloRatingID):
    todaydate=datetime.today().strftime('%Y-%m-%d')
    with open('elo_dataset.json', 'r') as f:
        team_data = json.load(f)
    if todaydate == team_data["date"]:
      for team in team_data["elo_data"]:
        if team["sportsradar_competitor_id"] == data.competitor_id:
          modified_data = team
          return {"data": modified_data}
      return {"data": None}
    else:
      elo_data = elomaping_sportsradar_clubelo()
      data1 = {
          "date": todaydate,
          "elo_data": elo_data
      }
      with open("elo_dataset.json", 'w') as f:
        f.write(json.dumps(data1, indent=2))
      for team in elo_data:
        if team["sportsradar_competitor_id"] == data.competitor_id:
          modified_data = team
          return {"data": modified_data}
      return {"data": None}

@app.post("/team_data/")
def team_data1(team: CompetitorData):
    # print(team)
    url =  'https://aisportstrading.com:8000/api/GetTeamByCompitationIdSportsradar'
    # url = "https://api.sportradar.com/soccer/production/v4/en/competitors/"+str(team.competitor_id)+"/summaries.json?api_key=58a5hbhysexwsv3nw9r9kffz"
    print(team)
    payload2 = json.dumps({"competitor_id":team.competitor_id,"competition_id":team.competition_id})
    headers2 = {'Content-Type': 'application/json'}
    response2 = requests.request("POST", url, headers=headers2, data=payload2, verify=False)
    res =json.dumps(json.loads(response2.text))
    rec = json.loads(res)
    response_data=rec['data'][0]
    teamDataArr = json.loads(response_data['team_data'])
    # print(teamDataArr["summaries"])
    # return (teamDataArr)
    # print(response.json())
    elo_data = elo_ratings_by_competition_process(str(team.competitor_id))
    elo_data = elo_data["data"]
    # data = response.json()
    sot_value=[]
    formpoint_value=[]
    if 'summaries' in teamDataArr:
      for info in teamDataArr["summaries"]:
          if info["sport_event"]["sport_event_context"]["competition"]["id"] == str(team.competition_id):
              try:
                  if info["sport_event_status"]["winner_id"] == str(team.competitor_id):
                      formpoint_value.append(3)
                  elif info["sport_event_status"]["winner_id"] != str(team.competitor_id):
                      formpoint_value.append(0)
              except:
                  formpoint_value.append(1)
              for info1 in info["statistics"]["totals"]["competitors"]:
                  try:
                      if info1["id"]==str(team.competitor_id):
                         sot_value.append(info1["statistics"]["shots_on_target"])
                  except:
                      sot_value.append(0)
          if len(formpoint_value) == 5 and len(sot_value) == 5:
              break
    return {
        'form_points':sum(formpoint_value),
        'avg_shot_on_target':round((sum(sot_value)/len(sot_value)),2),
        'elo_rating': float(elo_data["elo_rating"])
        
    }
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from datetime import datetime
# from auditlog.models import AuditlogHistoryField
# from auditlog.registry import auditlog
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.postgres import fields

class Users(AbstractUser):
    postal_code = models.IntegerField(blank=True, null=True)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='images/',blank=True, null=True)
    is_verifed_email = models.BooleanField(default=False,verbose_name = "mail_verifed")
    email_notification = models.BooleanField(default=False)
    sms_notification = models.BooleanField(default=False)
    whatsapp_notification = models.BooleanField(default=False)
    phone_notification = models.BooleanField(default=False)
    site_notification = models.BooleanField(default=False)

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []


    class Meta:
        db_table = 'auth_user'
        verbose_name = "User Manager"
        verbose_name_plural = "User Manager"

class AffiliateUser(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=199, blank=True, null=True)
    confirm_password = models.CharField(max_length=199, blank=True, null=True)
    is_active = models.BooleanField(default=False,blank=True,null=True,verbose_name='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def clean(self):
    #     if self.password != self.confirm_password:
    #         raise ValidationError("password must be same")

    class Meta:
        db_table = "affiliate_user"
        verbose_name = "Affiliate Manager"
        verbose_name_plural = "Affiliate Manager"

class Contactus(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True)
    message = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'contactus'

class Blogs(models.Model):
    class Meta:
        db_table = 'Blog'
        verbose_name = "News"
        verbose_name_plural = "News"

    # enum_choices=(
    #     ('y', 'y'),
    #     ('n', 'n')
    # )
    
    title = models.CharField(max_length=255, default='')
    slug = models.CharField(max_length=255, default='')
    description = models.TextField(null=True)
    meta_title = models.TextField(null=True)
    meta_key = models.TextField(null=True)
    meta_description = models.TextField(null=True)
    # ispublished = models.CharField(max_length=2,choices=enum_choices, default='y')
    # isblocked = models.CharField(max_length=2,choices=enum_choices, default='n')
    # isdeleted = models.CharField(max_length=2,choices=enum_choices, default='n')
    is_published = models.BooleanField(default=True, null=True, blank=True,verbose_name = "Published")
    is_blocked = models.BooleanField(default=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserSubscriptionPayment(models.Model):
    id= models.CharField(max_length=512, default='',primary_key=True)
    subscription_id = models.IntegerField(blank=True, null=True)
    user_id = models.CharField(max_length=512,blank=True, null=True)
    username = models.CharField(max_length=512,blank=True, null=True)
    transaction_id = models.CharField(max_length=512,blank=True, null=True)
    payment_status = models.CharField(max_length=512,blank=True, null=True)
    currency_code = models.CharField(max_length=512,blank=True, null=True)
    amount = models.CharField(max_length=512,blank=True, null=True)
    payee_email = models.CharField(max_length=512,blank=True, null=True)
    merchant_id= models.CharField(max_length=512,blank=True, null=True)
    shipping_name = models.CharField(max_length=512,blank=True, null=True)
    shipping_address=models.TextField(null=True)
    payment_capture_id= models.CharField(max_length=512,blank=True, null=True)
    payer_email = models.CharField(max_length=512,blank=True, null=True)
    payer_id = models.CharField(max_length=512,blank=True, null=True)
    shiping_status = models.CharField(max_length=512,blank=True, null=True)
    date_of_payment = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    dump_response = models.TextField(null=True)
   

    class Meta:
        db_table = 'user_subscription'
        verbose_name = "Subscriptions"
        verbose_name_plural = "Subscriptions"

class Subscriptions(models.Model):
    name = models.CharField(max_length=199,blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(default=False,verbose_name='Active')
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'subscriptions'
        verbose_name = "Subscription Manager"
        verbose_name_plural = "Subscription"

class EventType(models.Model):

    eventtype_id= models.BigIntegerField(blank=True, null=True)
    eventtype_name=models.TextField(null=True)
    market_count =models.TextField(null=True)
    class Meta:
        db_table = 'event_type'

class EventType2(models.Model):

    eventtype2_id= models.BigIntegerField(blank=True, null=True)
    eventtype2_name=models.TextField(null=True)
    market_count2 =models.TextField(null=True)
    class Meta:
        db_table = 'event_type2'

class Events(models.Model):
    competition_id = models.BigIntegerField(blank=True, null=True)
    events_id = models.BigIntegerField(blank=True, null=False)
    events_name = models.TextField(null=True)
    events_countrycode = models.TextField(null=True)
    events_timezone = models.TextField(null=True)
    events_opendate = models.DateTimeField(null=True)
    market_counts = models.TextField(null=True)

    class Meta:
        db_table = 'events'

class MarketInformation(models.Model):
    market_id = models.CharField(max_length=191, blank=True, null=False)
    market_name = models.TextField(null=True)
    market_starttime = models.DateTimeField(null=True)
    total_matched = models.TextField(null=True)
    runners = models.TextField(null=True, blank=True)
    eventtype_id = models.BigIntegerField(blank=True, null=True)
    eventtype_name = models.TextField(null=True)
    competition_id = models.BigIntegerField(blank=True, null=True)
    competition_name = models.TextField(null=True)
    event_id = models.BigIntegerField(blank=True, null=True)
    event_name = models.TextField(null=True)
    event_countrycode = models.TextField(null=True)
    event_timezone = models.TextField(null=True)
    event_opendate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'market_information'

class MarketCatelog(models.Model):
    market_id = models.CharField(max_length=191,primary_key=True)
    market_name = models.TextField(null=True)
    market_start_time = models.DateTimeField(null=True)
    inplay = models.BooleanField(default=False)
    status = models.CharField(max_length=191, blank=True, null=False)
    competition_id = models.BigIntegerField(blank=True, null=True)
    event_id = models.BigIntegerField(blank=True, null=True)
    total_matched = models.CharField(max_length=191, blank=True, null=False)
    market_runner_details= models.TextField(null=True)
    runners = models.TextField(null=True, blank=True)
    
    Probability=models.CharField(max_length=255, default='')
    under_2_5_goals_probability=models.CharField(max_length=255, default='')
    under_2_5_odds=models.CharField(max_length=255, default='')
    over_2_5_goals_probability=models.CharField(max_length=255, default='')
    over_2_5_odds=models.CharField(max_length=255, default='')
    home_handicap=models.CharField(max_length=255, default='')
    away_handicap=models.CharField(max_length=255, default='')
    poision_prediction = models.CharField(max_length=255, default='')
    prediction = models.CharField(max_length=255, default='')
    probability_percent_away_win=models.CharField(max_length=255, default='')
    probability_percent_draw=models.CharField(max_length=255, default='')
    probability_percent_home_win=models.CharField(max_length=255, default='')
    predicted_decimal_odds_away_odds=models.CharField(max_length=255, default='')
    predicted_decimal_odds_draw_odds=models.CharField(max_length=255, default='')
    predicted_decimal_odds_home_odds=models.CharField(max_length=255, default='')
    predicted_fractional_odds_away_odds=models.CharField(max_length=255, default='')
    predicted_fractional_odds_draw_odds=models.CharField(max_length=255, default='')
    predicted_fractional_odds_home_odds=models.CharField(max_length=255, default='')
    predicted_american_odds_away_odds=models.CharField(max_length=255, default='')
    predicted_american_odds_draw_odds=models.CharField(max_length=255, default='')
    predicted_american_odds_home_odds=models.CharField(max_length=255, default='')
    ht_form_point=models.CharField(max_length=255, default='')
    at_form_point=models.CharField(max_length=255, default='')
    AVG_HST=models.CharField(max_length=255, default='')
    AVG_AST=models.CharField(max_length=255, default='')
    HTEloRatings=models.CharField(max_length=255, default='')
    ATEloRatings=models.CharField(max_length=255, default='')

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        db_table = 'market_catelog'

class HorseRacing(models.Model):
    market_id = models.CharField(max_length=191, blank=True, null=False)
    market_name = models.TextField(null=True)
    market_starttime = models.DateTimeField(null=True)
    total_matched = models.TextField(null=True)
    runners = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'hourse_racing'

class FootballCompetitions(models.Model):
    competition_id = models.BigIntegerField(blank=True, null=True)
    competition_name = models.TextField(null=True)
    market_count = models.TextField(null=True)
    competition_region = models.TextField(null=True)
    is_active= models.BooleanField(default=False,null=True,blank=True)

    class Meta:
        db_table = "football_competitions"

class PlaceOrdersBetfair(models.Model):
    status = models.TextField(blank=True, null=True)
    bet_id = models.TextField(blank=True, null=True)
    average_price_matched = models.TextField(blank=True, null=True)
    errorcode = models.TextField(blank=True, null=True)
    market_id = models.CharField(max_length=191, blank=True, null=True)
    selection_id = models.CharField(max_length=191, blank=True, null=True)
    price = models.CharField(max_length=191, blank=True, null=True)
    handicap =models.CharField(max_length=191, blank=True, null=True)
    size = models.CharField(max_length=191, blank=True, null=True)
    placedDate = models.DateTimeField(blank=True, null=True)
    sizeMatched = models.CharField(max_length=191, blank=True, null=True)
    user_id = models.CharField(max_length=191, blank=True, null=True)
    bookmaker_price = models.CharField(max_length=191, blank=True, null=True)
    bookmaker_size = models.CharField(max_length=191, blank=True, null=True)
    
    persistenceType= models.CharField(max_length=191, blank=True, null=True)
    orderType= models.CharField(max_length=191, blank=True, null=True)
    side= models.CharField(max_length=191, blank=True, null=True)
    betOutcome= models.CharField(max_length=191, blank=True, null=True)
    settledDate= models.DateTimeField(blank=True, null=True)
    priceReduced= models.CharField(max_length=191, blank=True, null=True)
    profit = models.CharField(max_length=191, blank=True, null=True)
    placeorder_update_status=models.BooleanField(default=False)
    class Meta:
        db_table = "place_orders_betfair"

class PlaceOrdersspbet(models.Model):
    status = models.TextField(blank=True, null=True)
    bet_id = models.TextField(blank=True, null=True)
    average_price_matched = models.TextField(blank=True, null=True)
    errorcode = models.TextField(blank=True, null=True)
    market_id = models.CharField(max_length=191, blank=True, null=True)
    selection_id = models.CharField(max_length=191, blank=True, null=True)
    price = models.CharField(max_length=191, blank=True, null=True)
    handicap =models.CharField(max_length=191, blank=True, null=True)
    size = models.CharField(max_length=191, blank=True, null=True)
    placedDate = models.DateTimeField(blank=True, null=True)
    sizeMatched = models.CharField(max_length=191, blank=True, null=True)
    user_id = models.CharField(max_length=191, blank=True, null=True)
    
    class Meta:
        db_table = "place_orders_spbet"

class ListcurrentOrders(models.Model):
    bet_id = models.CharField(max_length=191, blank=True, null=True)
    market_id = models.CharField(max_length=191, blank=True, null=True)
    selection_id = models.CharField(max_length=191, blank=True, null=True)
    handicap = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    size = models.TextField(blank=True, null=True)
    bspliability = models.TextField(blank=True, null=True)
    side = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    persistencetype = models.TextField(blank=True, null=True)
    ordertype = models.TextField(blank=True, null=True)
    placed_date = models.DateTimeField(blank=True, null=True)
    matcheddate = models.DateTimeField(blank=True, null=True)
    averagepricematched = models.TextField(blank=True, null=True)
    sizematched = models.TextField(blank=True, null=True)
    sizeremaining = models.TextField(blank=True, null=True)
    sizelapsed = models.TextField(blank=True, null=True)
    sizecancelled = models.TextField(blank=True, null=True)
    sizevoided = models.TextField(blank=True, null=True)
    regulatorcode = models.TextField(blank=True, null=True)


    class Meta:
        db_table = "listcurrentorders"

class Listmarketbook(models.Model):
    market_id = models.CharField(max_length=191, blank=True, null=True)
    is_marketdatadelayed = models.BooleanField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    betdelay = models.CharField(max_length=200,blank=True, null=True)
    bspreconciled = models.BooleanField(blank=True, null=True)
    complete = models.BooleanField(blank=True, null=True)
    inplay = models.BooleanField(blank=True, null=True)
    numberofwinners = models.CharField(max_length=200, blank=True, null=True)
    numberofrunners = models.CharField(max_length=200, blank=True, null=True)
    numberofactiverunners = models.CharField(max_length=200, blank=True, null=True)
    lastmatchtime = models.DateTimeField(blank=True, null=True)
    totalmatched = models.CharField(max_length=200, blank=True, null=True)
    totalavailable = models.CharField(max_length=200, blank=True, null=True)
    crossmatching = models.BooleanField(blank=True, null=True)
    runnersvoidable = models.BooleanField(blank=True, null=True)
    version = models.CharField(max_length=200, blank=True, null=True)
    runners = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "listmarketbook"

class MarketPrices(models.Model):
    market_id = models.CharField(max_length=191, blank=True, null=True)
    is_marketdatadelayed = models.BooleanField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    betdelay = models.CharField(max_length=200,blank=True, null=True)
    bspreconciled = models.BooleanField(blank=True, null=True)
    complete = models.BooleanField(blank=True, null=True)
    inplay = models.BooleanField(blank=True, null=True)
    numberofwinners = models.CharField(max_length=200, blank=True, null=True)
    numberofrunners = models.CharField(max_length=200, blank=True, null=True)
    numberofactiverunners = models.CharField(max_length=200, blank=True, null=True)
    lastmatchtime = models.DateTimeField(blank=True, null=True)
    totalmatched = models.CharField(max_length=200, blank=True, null=True)
    totalavailable = models.CharField(max_length=200, blank=True, null=True)
    crossmatching = models.BooleanField(blank=True, null=True)
    runnersvoidable = models.BooleanField(blank=True, null=True)
    version = models.CharField(max_length=200, blank=True, null=True)
    runners = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "marketprices"

class Countries(models.Model):
    country_id = models.BigIntegerField(blank=True,null=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    image_path = models.ImageField(blank=True, null=True)
    continent = models.CharField(max_length=191, blank=True, null=True)
    sub_region = models.CharField(max_length=191, blank=True, null=True)
    world_region = models.CharField(max_length=191, blank=True, null=True)
    fifa = models.CharField(max_length=191, blank=True, null=True)
    iso = models.CharField(max_length=191, blank=True, null=True)
    iso2 = models.CharField(max_length=191, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    flag = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "countries"
        verbose_name = "countries"
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name

class Legacy (models.Model):
    name = models.CharField(max_length=191,blank=True,null=True)

    class Meta:
        db_table = "legacy"

class Round(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        db_table = "round"

class Stage(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        db_table = "stage"

class Venue(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        db_table = "venue"

class Position(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        db_table = "position"

class Continents(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        db_table = "Continents"

class Group(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        db_table = "group"

class Aggregate(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        db_table = "aggregate"

class Referee(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        db_table = "referee"

class Weather(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        db_table = "weather"

class StandingSession(models.Model):
    standing_session_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    season_id = models.BigIntegerField(blank=True, null=True)
    round_id = models.BigIntegerField(blank=True, null=True)
    round_name = models.CharField(max_length=191, blank=True, null=True)
    type = models.CharField(max_length=191, blank=True, null=True)
    stage_id = models.BigIntegerField(blank=True, null=True)
    stage_name = models.CharField(max_length=191, blank=True, null=True)
    resource = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        db_table = "standing_season"

class Season(models.Model):
    
    name = models.CharField(max_length=191, blank=True, null=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    season_id = models.BigIntegerField(blank=True, null=True)
    round_id = models.BigIntegerField(blank=True, null=True)
    round_name = models.CharField(max_length=191, blank=True, null=True)
    type = models.CharField(max_length=191, blank=True, null=True)
    stage_id = models.BigIntegerField(blank=True, null=True)
    stage_name = models.CharField(max_length=191, blank=True, null=True)
    resource = models.CharField(max_length=191, blank=True, null=True)
    # standings = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=191, blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    team_name = models.CharField(max_length=191, blank=True, null=True)
    group_id = models.BigIntegerField(blank=True, null=True)
    group_name = models.CharField(max_length=191, blank=True, null=True)
    
    overall = models.TextField(blank=True, null=True)
    overall_games_played = models.BigIntegerField(default=0)
    overall_won = models.BigIntegerField(default=0)
    overall_draw = models.BigIntegerField(default=0)
    overall_lost = models.BigIntegerField(default=0)
    overall_goals_scored = models.BigIntegerField(default=0)
    overall_goals_against = models.BigIntegerField(default=0)
    overall_points = models.BigIntegerField(default=0)
    
    home = models.TextField(blank=True, null=True)

    home_games_played = models.BigIntegerField(default=0)
    home_won = models.BigIntegerField(default=0)
    home_draw = models.BigIntegerField(default=0)
    home_lost = models.BigIntegerField(default=0)
    home_goals_scored = models.BigIntegerField(default=0)
    home_goals_against = models.BigIntegerField(default=0)
    home_points = models.BigIntegerField(default=0)

    away = models.TextField(blank=True, null=True)

    away_games_played = models.BigIntegerField(default=0)
    away_won = models.BigIntegerField(default=0)
    away_draw = models.BigIntegerField(default=0)
    away_lost = models.BigIntegerField(default=0)
    away_goals_scored = models.BigIntegerField(default=0)
    away_goals_against = models.BigIntegerField(default=0)
    away_points = models.BigIntegerField(default=0)
    
    total = models.TextField(blank=True, null=True)

    total_goals_difference = models.BigIntegerField(default=0)
    total_points = models.BigIntegerField(default=0)

    result = models.CharField(max_length=191, blank=True, null=True)
    points = models.CharField(max_length=191, blank=True, null=True)
    recent_form = models.CharField(max_length=191, blank=True, null=True)
    status = models.CharField(max_length=191, blank=True, null=True)
    is_active = models.BooleanField(default=False, blank=True, null=True,verbose_name='Active')

    class Meta:
        db_table = "season"
        verbose_name = "Season Manager"
        verbose_name_plural = "Season Manager"

    def __str__(self):
        return self.name

class Leagues(models.Model):
    league_id = models.BigIntegerField(blank=True,null=True)
    active = models.BooleanField(blank=True,null=True)
    type = models.CharField(max_length=191,blank=True,null=True)
    legacy_id = models.BigIntegerField(blank=True, null=True)
    country_id = models.BigIntegerField(blank=True, null=True)
    logo_path = models.CharField(max_length=191,blank=True,null=True)
    name = models.CharField(max_length=191,blank=True,null=True)
    is_cup = models.BooleanField(blank=True,null=True)
    season_id = models.BigIntegerField(blank=True, null=True)
    round_id = models.BigIntegerField(blank=True, null=True)
    stage_id = models.BigIntegerField(blank=True, null=True)
    live_standings = models.BooleanField(blank=True, null=True)
    predictions = models.BooleanField(blank=True, null=True)
    topscorer_goals = models.BooleanField(blank=True, null=True)
    topscorer_assists = models.BooleanField(blank=True, null=True)
    topscorer_cards = models.BooleanField(blank=True, null=True)

    league_dname = models.CharField(max_length=255,blank=True,null=True)
    slug_name = models.CharField(max_length=255,blank=True,null=True)
    collection_datasource = models.CharField(max_length=255,blank=True,null=True)
    class Meta:
        db_table = "leagues"
        verbose_name = "League Manager"
        verbose_name_plural = "League Manager"

    def __str__(self):
        return self.name

class Teams(models.Model):
    id = models.CharField(max_length=512, default='',primary_key=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    legacy_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    short_code = models.CharField(max_length=191, blank=True, null=True)
    twitter = models.CharField(max_length=191, blank=True, null=True)
    country_id = models.BigIntegerField(blank=True, null=True)
    national_team = models.BooleanField(blank=True, null=True)
    founded = models.CharField(max_length=191, blank=True, null=True)
    logo_path = models.CharField(max_length=191, blank=True, null=True)
    venue_id = models.BigIntegerField(blank=True, null=True)
    season_id = models.BigIntegerField(blank=True, null=True)
    is_placeholder = models.BooleanField(blank=True, null=True)
    is_active = models.BooleanField(default=False,blank=True, null=True,verbose_name='Active')
    team_name_odd = models.CharField(max_length=255, blank=True, null=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    collection_datasource = models.CharField(max_length=255,blank=True,null=True)
    slug =  models.CharField(max_length=255,blank=True,null=True)
    data_id  = models.BigIntegerField(blank=True, null=True)
    current_season_id  = models.BigIntegerField(blank=True, null=True)
    class Meta:
        db_table = "teams"
        verbose_name = "Team Manager"
        verbose_name_plural = "Team Manager"

    def __str__(self):
        return self.name

class Players(models.Model):
    id = models.CharField(max_length=512, default='',primary_key=True)
    player_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    country_id = models.BigIntegerField(blank=True, null=True)
    position_id = models.BigIntegerField(blank=True, null=True)
    common_name = models.CharField(max_length=200,blank=True,null=True)
    display_name = models.CharField(max_length=200,blank=True,null=True)
    fullname = models.CharField(max_length=200,blank=True,null=True)
    firstname = models.CharField(max_length=200,blank=True,null=True)
    lastname = models.CharField(max_length=200,blank=True,null=True)
    nationality = models.CharField(max_length=200,blank=True,null=True)
    birthdate = models.DateField(blank=True, null=True)
    birthcountry = models.CharField(max_length=200, blank=True, null=True)
    birthplace = models.CharField(max_length=200, blank=True, null=True)
    height = models.CharField(max_length=200,blank=True,null=True)
    weight = models.CharField(max_length=200,blank=True,null=True)
    image_path = models.ImageField(blank=True, null=True)
    is_active = models.BooleanField(default=False,blank=True, null=True,verbose_name='Active')

    class Meta:
        db_table = "players"
        verbose_name = "Player Manager"
        verbose_name_plural = "Player Manager"

    def __str__(self):
        return self.display_name

# from django.contrib.postgres.fields import ArrayField
class MatchFixtureUpdate(models.Model):
    matchid = models.BigIntegerField(blank=True, null=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    season_id = models.BigIntegerField(blank=True, null=True)
    stage_id = models.BigIntegerField(blank=True, null=True)
    round_id = models.BigIntegerField(blank=True, null=True)
    group_id = models.BigIntegerField(blank=True, null=True)
    aggregate_id = models.BigIntegerField(blank=True, null=True)
    venue_id = models.BigIntegerField(blank=True, null=True)
    referee_id = models.BigIntegerField(blank=True, null=True)
    localteam_id = models.BigIntegerField(blank=True, null=True)
    visitorteam_id = models.BigIntegerField(blank=True, null=True)
    winnerteam_id = models.BigIntegerField(blank=True, null=True)
    weather_report = models.TextField(max_length=191, blank=True, null=True)
    commentaries = models.BooleanField(blank=True, null=True)
    attendance = models.CharField(max_length=191, blank=True, null=True)
    pitch = models.CharField(max_length=191, blank=True, null=True)
    details = models.CharField(max_length=191, blank=True, null=True)
    neutral_venue = models.BooleanField(blank=True, null=True)
    winning_odds_calculated = models.BooleanField(blank=True, null=True)
    # formations = models.ArrayField(models.TextField(null=True, blank=True))
    # formations = ArrayField(ArrayField(models.TextField(null=True, blank=True)))
    formations = models.TextField(null=True, blank=True)
    scores = models.TextField(null=True, blank=True)
    time = models.TextField(null=True, blank=True)
    coaches = models.TextField(null=True, blank=True)
    standings = models.TextField(null=True, blank=True)
    assistants = models.TextField(null=True, blank=True)
    leg = models.CharField(max_length=191, blank=True, null=True)
    colors = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(blank=True, null=True)
    is_placeholder = models.BooleanField(blank=True, null=True)
    time_date = models.DateField(blank=True, null=True,verbose_name = "Date")
    is_popular = models.BooleanField(default=False,verbose_name = "Popular",blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    # import datetime
    # from django.utils import timezone as tz
    # def get_date(self):
    #    d = tz.now() - datetime.timedelta(days=10)
    #    dish = MatchFixtureUpdate.objects.filter(time_date__lt=d)

    class Meta:
        db_table = "matchfixtureupdate"
        verbose_name = "Popular Match"
        verbose_name_plural = "Popular Match"

    def __str__(self):
        return str(self.matchid)

class Odds(models.Model):
    odds_id = models.BigIntegerField(models.Model)
    name = models.CharField(max_length=191, blank=True, null=True)
    suspended = models.BooleanField(blank=True, null=True)
    is_popular = models.BooleanField(default=False,verbose_name = "Popular",blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    class Meta:
        db_table = " Odds"
        verbose_name = "Popular Odds"
        verbose_name_plural = "Popular Odds"

    def __str__(self):
        return str(self.odds_id)

class Bookmaker(models.Model):
    parent_oddsid = models.BigIntegerField(models.Model)
    bookmaker_id = models.BigIntegerField(models.Model)
    bookmaker_name = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        db_table = "Bookmaker"

class Oddsdata(models.Model):
    parent_oddsid = models.BigIntegerField(models.Model)
    label = models.CharField(max_length=191, blank=True, null=True)
    value = models.CharField(max_length=191, blank=True, null=True)
    probability = models.CharField(max_length=191, blank=True, null=True)
    dp3 = models.CharField(max_length=191, blank=True, null=True)
    american = models.CharField(max_length=191, blank=True, null=True)
    factional = models.CharField(max_length=191, blank=True, null=True)
    winning = models.BooleanField(blank=True, null=True)
    handicap = models.CharField(max_length=191, blank=True, null=True)
    total = models.CharField(max_length=191, blank=True, null=True)
    bookmaker_event_id = models.CharField(max_length=191, blank=True, null=True)
    # last_update = models.TextField(max_length=191, blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True)
    timezone_type = models.CharField(max_length=191, blank=True, null=True)
    timezone = models.CharField(max_length=191, blank=True, null=True)


    class Meta:
        db_table = "Oddsdata"

class Fixture(models.Model):
    fixture_id = models.BigIntegerField(blank=True, null=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    season_id = models.BigIntegerField(blank=True, null=True)
    stage_id = models.BigIntegerField(blank=True, null=True)
    round_id = models.BigIntegerField(blank=True, null=True)
    group_id = models.BigIntegerField(blank=True, null=True)
    aggregate_id = models.BigIntegerField(blank=True, null=True)
    venue_id = models.BigIntegerField(blank=True, null=True)
    referee_id = models.BigIntegerField(blank=True, null=True)
    localteam_id = models.BigIntegerField(blank=True, null=True)
    visitorteam_id = models.BigIntegerField(blank=True, null=True)
    winnerteam_id = models.BigIntegerField(blank=True, null=True)
    weather_report = models.TextField(max_length=191, blank=True, null=True)
    commentaries = models.BooleanField(blank=True, null=True)
    attendance = models.CharField(max_length=191, blank=True, null=True)
    pitch = models.CharField(max_length=191, blank=True, null=True)
    details = models.CharField(max_length=191, blank=True, null=True)
    neutral_venue = models.BooleanField(blank=True, null=True)
    winning_odds_calculated = models.BooleanField(blank=True, null=True)
    formations = models.TextField(null=True, blank=True)
    scores = models.TextField(null=True, blank=True)
    time = models.TextField(null=True, blank=True)
    coaches = models.TextField(null=True, blank=True)
    standings = models.TextField(null=True, blank=True)
    assistants = models.TextField(null=True, blank=True)
    leg = models.CharField(max_length=191, blank=True, null=True)
    colors = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(blank=True, null=True)
    is_placeholder = models.BooleanField(blank=True, null=True)
    is_active = models.BooleanField(default=False, verbose_name="Active", blank=True, null=True)

    class Meta:
        db_table = "fixture"
        verbose_name = "Live match listing"
        verbose_name_plural = "Live match listing"

class PlayerStatistics(models.Model):
    parent_player_id = models.BigIntegerField(blank=True, null=True)
    player_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    season_id = models.BigIntegerField(blank=True, null=True)
    captain = models.CharField(max_length=200, blank=True, null=True)
    minutes = models.CharField(max_length=200, blank=True, null=True)
    appearences = models.CharField(max_length=200, blank=True, null=True)
    lineups = models.CharField(max_length=200, blank=True, null=True)
    substitute_in = models.CharField(max_length=200, blank=True, null=True)
    substitute_out = models.CharField(max_length=200, blank=True, null=True)
    substitutes_on_bench = models.CharField(max_length=200, blank=True, null=True)
    goals = models.CharField(max_length=200, blank=True, null=True)
    owngoals = models.CharField(max_length=200, blank=True, null=True)
    assists = models.CharField(max_length=200, blank=True, null=True)
    saves = models.CharField(max_length=200, blank=True, null=True)
    inside_box_saves = models.CharField(max_length=200, blank=True, null=True)
    dispossesed = models.CharField(max_length=200, blank=True, null=True)
    interceptions = models.CharField(max_length=200, blank=True, null=True)
    yellowcards = models.CharField(max_length=200, blank=True, null=True)
    yellowred = models.CharField(max_length=200, blank=True, null=True)
    redcards = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    tackles = models.CharField(max_length=200, blank=True, null=True)
    blocks = models.CharField(max_length=200, blank=True, null=True)
    hit_post = models.CharField(max_length=200, blank=True, null=True)
    cleansheets = models.CharField(max_length=200, blank=True, null=True)
    rating = models.CharField(max_length=200, blank=True, null=True)
    fouls = models.TextField(null=True, blank=True)
    crosses = models.TextField(null=True, blank=True)
    dribbles = models.TextField(null=True, blank=True)
    duels = models.TextField(null=True, blank=True)
    passes = models.TextField(null=True, blank=True)
    penalties = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "playerStatistics"

class SeasonStatistics(models.Model):
    season_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    is_current_season = models.BooleanField(blank=True, null=True)
    current_round_id = models.BigIntegerField(blank=True, null=True)
    current_stage_id = models.BigIntegerField(blank=True, null=True)
    iid = models.BigIntegerField(blank=True, null=True)
    stats_season_id = models.BigIntegerField(blank=True, null=True)
    stats_league_id = models.BigIntegerField(blank=True, null=True)
    number_of_clubs = models.CharField(max_length=200, blank=True, null=True)
    number_of_matches = models.CharField(max_length=200, blank=True, null=True)
    number_of_matches_played = models.CharField(max_length=200, blank=True, null=True)
    number_of_goals = models.CharField(max_length=200, blank=True, null=True)
    matches_both_teams_scored = models.CharField(max_length=200, blank=True, null=True)
    number_of_yellowcards = models.CharField(max_length=200, blank=True, null=True)
    number_of_yellowredcards = models.CharField(max_length=200, blank=True, null=True)
    number_of_redcards = models.CharField(max_length=200, blank=True, null=True)
    avg_goals_per_match = models.CharField(max_length=200, blank=True, null=True)
    avg_yellowcards_per_match = models.CharField(max_length=200, blank=True, null=True)
    avg_yellowredcards_per_match = models.CharField(max_length=200, blank=True, null=True)
    avg_redcards_per_match = models.CharField(max_length=200, blank=True, null=True)
    team_with_most_goals_id = models.BigIntegerField(blank=True, null=True)
    team_with_most_goals_number = models.CharField(max_length=200, blank=True, null=True)
    team_with_most_conceded_goals_id = models.BigIntegerField(blank=True, null=True)
    team_with_most_conceded_goals_number = models.CharField(max_length=200, blank=True, null=True)
    team_with_most_goals_per_match_id = models.BigIntegerField(blank=True, null=True)
    team_with_most_goals_per_match_number = models.CharField(max_length=200, blank=True, null=True)
    season_topscorer_id = models.BigIntegerField(blank=True, null=True)
    season_topscorer_number = models.CharField(max_length=200, blank=True, null=True)
    season_assist_topscorer_id = models.BigIntegerField(blank=True, null=True)
    season_assist_topscorer_number = models.CharField(max_length=200, blank=True, null=True)
    team_most_cleansheets_id = models.BigIntegerField(blank=True, null=True)
    team_most_cleansheets_number = models.CharField(max_length=200, blank=True, null=True)
    goals_scored_minutes =models.TextField(null=True, blank=True)
    goalkeeper_most_cleansheets_id =models.BigIntegerField(blank=True, null=True)
    goalkeeper_most_cleansheets_number = models.CharField(max_length=200, blank=True, null=True)
    goal_scored_every_minutes = models.CharField(max_length=200, blank=True, null=True)
    btts = models.CharField(max_length=200, blank=True, null=True)
    goal_line = models.TextField(null=True, blank=True)
    avg_corners_per_match = models.CharField(max_length=200, blank=True, null=True)
    team_most_corners_count = models.CharField(max_length=200, blank=True, null=True)
    team_most_corners_id = models.BigIntegerField(blank=True, null=True)
    goals_conceded = models.TextField(null=True, blank=True)
    goals_scored = models.TextField(null=True, blank=True)
    win_percentage = models.TextField(null=True, blank=True)
    defeat_percentage = models.TextField(null=True, blank=True)
    draw_percentage = models.CharField(max_length=200, blank=True, null=True)
    avg_homegoals_per_match = models.CharField(max_length=200, blank=True, null=True)
    avg_awaygoals_per_match = models.CharField(max_length=200, blank=True, null=True)
    avg_player_rating = models.CharField(max_length=200, blank=True, null=True)
    updated_at = models.DateField(null=True, blank=True)



    class Meta:
        db_table = "seasonstatistics"

class AllSeason(models.Model):
    id = models.CharField(max_length=512, default='',blank=True, primary_key=True)
    season_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    is_current_season = models.BooleanField(blank=True, null=True)
    current_round_id = models.BigIntegerField(blank=True, null=True)
    current_stage_id = models.BigIntegerField(blank=True, null=True)
    collection_datasource = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False, verbose_name="Active", blank=True, null=True)
    class Meta:
        db_table = "allseason"

class TeamStatistics(models.Model):
    id = models.CharField(max_length=512, default='',blank=True, primary_key=True)
    legacy_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    short_code = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    country_id = models.BigIntegerField(blank=True, null=True)
    national_team = models.BooleanField(blank=True, null=True)
    founded = models.CharField(max_length=200, blank=True, null=True)
    logo_path = models.CharField(max_length=191, blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    venue_id = models.CharField(max_length=200, blank=True, null=True)
    current_season_id = models.BigIntegerField(blank=True, null=True)
    is_placeholder = models.BooleanField(blank=True, null=True)
    class Meta:
        db_table = "TeamStatistics"

class TeamStatsDetails(models.Model):
    teamstatistics_id =models.TextField(blank=True, default=0)
    team_id = models.BigIntegerField(blank=True, null=True)
    season_id = models.BigIntegerField(blank=True, null=True)
    stage_id = models.BigIntegerField(blank=True, null=True)
    win = models.TextField(blank=True, null=True)
    draw = models.TextField(blank=True, null=True)
    lost = models.TextField(blank=True, null=True)
    goals_for = models.TextField(blank=True, null=True)
    goals_against = models.TextField(blank=True, null=True)
    clean_sheet = models.TextField(blank=True, null=True)
    failed_to_score = models.TextField(blank=True, null=True)
    scoring_minutes = models.TextField(blank=True, null=True)
    goals_conceded_minutes = models.TextField(blank=True, null=True)
    avg_goals_per_game_scored = models.TextField(blank=True, null=True)
    avg_goals_per_game_conceded = models.TextField(blank=True, null=True)
    avg_first_goal_scored = models.TextField(blank=True, null=True)
    avg_first_goal_conceded = models.TextField(blank=True, null=True)
    attacks = models.BigIntegerField(blank=True, null=True)
    dangerous_attacks = models.BigIntegerField(blank=True, null=True)
    avg_ball_possession_percentage = models.DecimalField(max_digits=15, default=0.0, decimal_places=4)
    fouls = models.BigIntegerField(blank=True, null=True)
    avg_fouls_per_game = models.DecimalField(max_digits=15,default=0.0, decimal_places=4)
    offsides = models.BigIntegerField(blank=True, null=True)
    redcards = models.BigIntegerField(blank=True, null=True)
    yellowcards = models.BigIntegerField(blank=True, null=True)
    shots_blocked = models.BigIntegerField(blank=True, null=True)
    shots_off_target = models.BigIntegerField(blank=True, null=True)
    avg_shots_off_target_per_game = models.DecimalField(max_digits=15, default=0.0, decimal_places=4)
    shots_on_target = models.BigIntegerField(blank=True, null=True)
    avg_shots_on_target_per_game = models.DecimalField(max_digits=15, default=0.0, decimal_places=4)
    avg_corners = models.DecimalField(max_digits=15, default=0.0,decimal_places=4)
    total_corners = models.BigIntegerField(blank=True, null=True)
    btts  = models.DecimalField(max_digits=15, default=0.0, decimal_places=4)
    goal_line_over = models.TextField(blank=True, null=True)
    goal_line_under = models.TextField(blank=True, null=True)
    avg_player_rating = models.DecimalField(max_digits=15, default=0.0, decimal_places=4)
    avg_player_rating_per_match = models.DecimalField(max_digits=15, default=0.0, decimal_places=4)
    tackles = models.BigIntegerField(blank=True, null=True)
    class Meta:
       db_table = "TeamStatsDetails"

class PopularMatch(models.Model):
    match = models.OneToOneField(MatchFixtureUpdate, on_delete=models.CASCADE)
    is_popular = models.BooleanField(default=False)
    date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.match.matchid)

    class Meta:
        db_table = "popular_match"

class PopularOdds(models.Model):
    odds = models.OneToOneField(Odds, on_delete=models.CASCADE)
    is_popular = models.BooleanField(default=False)
    date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.odds.odds_id)

    class Meta:
        db_table = "popular_odds"

class Statistics(models.Model):
    RANKING_CHOICES = (
        ('1', 'Ranking 1'),
        ('2', 'Ranking 2'),
        ('3', 'Ranking 3'),
        ('4', 'Ranking 4'),
    )
    ranking = models.CharField(max_length=32, choices=RANKING_CHOICES, null=True, blank=True)
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "statistics"

class MatchRanking(models.Model):
    # RANKING_CHOICES = (
    #     ('1', 'Ranking 1'),
    #     ('2', 'Ranking 2'),
    #     ('3', 'Ranking 3'),
    #     ('4', 'Ranking 4'),
    # )
    # ranking = models.CharField(max_length=32, choices=RANKING_CHOICES, null=True, blank=True)
    rank_id = models.AutoField(primary_key = True)
    ranking = models.CharField(max_length=200,null=True, blank=True)
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "match_ranking"
        verbose_name = "Match Ranking"
        verbose_name_plural = "Match Ranking"

class MatchRankings(models.Model):
    # RANKING_CHOICES = (
    #     ('1', 'Ranking 1'),
    #     ('2', 'Ranking 2'),
    #     ('3', 'Ranking 3'),
    #     ('4', 'Ranking 4'),
    # )
    # ranking = models.CharField(max_length=32, choices=RANKING_CHOICES, null=True, blank=True)
    ranking = models.CharField(max_length=200,null=True, blank=True)
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "match_rankings"
        verbose_name = "Match Ranking"
        verbose_name_plural = "Match Ranking"

class Cms(models.Model):
    class Meta:
        db_table = 'Cms'
        verbose_name = "Cms"
        verbose_name_plural = "Cms"

    # enum_choices = (
    #     ('y', 'y'),
    #     ('n', 'n')
    # )

    title = models.CharField(max_length=255, default='')
    slug = models.CharField(max_length=255, default='')
    description = models.TextField(null=True)
    meta_title = models.TextField(null=True)
    meta_key = models.TextField(null=True)
    meta_description = models.TextField(null=True)
    # ispublished = models.CharField(max_length=2, choices=enum_choices, default='y')
    # isblocked = models.CharField(max_length=2, choices=enum_choices, default='n')
    # isdeleted = models.CharField(max_length=2, choices=enum_choices, default='n')
    is_published = models.BooleanField(default=True,null=True,blank=True,verbose_name = "Published")
    is_blocked = models.BooleanField(default=False,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    class Meta:
        db_table = 'message'

    message_type_choices = (
        ('message', 'message'),
        ('file', 'file'),
        ('image', 'image')
    )

    enum_choices = (
        ('yes', 'yes'),
        ('no', 'no')
    )


    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='message_receiver_info', null=True)
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='message_sender_info', null=True)
    message = models.TextField(null=True)
    is_read = models.BooleanField(default=False)
    message_type = models.CharField(max_length=255, default='message')
    created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True,verbose_name = "Date")
    is_email_sent = models.CharField(max_length=20, choices=enum_choices, default='no')
    email_sent_date = models.DateTimeField(null=True,blank=True)
    reply_message_id = models.BigIntegerField(blank=True, null=True)

class Betslip(MatchFixtureUpdate):
    class Meta:
        proxy = True
        verbose_name = "Bet slip"
        verbose_name_plural = "Bet slip"

class SeasonMatchPlan(models.Model):
    class Meta:
        db_table = 'season_match_plan'
        verbose_name = "Season Match Plan"
        verbose_name_plural = "Season Match Plan"
    # CREATE TABLE season_match_plan (
    match_id = models.BigIntegerField(blank=True, null=True)
    season_id =  models.BigIntegerField(blank=True, null=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    date = models.CharField(max_length=255, default='')
    time  = models.CharField(max_length=255, default='')
    home_team_id =  models.BigIntegerField(blank=True, null=True)
    away_team_id = models.BigIntegerField(blank=True, null=True)
    total_home_score = models.BigIntegerField(blank=True, null=True)
    half_home_score = models.BigIntegerField(blank=True, null=True)
    total_away_score = models.BigIntegerField(blank=True, null=True)
    half_away_score = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, default='')
    Home_TGPR = models.CharField(max_length=255, default='')
    Away_TGPR = models.CharField(max_length=255, default='')
    D_Home_RS_8 = models.CharField(max_length=255, default='')
    D_Home_ranking_8 = models.CharField(max_length=255, default='')
    D_Home_RS_6 = models.CharField(max_length=255, default='')
    D_Home_ranking_6= models.CharField(max_length=255, default='')
    home_team_score = models.CharField(max_length=255, default='')
    home_team_strength = models.CharField(max_length=255, default='')
    away_team_score = models.CharField(max_length=255, default='')
    away_team_strength = models.CharField(max_length=255, default='')
    D_Away_RS_8 = models.CharField(max_length=255, default='')
    D_Away_ranking_8 = models.CharField(max_length=255, default='')
    D_Away_RS_6 = models.CharField(max_length=255, default='')
    D_Away_ranking_6 = models.CharField(max_length=255, default='')
    HPPG = models.CharField(max_length=255, default='')
    HGDPG = models.CharField(max_length=255, default='')
    APPG = models.CharField(max_length=255, default='')
    AGDPG = models.CharField(max_length=255, default='')
    WN  = models.BigIntegerField(blank=True, null=True)
    c_WN  = models.BigIntegerField(blank=True, null=True)
    DSL_refer_id  = models.BigIntegerField(blank=True, null=True)
    DCL_refer_id  = models.BigIntegerField(blank=True, null=True)
    CL_mo_refer_id  = models.BigIntegerField(blank=True, null=True)
    collection_datasource = models.CharField(max_length=255, default='')

class MatchTeamPlayerInfo(models.Model):
    
    class Meta:
        db_table = 'match_team_player_info'
        verbose_name = "MatchTeamPlayerInfo"
        verbose_name_plural = "MatchTeamPlayerInfo"
    id = models.CharField(max_length=512, default='',primary_key=True)
    match_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    player_id = models.BigIntegerField(blank=True, null=True)
    goals = models.BigIntegerField(blank=True, null=True)
    assists = models.BigIntegerField(blank=True, null=True)
    collection_datasource = models.CharField(max_length=255, default='')

class PlayerCareer(models.Model):
    
    class Meta:
        db_table = 'player_career'
        verbose_name = "PlayerCareer"
        verbose_name_plural = "PlayerCareer"
    id = models.CharField(max_length=512, default='',primary_key=True)
    player_id = models.BigIntegerField(blank=True, null=True)
    flag = models.CharField(max_length=255, default='')
    season_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    league_id =models.BigIntegerField(blank=True, null=True)
    matches = models.BigIntegerField(blank=True, null=True)
    goals = models.BigIntegerField(blank=True, null=True)
    started = models.BigIntegerField(blank=True, null=True)
    s_in = models.BigIntegerField(blank=True, null=True)
    s_out = models.BigIntegerField(blank=True, null=True)
    yellow = models.BigIntegerField(blank=True, null=True)
    s_yellow = models.BigIntegerField(blank=True, null=True)
    red = models.BigIntegerField(blank=True, null=True)
    collection_datasource = models.CharField(max_length=255, default='')

class PlayerList(models.Model):
    
    class Meta:
        db_table = 'playerlist'
        verbose_name = "PlayerList"
        verbose_name_plural = "PlayerList"
   
    player_id = models.BigIntegerField(blank=True, null=True)
    player_name = models.CharField(max_length=255, default='')
    birthday = models.CharField(max_length=255, default='')
    nationality = models.CharField(max_length=255, default='')
    img_src = models.CharField(max_length=255, default='')
    height = models.CharField(max_length=255, default='')
    weight = models.CharField(max_length=255, default='')
    foot = models.CharField(max_length=255, default='')
    position = models.CharField(max_length=255, default='')
    now_team_id = models.BigIntegerField(blank=True, null=True)
    now_pNumber = models.BigIntegerField(blank=True, null=True)
    collection_datasource = models.CharField(max_length=255, default='')

class SeasonLeagueTeamInfo(models.Model):
    
    class Meta:
        db_table = 'season_league_team_info'
        verbose_name = "SeasonLeagueTeamInfo"
        verbose_name_plural = "SeasonLeagueTeamInfo"
    
    info_id = models.BigIntegerField(blank=True, null=True)
    season_id = models.BigIntegerField(blank=True, null=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    t_mp = models.BigIntegerField(blank=True, null=True)
    t_w = models.BigIntegerField(blank=True, null=True)
    t_d = models.BigIntegerField(blank=True, null=True)
    t_l = models.BigIntegerField(blank=True, null=True)
    t_f = models.BigIntegerField(blank=True, null=True)
    t_a = models.BigIntegerField(blank=True, null=True)
    h_mp = models.BigIntegerField(blank=True, null=True)
    h_w = models.BigIntegerField(blank=True, null=True)
    h_d = models.BigIntegerField(blank=True, null=True)
    h_l = models.BigIntegerField(blank=True, null=True)
    h_f = models.BigIntegerField(blank=True, null=True)
    h_a = models.BigIntegerField(blank=True, null=True)
    a_mp = models.BigIntegerField(blank=True, null=True)
    a_w = models.BigIntegerField(blank=True, null=True)
    a_d = models.BigIntegerField(blank=True, null=True)
    a_l = models.BigIntegerField(blank=True, null=True)
    a_f = models.BigIntegerField(blank=True, null=True)
    a_a = models.BigIntegerField(blank=True, null=True)
    D = models.BigIntegerField(blank=True, null=True)
    P = models.BigIntegerField(blank=True, null=True)
    PPG = models.CharField(max_length=255, default='')
    HPPG = models.CharField(max_length=255, default='')
    H_percent = models.CharField(max_length=255, default='')
    HG =  models.CharField(max_length=255, default='')
    HDGPG = models.CharField(max_length=255, default='')
    HRS = models.CharField(max_length=255, default='')
    APPG = models.CharField(max_length=255, default='')
    A_percent = models.CharField(max_length=255, default='')
    AG =  models.CharField(max_length=255, default='')
    ADGPG = models.CharField(max_length=255, default='')
    ARS = models.CharField(max_length=255, default='')
    S_H_ranking = models.CharField(max_length=255, default='')
    S_A_ranking = models.CharField(max_length=255, default='')
    collection_datasource = models.CharField(max_length=255, default='')

class ScrapTool(models.Model):
    class Meta:
        db_table = 'scrap_tool'
    slug = models.SlugField(max_length = 250, unique = True) 
    scrapname = models.TextField(null=True)
    scrap_url = models.TextField(null=True)
    scrap_element_class = models.TextField(null=True)
    scrap_return_reult = models.TextField(null=True)
    scrap_type =  models.CharField(max_length=255, default='')
    scrap_element_type =  models.CharField(max_length=255, default='')
    exemptColumn =  models.CharField(max_length=255, default='')
    created_date = models.DateTimeField(auto_now_add=True)

class CreamTeam(models.Model):
    class Meta:
        db_table = 'cream_team_list'
    
    id = models.CharField(max_length=512, default='',primary_key=True)
    season_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    cream_status =  models.CharField(max_length=255, default='')

class OddCalculation(models.Model):
    class Meta:
        db_table = 'odd_calculation'
    id = models.CharField(max_length=512, default='',primary_key=True)
    match_id  = models.BigIntegerField(blank=True, null=True)
    bookmaker_id  = models.BigIntegerField(blank=True, null=True)
    Home = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    Draw = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    Away = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    Over2d5 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    Under2d5 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH2_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH2_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH1d75_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH1d75_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH1d5_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH1d5_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH1d25_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH1d25_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH1_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH1_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH0d75_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH0d75_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH0d5_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH0d5_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH0d25_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH0d25_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH0_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH0_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p0d25_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p0d25_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p0d5_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p0d5_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p0d75_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p0d75_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p1_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p1_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p1d25_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p1d25_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p1d5_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p1d5_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p1d75_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p1d75_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p2_1 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    AH_p2_2 = models.DecimalField(max_digits=15,  null=True, decimal_places=4)
    collection_datasource = models.CharField(max_length=255, default='')
    updated_at = models.DateTimeField(auto_now_add=True)

class HomeAwayTeamByLeague(models.Model):
    class Meta:
        db_table = 'home_away_team_by_league'
    
    id = models.CharField(max_length=512, default='',primary_key=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    team_type =  models.CharField(max_length=255, default='')
    team_name =  models.CharField(max_length=255, default='')
    team_slug =  models.CharField(max_length=255, default='')
    gp =  models.BigIntegerField(blank=True, null=True)
    w =  models.BigIntegerField(blank=True, null=True)
    d =  models.BigIntegerField(blank=True, null=True)
    l =  models.BigIntegerField(blank=True, null=True)
    gf =  models.BigIntegerField(blank=True, null=True)
    ga =  models.BigIntegerField(blank=True, null=True)
    gd =  models.BigIntegerField(blank=True, null=True)
    pts =  models.BigIntegerField(blank=True, null=True)
    collection_datasource = models.CharField(max_length=255, default='')
    created = models.DateTimeField(auto_now_add=True)

class TeamDetailsScrapData(models.Model):
    class Meta:
        db_table = 'team_detailss_scrap_data'

    id = models.CharField(max_length=512, default='',primary_key=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    team_slug =  models.CharField(max_length=255, default='')
    season_id = models.BigIntegerField(blank=True, null=True)
    gp =  models.BigIntegerField(blank=True, null=True)
    w =  models.BigIntegerField(blank=True, null=True)
    d =  models.BigIntegerField(blank=True, null=True)
    l =  models.BigIntegerField(blank=True, null=True)
    gf =  models.BigIntegerField(blank=True, null=True)
    ga =  models.BigIntegerField(blank=True, null=True)
    gd =  models.BigIntegerField(blank=True, null=True)
    pts =  models.BigIntegerField(blank=True, null=True)
    collection_datasource = models.CharField(max_length=255, default='')
    created = models.DateTimeField(auto_now_add=True)

class TeamGoalStatistics(models.Model):
    class Meta:
        db_table = 'team_goalstatistics'
    id = models.CharField(max_length=512, default='',primary_key=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    team_id   = models.BigIntegerField(blank=True, null=True)
    team_slug =  models.CharField(max_length=255, default='')
    season_id = models.BigIntegerField(blank=True, null=True)
    fieldName =  models.CharField(max_length=255, default='')
    homevalue = models.CharField(max_length=255, default='')
    awayvalue = models.CharField(max_length=255, default='')
    allvalue = models.CharField(max_length=255, default='')
    collection_datasource = models.CharField(max_length=255, default='')
    created = models.DateTimeField(auto_now_add=True)
class CountryFootballDataCoUk(models.Model):
    class Meta:
        db_table = 'country_football_data_co_uk'

    id = models.CharField(max_length=512, default='',primary_key=True)
    country_name=models.CharField(max_length=255, default='')
    country_url =models.TextField(null=True)
    country_logo = models.CharField(max_length=255, default='')
    collection_datasource = models.CharField(max_length=255, default='')
    created = models.DateTimeField(auto_now_add=True)

class FixtureRapidApi(models.Model):
    class Meta:
        db_table = 'fixture_rapid_api'

    fixture_id:models.CharField(max_length=512, default='',primary_key=True)
    referee=models.CharField(max_length=255, default='')
    timezone=models.CharField(max_length=255, default='')
    date= models.DateTimeField(null=True)
    timestamp=models.CharField(max_length=255, default='')
    periods_first=models.CharField(max_length=255, default='')
    periods_second=models.CharField(max_length=255, default='')
    venue_id=models.BigIntegerField(blank=True, null=True)
    venue_name=models.CharField(max_length=255, default='')
    venue_city=models.CharField(max_length=255, default='')
    status_long=models.CharField(max_length=255, default='')
    status_short=models.CharField(max_length=255, default='')
    status_elapsed=models.CharField(max_length=255, default='')
    league_id=models.BigIntegerField(blank=True, null=True)
    league_name=models.CharField(max_length=255, default='')
    league_country=models.CharField(max_length=255, default='')
    league_logo=models.CharField(max_length=255, default='')
    league_flag=models.CharField(max_length=255, default='')
    league_season=models.CharField(max_length=255, default='')
    league_round=models.CharField(max_length=255, default='')
    teams_home_id=models.BigIntegerField(blank=True, null=True)
    teams_home_name=models.CharField(max_length=255, default='')
    teams_home_logo=models.CharField(max_length=255, default='')
    teams_home_winner=models.CharField(max_length=255, default='')
    teams_away_id=models.BigIntegerField(blank=True, null=True)
    teams_away_name=models.CharField(max_length=255, default='')
    teams_away_logo=models.CharField(max_length=255, default='')
    teams_away_winner=models.CharField(max_length=255, default='')
    goal_home=models.CharField(max_length=255, default='')
    goal_away=models.CharField(max_length=255, default='')
    score_halftime_home=models.CharField(max_length=255, default='')
    score_halftime_away=models.CharField(max_length=255, default='')
    score_fulltime_home=models.CharField(max_length=255, default='')
    score_fulltime_away=models.CharField(max_length=255, default='')
    score_extratime_home=models.CharField(max_length=255, default='')
    score_extratime_away=models.CharField(max_length=255, default='')
    score_penalty_home=models.CharField(max_length=255, default='')
    score_penalty_away=models.CharField(max_length=255, default='')

class LeagueRapidApi(models.Model):
    class Meta:
        db_table = 'league_rapid_api'

    league_id = models.CharField(max_length=512, default='',primary_key=True)
    name=models.CharField(max_length=255, default='')
    league_type=models.CharField(max_length=255, default='')
    logo=models.CharField(max_length=255, default='')
    country_name=models.CharField(max_length=255, default='')
    country_code=models.CharField(max_length=255, default='')
    country_flag=models.CharField(max_length=255, default='')
    seasons=models.TextField(null=True)

class SeasonRapidApi(models.Model):
    class Meta:
        db_table = 'season_rapid_api'

    season_id = models.CharField(max_length=512, default='',primary_key=True)
    year=models.CharField(max_length=255, default='')
    start= models.DateTimeField(null=True)
    end= models.DateTimeField(null=True)
    current=models.TextField(null=True)
    coverage=models.CharField(max_length=255, default='')
    
class LeaguesOtherSource(models.Model):
    league_id = models.BigIntegerField(blank=True,null=True)
    active = models.BooleanField(blank=True,null=True)
    type = models.CharField(max_length=191,blank=True,null=True)
    legacy_id = models.BigIntegerField(blank=True, null=True)
    country_id = models.BigIntegerField(blank=True, null=True)
    logo_path = models.CharField(max_length=191,blank=True,null=True)
    name = models.CharField(max_length=191,blank=True,null=True)
    is_cup = models.BooleanField(blank=True,null=True)
    season_id = models.BigIntegerField(blank=True, null=True)
    round_id = models.BigIntegerField(blank=True, null=True)
    stage_id = models.BigIntegerField(blank=True, null=True)
    live_standings = models.BooleanField(blank=True, null=True)
    predictions = models.BooleanField(blank=True, null=True)
    topscorer_goals = models.BooleanField(blank=True, null=True)
    topscorer_assists = models.BooleanField(blank=True, null=True)
    topscorer_cards = models.BooleanField(blank=True, null=True)

    league_dname = models.CharField(max_length=255,blank=True,null=True)
    slug_name = models.CharField(max_length=255,blank=True,null=True)
    collection_datasource = models.CharField(max_length=255,blank=True,null=True)
    class Meta:
        db_table = "leagues_other_source"
        verbose_name = "League Manager Other Source"
        verbose_name_plural = "League Manager Other Source"

    def __str__(self):
        return self.name

# Model For Historic Data
class HistoricData(models.Model):
    class Meta:
        db_table = 'historic_data'
    id = models.CharField(max_length=512, default='',primary_key=True)
    Date = models.DateTimeField(null=True)
    League =models.CharField(max_length=255, default='')
    HomeTeam =models.CharField(max_length=255, default='')
    AwayTeam =models.CharField(max_length=255, default='')
    FTHG =models.CharField(max_length=255, default='')
    FTAG=models.CharField(max_length=255, default='')
    FTR =models.CharField(max_length=255, default='')
    AST =models.CharField(max_length=255, default='')
    HomeTeamLP =models.CharField(max_length=255, default='')
    AwayTeamLP =models.CharField(max_length=255, default='')
    HTFormPts =models.CharField(max_length=255, default='')
    ATFormPts =models.CharField(max_length=255, default='')
    HTQualityCR =models.CharField(max_length=255, default='')
    ATQualityCR =models.CharField(max_length=255, default='')
    PredictedFTR =models.CharField(max_length=255, default='')
    PredictedHomeWinProbability =models.CharField(max_length=255, default='')
    PredictedDrawProbability =models.CharField(max_length=255, default='')
    PredictedAwayWinProbability =models.CharField(max_length=255, default='')
    PredictedHomeWinOdds =models.CharField(max_length=255, default='')
    PredictedDrawOdds =models.CharField(max_length=255, default='')
    PredictedAwayWinOdds =models.CharField(max_length=255, default='')

class LeagueGoalserve(models.Model):
    class Meta:
        db_table = 'league_goalserve'

    id = models.CharField(max_length=512, default='',primary_key=True)
    league_id=models.BigIntegerField(blank=True, null=True)
    country=models.CharField(max_length=255, default='')
    name=models.CharField(max_length=255, default='')
    season=models.CharField(max_length=255, default='')
    date_start= models.DateTimeField(null=True)
    date_end= models.DateTimeField(null=True)
    iscup=models.CharField(max_length=255, default='')
    live_lineups=models.CharField(max_length=255, default='')
    live_stats=models.CharField(max_length=255, default='')
    path=models.CharField(max_length=255, default='')
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False, verbose_name="Active", blank=True, null=True)

class SeasonGoalserve(models.Model):
    class Meta:
        db_table = 'season_goalserve'

    id = models.CharField(max_length=512, default='',primary_key=True)
    league_id=models.BigIntegerField(blank=True, null=True)
    country=models.CharField(max_length=255, default='')
    league_name=models.CharField(max_length=255, default='')
    iscup=models.CharField(max_length=255, default='')
    season=models.CharField(max_length=255, default='')
    is_standing =models.CharField(max_length=255, default='')
    standing =models.CharField(max_length=255, default='')
    created = models.DateTimeField(auto_now_add=True)

class MatchGoalserve(models.Model):
    class Meta:
        db_table = 'match_goalserve'

    id= models.CharField(max_length=512, default='',primary_key=True)
    group_id= models.BigIntegerField(blank=True, null=True)
    league_id= models.BigIntegerField(blank=True, null=True)
    match_name=models.CharField(max_length=255, default='')
    gid= models.BigIntegerField(blank=True, null=True)
    file_group=models.CharField(max_length=255, default='')
    iscup=models.CharField(max_length=255, default='')
    string_date = models.CharField(max_length=255, default='')
    formated_date=models.DateTimeField(null=True)
    formated_time=models.CharField(max_length=255, default='')
    time_status=models.CharField(max_length=255, default='')
    venue=models.CharField(max_length=255, default='')
    static_id= models.CharField(max_length=255, default='')
    fix_id= models.BigIntegerField(blank=True, null=True)
    match_id= models.BigIntegerField(blank=True, null=True)
    localteam_name=models.CharField(max_length=255, default='')
    localteam_goals=models.CharField(max_length=255, default='')
    localteam_id= models.BigIntegerField(blank=True, null=True)
    visitorteam_name=models.CharField(max_length=255, default='')
    visitorteam_goals=models.CharField(max_length=255, default='')
    visitorteam_id= models.BigIntegerField(blank=True, null=True)
    events=models.CharField(max_length=255, default='')
    ht_score=models.CharField(max_length=255, default='')
    created = models.DateTimeField(auto_now_add=True)

class TeamStatisticsGoalserve(models.Model):
    class Meta:
        db_table = 'teamstatistics_goalserve'
    
    id= models.CharField(max_length=512, default='',primary_key=True)
    match_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    is_national_team = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    fullname = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255, default='')
    founded = models.CharField(max_length=255, default='')
    league_rank = models.CharField(max_length=255, default='')
    league_ids = models.CharField(max_length=255, default='')
    venue_name = models.CharField(max_length=255, default='')
    venue_id = models.CharField(max_length=255, default='')
    venue_city = models.CharField(max_length=255, default='')
    venue_capacity = models.CharField(max_length=255, default='')
    venue_address = models.CharField(max_length=255, default='')
    venue_image = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    coach_id = models.CharField(max_length=255, default='')
    coach_name = models.CharField(max_length=255, default='')
    
    rank_home = models.CharField(max_length=255, default='')
    rank_total = models.CharField(max_length=255, default='')
    rank_away = models.CharField(max_length=255, default='')

    win_home = models.CharField(max_length=255, default='')
    win_total = models.CharField(max_length=255, default='')
    win_away = models.CharField(max_length=255, default='')

    draw_home = models.CharField(max_length=255, default='')
    draw_total = models.CharField(max_length=255, default='')
    draw_away = models.CharField(max_length=255, default='')

    lost_home = models.CharField(max_length=255, default='')
    lost_total = models.CharField(max_length=255, default='')
    lost_away = models.CharField(max_length=255, default='')

    goals_for_home = models.CharField(max_length=255, default='')
    goals_for_total = models.CharField(max_length=255, default='')
    goals_for_away = models.CharField(max_length=255, default='')

    goals_against_home = models.CharField(max_length=255, default='')
    goals_against_total = models.CharField(max_length=255, default='')
    goals_against_away = models.CharField(max_length=255, default='')

    clean_sheet_home = models.CharField(max_length=255, default='')
    clean_sheet_total = models.CharField(max_length=255, default='')
    clean_sheet_away = models.CharField(max_length=255, default='')

    avg_goals_per_game_conceded_home = models.CharField(max_length=255, default='')
    avg_goals_per_game_conceded_total = models.CharField(max_length=255, default='')
    avg_goals_per_game_conceded_away = models.CharField(max_length=255, default='')

    avg_first_goal_conceded_home = models.CharField(max_length=255, default='')
    avg_first_goal_conceded_total = models.CharField(max_length=255, default='')
    avg_first_goal_conceded_away = models.CharField(max_length=255, default='')

    avg_first_goal_scored_home = models.CharField(max_length=255, default='')
    avg_first_goal_scored_total = models.CharField(max_length=255, default='')
    avg_first_goal_scored_away = models.CharField(max_length=255, default='')

    avg_goals_per_game_scored_home = models.CharField(max_length=255, default='')
    avg_goals_per_game_scored_total = models.CharField(max_length=255, default='')
    avg_goals_per_game_scored_away = models.CharField(max_length=255, default='')

    scoring_minutes = models.CharField(max_length=255, default='')

class TeamPlayerSquadGoalserve(models.Model):
    class Meta:
        db_table = 'teamsplayersquad_goalserve'
    
    id= models.CharField(max_length=512, default='',primary_key=True)
    match_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    age = models.CharField(max_length=255, default='')
    appearences = models.CharField(max_length=255, default='')
    assists = models.CharField(max_length=255, default='')
    blocks = models.CharField(max_length=255, default='')
    clearances = models.CharField(max_length=255, default='')
    crossesAccurate = models.CharField(max_length=255, default='')
    crossesTotal = models.CharField(max_length=255, default='')
    dispossesed = models.CharField(max_length=255, default='')
    dribbleAttempts = models.CharField(max_length=255, default='')
    dribbleSucc = models.CharField(max_length=255, default='')
    duelsTotal = models.CharField(max_length=255, default='')
    duelsWon = models.CharField(max_length=255, default='')
    fouldDrawn = models.CharField(max_length=255, default='')
    foulsCommitted = models.CharField(max_length=255, default='')
    goals = models.CharField(max_length=255, default='')
    goalsConceded = models.CharField(max_length=255, default='')
    player_id = models.CharField(max_length=255, default='')
    injured = models.CharField(max_length=255, default='')
    insideBoxSaves = models.CharField(max_length=255, default='')
    interceptions = models.CharField(max_length=255, default='')
    isCaptain = models.CharField(max_length=255, default='')
    keyPasses = models.CharField(max_length=255, default='')
    lineups = models.CharField(max_length=255, default='')
    minutes = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    number = models.CharField(max_length=255, default='')
    pAccuracy = models.CharField(max_length=255, default='')
    passes = models.CharField(max_length=255, default='')
    penComm = models.CharField(max_length=255, default='')
    penMissed = models.CharField(max_length=255, default='')
    penSaved = models.CharField(max_length=255, default='')
    penScored = models.CharField(max_length=255, default='')
    penWon = models.CharField(max_length=255, default='')
    position = models.CharField(max_length=255, default='')
    rating = models.CharField(max_length=255, default='')
    redcards = models.CharField(max_length=255, default='')
    saves = models.CharField(max_length=255, default='')
    shotsOn = models.CharField(max_length=255, default='')
    shotsTotal = models.CharField(max_length=255, default='')
    substitutes_on_bench = models.CharField(max_length=255, default='')
    substitute_in = models.CharField(max_length=255, default='')
    substitute_out = models.CharField(max_length=255, default='')
    tackles = models.CharField(max_length=255, default='')
    woordworks = models.CharField(max_length=255, default='')
    yellowcards = models.CharField(max_length=255, default='')
    yellowred = models.CharField(max_length=255, default='')
 
class TeamPlayerTransferINGoalserve(models.Model):
    class Meta:
        db_table = 'teamsplayer_transfer_from_goalserve'
    
    id= models.CharField(max_length=512, default='',primary_key=True)
    match_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    age = models.CharField(max_length=255, default='')
    date = models.DateField(null=True, blank=True)
    from_team = models.CharField(max_length=255, default='')
    player_id = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    position = models.CharField(max_length=255, default='')
    from_team_id = models.CharField(max_length=255, default='')
    from_type = models.CharField(max_length=255, default='')
    transfer_type = models.CharField(max_length=255, default='')
    
class TeamPlayerTransferOUTGoalserve(models.Model):
    class Meta:
        db_table = 'teamsplayer_transfer_to_goalserve'
    
    id= models.CharField(max_length=512, default='',primary_key=True)
    match_id = models.BigIntegerField(blank=True, null=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    age = models.CharField(max_length=255, default='')
    date = models.DateField(null=True, blank=True)
    to_team = models.CharField(max_length=255, default='')
    player_id = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    position = models.CharField(max_length=255, default='')
    to_team_id = models.CharField(max_length=255, default='')
    from_type = models.CharField(max_length=255, default='')
    transfer_type = models.CharField(max_length=255, default='')
    
class TeamsLeagueStatisticsToGoalserve(models.Model):
    class Meta:
        db_table = 'teams_league_statistics_goalserve'
    
    id= models.CharField(max_length=512, default='',primary_key=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    league_id = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    season = models.CharField(max_length=255, default='')
    
    fulltime_avg_corners_total = models.CharField(max_length=255, default='')
    fulltime_avg_corners_home = models.CharField(max_length=255, default='')
    fulltime_avg_corners_away = models.CharField(max_length=255, default='')
    
    fulltime_avg_first_goal_conceded_total = models.CharField(max_length=255, default='')
    fulltime_avg_first_goal_conceded_home = models.CharField(max_length=255, default='')
    fulltime_avg_first_goal_conceded_away = models.CharField(max_length=255, default='')
    
    fulltime_avg_first_goal_scored_total = models.CharField(max_length=255, default='')
    fulltime_avg_first_goal_scored_home = models.CharField(max_length=255, default='')
    fulltime_avg_first_goal_scored_away = models.CharField(max_length=255, default='')
    
       
    fulltime_avg_goals_per_game_conceded_total = models.CharField(max_length=255, default='')
    fulltime_avg_goals_per_game_conceded_home = models.CharField(max_length=255, default='')
    fulltime_avg_goals_per_game_conceded_away = models.CharField(max_length=255, default='')
    
    fulltime_avg_goals_per_game_scored_total = models.CharField(max_length=255, default='')
    fulltime_avg_goals_per_game_scored_home = models.CharField(max_length=255, default='')
    fulltime_avg_goals_per_game_scored_away = models.CharField(max_length=255, default='')
    
    fulltime_avg_redcards_total = models.CharField(max_length=255, default='')
    fulltime_avg_redcards_home = models.CharField(max_length=255, default='')
    fulltime_avg_redcards_away = models.CharField(max_length=255, default='')
    
    fulltime_avg_yellowcards_total = models.CharField(max_length=255, default='')
    fulltime_avg_yellowcards_home = models.CharField(max_length=255, default='')
    fulltime_avg_yellowcards_away = models.CharField(max_length=255, default='')

    fulltime_biggest_defeat_total = models.CharField(max_length=255, default='')
    fulltime_biggest_defeat_home = models.CharField(max_length=255, default='')
    fulltime_biggest_defeat_away = models.CharField(max_length=255, default='')

    fulltime_biggest_victory_total = models.CharField(max_length=255, default='')
    fulltime_biggest_victory_home = models.CharField(max_length=255, default='')
    fulltime_biggest_victory_away = models.CharField(max_length=255, default='')

    fulltime_clean_sheet_total = models.CharField(max_length=255, default='')
    fulltime_clean_sheet_home = models.CharField(max_length=255, default='')
    fulltime_clean_sheet_away = models.CharField(max_length=255, default='')

    fulltime_corners_total = models.CharField(max_length=255, default='')
    fulltime_corners_home = models.CharField(max_length=255, default='')
    fulltime_corners_away = models.CharField(max_length=255, default='')

    fulltime_draw_total = models.CharField(max_length=255, default='')
    fulltime_draw_home = models.CharField(max_length=255, default='')
    fulltime_draw_away = models.CharField(max_length=255, default='')

    fulltime_failed_to_score_total = models.CharField(max_length=255, default='')
    fulltime_failed_to_score_home = models.CharField(max_length=255, default='')
    fulltime_failed_to_score_away = models.CharField(max_length=255, default='')

    fulltime_fouls_total = models.CharField(max_length=255, default='')
    fulltime_fouls_home = models.CharField(max_length=255, default='')
    fulltime_fouls_away = models.CharField(max_length=255, default='')

    fulltime_goals_against_total = models.CharField(max_length=255, default='')
    fulltime_goals_against_home = models.CharField(max_length=255, default='')
    fulltime_goals_against_away = models.CharField(max_length=255, default='')

    fulltime_goals_for_total = models.CharField(max_length=255, default='')
    fulltime_goals_for_home = models.CharField(max_length=255, default='')
    fulltime_goals_for_away = models.CharField(max_length=255, default='')

    fulltime_lost_total = models.CharField(max_length=255, default='')
    fulltime_lost_home = models.CharField(max_length=255, default='')
    fulltime_lost_away = models.CharField(max_length=255, default='')

    fulltime_offsides_total = models.CharField(max_length=255, default='')
    fulltime_offsides_home = models.CharField(max_length=255, default='')
    fulltime_offsides_away = models.CharField(max_length=255, default='')

    fulltime_possession_total = models.CharField(max_length=255, default='')
    fulltime_possession_home = models.CharField(max_length=255, default='')
    fulltime_possession_away = models.CharField(max_length=255, default='')

    fulltime_redcards_total = models.CharField(max_length=255, default='')
    fulltime_redcards_home = models.CharField(max_length=255, default='')
    fulltime_redcards_away = models.CharField(max_length=255, default='')

    fulltime_shotsOnGoal_total = models.CharField(max_length=255, default='')
    fulltime_shotsOnGoal_home = models.CharField(max_length=255, default='')
    fulltime_shotsOnGoal_away = models.CharField(max_length=255, default='')

    fulltime_shotsTotal_total = models.CharField(max_length=255, default='')
    fulltime_shotsTotal_home = models.CharField(max_length=255, default='')
    fulltime_shotsTotal_away = models.CharField(max_length=255, default='')

    fulltime_yellowcards_total = models.CharField(max_length=255, default='')
    fulltime_yellowcards_home = models.CharField(max_length=255, default='')
    fulltime_yellowcards_away = models.CharField(max_length=255, default='')

    fulltime_win_total = models.CharField(max_length=255, default='')
    fulltime_win_home = models.CharField(max_length=255, default='')
    fulltime_win_away = models.CharField(max_length=255, default='')
    
    firsthalf_avg_corners_total = models.CharField(max_length=255, default='')
    firsthalf_avg_corners_home = models.CharField(max_length=255, default='')
    firsthalf_avg_corners_away = models.CharField(max_length=255, default='')
    
    firsthalf_avg_first_goal_conceded_total = models.CharField(max_length=255, default='')
    firsthalf_avg_first_goal_conceded_home = models.CharField(max_length=255, default='')
    firsthalf_avg_first_goal_conceded_away = models.CharField(max_length=255, default='')
    
    firsthalf_avg_first_goal_scored_total = models.CharField(max_length=255, default='')
    firsthalf_avg_first_goal_scored_home = models.CharField(max_length=255, default='')
    firsthalf_avg_first_goal_scored_away = models.CharField(max_length=255, default='')
    
    firsthalf_avg_goals_per_game_conceded_total = models.CharField(max_length=255, default='')
    firsthalf_avg_goals_per_game_conceded_home = models.CharField(max_length=255, default='')
    firsthalf_avg_goals_per_game_conceded_away = models.CharField(max_length=255, default='')
    
    firsthalf_avg_goals_per_game_scored_total = models.CharField(max_length=255, default='')
    firsthalf_avg_goals_per_game_scored_home = models.CharField(max_length=255, default='')
    firsthalf_avg_goals_per_game_scored_away = models.CharField(max_length=255, default='')
    
    firsthalf_avg_redcards_total = models.CharField(max_length=255, default='')
    firsthalf_avg_redcards_home = models.CharField(max_length=255, default='')
    firsthalf_avg_redcards_away = models.CharField(max_length=255, default='')
    
    firsthalf_avg_yellowcards_total = models.CharField(max_length=255, default='')
    firsthalf_avg_yellowcards_home = models.CharField(max_length=255, default='')
    firsthalf_avg_yellowcards_away = models.CharField(max_length=255, default='')

    firsthalf_biggest_defeat_total = models.CharField(max_length=255, default='')
    firsthalf_biggest_defeat_home = models.CharField(max_length=255, default='')
    firsthalf_biggest_defeat_away = models.CharField(max_length=255, default='')

    firsthalf_biggest_victory_total = models.CharField(max_length=255, default='')
    firsthalf_biggest_victory_home = models.CharField(max_length=255, default='')
    firsthalf_biggest_victory_away = models.CharField(max_length=255, default='')

    firsthalf_clean_sheet_total = models.CharField(max_length=255, default='')
    firsthalf_clean_sheet_home = models.CharField(max_length=255, default='')
    firsthalf_clean_sheet_away = models.CharField(max_length=255, default='')

    firsthalf_corners_total = models.CharField(max_length=255, default='')
    firsthalf_corners_home = models.CharField(max_length=255, default='')
    firsthalf_corners_away = models.CharField(max_length=255, default='')

    firsthalf_draw_total = models.CharField(max_length=255, default='')
    firsthalf_draw_home = models.CharField(max_length=255, default='')
    firsthalf_draw_away = models.CharField(max_length=255, default='')

    firsthalf_failed_to_score_total = models.CharField(max_length=255, default='')
    firsthalf_failed_to_score_home = models.CharField(max_length=255, default='')
    firsthalf_failed_to_score_away = models.CharField(max_length=255, default='')

    firsthalf_fouls_total = models.CharField(max_length=255, default='')
    firsthalf_fouls_home = models.CharField(max_length=255, default='')
    firsthalf_fouls_away = models.CharField(max_length=255, default='')

    firsthalf_goals_against_total = models.CharField(max_length=255, default='')
    firsthalf_goals_against_home = models.CharField(max_length=255, default='')
    firsthalf_goals_against_away = models.CharField(max_length=255, default='')

    firsthalf_goals_for_total = models.CharField(max_length=255, default='')
    firsthalf_goals_for_home = models.CharField(max_length=255, default='')
    firsthalf_goals_for_away = models.CharField(max_length=255, default='')

    firsthalf_lost_total = models.CharField(max_length=255, default='')
    firsthalf_lost_home = models.CharField(max_length=255, default='')
    firsthalf_lost_away = models.CharField(max_length=255, default='')

    firsthalf_offsides_total = models.CharField(max_length=255, default='')
    firsthalf_offsides_home = models.CharField(max_length=255, default='')
    firsthalf_offsides_away = models.CharField(max_length=255, default='')

    firsthalf_possession_total = models.CharField(max_length=255, default='')
    firsthalf_possession_home = models.CharField(max_length=255, default='')
    firsthalf_possession_away = models.CharField(max_length=255, default='')

    firsthalf_redcards_total = models.CharField(max_length=255, default='')
    firsthalf_redcards_home = models.CharField(max_length=255, default='')
    firsthalf_redcards_away = models.CharField(max_length=255, default='')

    firsthalf_shotsOnGoal_total = models.CharField(max_length=255, default='')
    firsthalf_shotsOnGoal_home = models.CharField(max_length=255, default='')
    firsthalf_shotsOnGoal_away = models.CharField(max_length=255, default='')

    firsthalf_shotsTotal_total = models.CharField(max_length=255, default='')
    firsthalf_shotsTotal_home = models.CharField(max_length=255, default='')
    firsthalf_shotsTotal_away = models.CharField(max_length=255, default='')

    firsthalf_yellowcards_total = models.CharField(max_length=255, default='')
    firsthalf_yellowcards_home = models.CharField(max_length=255, default='')
    firsthalf_yellowcards_away = models.CharField(max_length=255, default='')

    firsthalf_win_total = models.CharField(max_length=255, default='')
    firsthalf_win_home = models.CharField(max_length=255, default='')
    firsthalf_win_away = models.CharField(max_length=255, default='')  


    secondhalf_avg_corners_total = models.CharField(max_length=255, default='')
    secondhalf_avg_corners_home = models.CharField(max_length=255, default='')
    secondhalf_avg_corners_away = models.CharField(max_length=255, default='')
    
    secondhalf_avg_first_goal_conceded_total = models.CharField(max_length=255, default='')
    secondhalf_avg_first_goal_conceded_home = models.CharField(max_length=255, default='')
    secondhalf_avg_first_goal_conceded_away = models.CharField(max_length=255, default='')
    
    secondhalf_avg_first_goal_scored_total = models.CharField(max_length=255, default='')
    secondhalf_avg_first_goal_scored_home = models.CharField(max_length=255, default='')
    secondhalf_avg_first_goal_scored_away = models.CharField(max_length=255, default='')
    
    secondhalf_avg_first_goal_scored_total = models.CharField(max_length=255, default='')
    secondhalf_avg_first_goal_scored_home = models.CharField(max_length=255, default='')
    secondhalf_avg_first_goal_scored_away = models.CharField(max_length=255, default='')
    
    secondhalf_avg_goals_per_game_conceded_total = models.CharField(max_length=255, default='')
    secondhalf_avg_goals_per_game_conceded_home = models.CharField(max_length=255, default='')
    secondhalf_avg_goals_per_game_conceded_away = models.CharField(max_length=255, default='')
    
    secondhalf_avg_goals_per_game_scored_total = models.CharField(max_length=255, default='')
    secondhalf_avg_goals_per_game_scored_home = models.CharField(max_length=255, default='')
    secondhalf_avg_goals_per_game_scored_away = models.CharField(max_length=255, default='')
    
    secondhalf_avg_redcards_total = models.CharField(max_length=255, default='')
    secondhalf_avg_redcards_home = models.CharField(max_length=255, default='')
    secondhalf_avg_redcards_away = models.CharField(max_length=255, default='')
    
    secondhalf_avg_yellowcards_total = models.CharField(max_length=255, default='')
    secondhalf_avg_yellowcards_home = models.CharField(max_length=255, default='')
    secondhalf_avg_yellowcards_away = models.CharField(max_length=255, default='')

    secondhalf_biggest_defeat_total = models.CharField(max_length=255, default='')
    secondhalf_biggest_defeat_home = models.CharField(max_length=255, default='')
    secondhalf_biggest_defeat_away = models.CharField(max_length=255, default='')

    secondhalf_biggest_victory_total = models.CharField(max_length=255, default='')
    secondhalf_biggest_victory_home = models.CharField(max_length=255, default='')
    secondhalf_biggest_victory_away = models.CharField(max_length=255, default='')

    secondhalf_clean_sheet_total = models.CharField(max_length=255, default='')
    secondhalf_clean_sheet_home = models.CharField(max_length=255, default='')
    secondhalf_clean_sheet_away = models.CharField(max_length=255, default='')

    secondhalf_corners_total = models.CharField(max_length=255, default='')
    secondhalf_corners_home = models.CharField(max_length=255, default='')
    secondhalf_corners_away = models.CharField(max_length=255, default='')

    secondhalf_draw_total = models.CharField(max_length=255, default='')
    secondhalf_draw_home = models.CharField(max_length=255, default='')
    secondhalf_draw_away = models.CharField(max_length=255, default='')

    secondhalf_failed_to_score_total = models.CharField(max_length=255, default='')
    secondhalf_failed_to_score_home = models.CharField(max_length=255, default='')
    secondhalf_failed_to_score_away = models.CharField(max_length=255, default='')

    secondhalf_fouls_total = models.CharField(max_length=255, default='')
    secondhalf_fouls_home = models.CharField(max_length=255, default='')
    secondhalf_fouls_away = models.CharField(max_length=255, default='')

    secondhalf_goals_against_total = models.CharField(max_length=255, default='')
    secondhalf_goals_against_home = models.CharField(max_length=255, default='')
    secondhalf_goals_against_away = models.CharField(max_length=255, default='')

    secondhalf_goals_for_total = models.CharField(max_length=255, default='')
    secondhalf_goals_for_home = models.CharField(max_length=255, default='')
    secondhalf_goals_for_away = models.CharField(max_length=255, default='')

    secondhalf_lost_total = models.CharField(max_length=255, default='')
    secondhalf_lost_home = models.CharField(max_length=255, default='')
    secondhalf_lost_away = models.CharField(max_length=255, default='')

    secondhalf_offsides_total = models.CharField(max_length=255, default='')
    secondhalf_offsides_home = models.CharField(max_length=255, default='')
    secondhalf_offsides_away = models.CharField(max_length=255, default='')

    secondhalf_possession_total = models.CharField(max_length=255, default='')
    secondhalf_possession_home = models.CharField(max_length=255, default='')
    secondhalf_possession_away = models.CharField(max_length=255, default='')

    secondhalf_redcards_total = models.CharField(max_length=255, default='')
    secondhalf_redcards_home = models.CharField(max_length=255, default='')
    secondhalf_redcards_away = models.CharField(max_length=255, default='')

    secondhalf_shotsOnGoal_total = models.CharField(max_length=255, default='')
    secondhalf_shotsOnGoal_home = models.CharField(max_length=255, default='')
    secondhalf_shotsOnGoal_away = models.CharField(max_length=255, default='')

    secondhalf_shotsTotal_total = models.CharField(max_length=255, default='')
    secondhalf_shotsTotal_home = models.CharField(max_length=255, default='')
    secondhalf_shotsTotal_away = models.CharField(max_length=255, default='')

    secondhalf_yellowcards_total = models.CharField(max_length=255, default='')
    secondhalf_yellowcards_home = models.CharField(max_length=255, default='')
    secondhalf_yellowcards_away = models.CharField(max_length=255, default='')

    secondhalf_win_total = models.CharField(max_length=255, default='')
    secondhalf_win_home = models.CharField(max_length=255, default='')
    secondhalf_win_away = models.CharField(max_length=255, default='')

    scoring_minutes  =models.TextField(null=True, blank=True)
    goals_conceded_minutes  =models.TextField(null=True, blank=True)
    redcard_minutes  =models.TextField(null=True, blank=True)

class TeamPlayerSidelineGoalserve(models.Model):
    class Meta:
        db_table = 'teamsplayer_sideline_goalserve'
    match_id = models.BigIntegerField(blank=True, null=True)
    id= models.CharField(max_length=512, default='',primary_key=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, default='')
    player_id = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=512, default='')
    start_date = models.CharField(max_length=255, default='')
    end_date = models.CharField(max_length=255, default='')

class TeamsTrophyGoalserve(models.Model):
    class Meta:
        db_table = 'teams_trophy_goalserve'
    
    id= models.CharField(max_length=512, default='',primary_key=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    count = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255, default='')
    league = models.CharField(max_length=512, default='')
    seasons = models.CharField(max_length=255, default='')
    status = models.CharField(max_length=255, default='')   
    
class TeamHeadtoHeadGoalserve(models.Model):
    class Meta:
        db_table = 'team_headtohead_goalserve'
    id= models.CharField(max_length=512, default='',primary_key=True)
    team1_id= models.BigIntegerField(blank=True, null=True)
    team2_id= models.BigIntegerField(blank=True, null=True)
    # top50= fields.ArrayField(models.UUIDField(), blank=True, default=list)
    # overall= fields.ArrayField(models.UUIDField(), blank=True, default=list)
    # leagues= fields.ArrayField(models.UUIDField(), blank=True, default=list)
    # goals= fields.ArrayField(models.UUIDField(), blank=True, default=list)
    # biggest_victory= fields.ArrayField(models.UUIDField(), blank=True, default=list)
    # biggest_defeat= fields.ArrayField(models.UUIDField(), blank=True, default=list)
    # last5_matches= fields.ArrayField(models.UUIDField(), blank=True, default=list)
    # h2h_probabilities= fields.ArrayField(models.UUIDField(), blank=True, default=list)
    # teamFormPoints= fields.ArrayField(models.UUIDField(), blank=True, default=list)
    # teamShotOnTarget= fields.ArrayField(models.UUIDField(), blank=True, default=list)
    # teamStandings= fields.ArrayField(models.UUIDField(), blank=True, default=list)
    
class TeamsWiseLeagueStatisticsToGoalserve(models.Model):
    class Meta:
        db_table = 'teams_wise_league_statistics_goalserve'
    
    id= models.CharField(max_length=512, default='',primary_key=True)
    team_id = models.BigIntegerField(blank=True, null=True)
    league_id = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    season = models.CharField(max_length=255, default='')
    
    fulltime_avg_corners_total = models.CharField(max_length=255, default='')
    fulltime_avg_corners_home = models.CharField(max_length=255, default='')
    fulltime_avg_corners_away = models.CharField(max_length=255, default='')
    fulltime_avg_first_goal_conceded =models.TextField(null=True, blank=True)
    fulltime_avg_first_goal_scored =models.TextField(null=True, blank=True)
    fulltime_avg_goals_per_game_conceded =models.TextField(null=True, blank=True)
    fulltime_avg_goals_per_game_scored =models.TextField(null=True, blank=True)
    fulltime_avg_redcards =models.TextField(null=True, blank=True)
    fulltime_avg_yellowcards =models.TextField(null=True, blank=True)
    fulltime_biggest_defeat =models.TextField(null=True, blank=True)
    fulltime_biggest_victory =models.TextField(null=True, blank=True)
    fulltime_clean_sheet_total =models.TextField(null=True, blank=True)
    fulltime_corners =models.TextField(null=True, blank=True)
    fulltime_draw =models.TextField(null=True, blank=True)
    fulltime_failed_to_score =models.TextField(null=True, blank=True)
    fulltime_fouls =models.TextField(null=True, blank=True)
    fulltime_goals_against =models.TextField(null=True, blank=True)
    fulltime_goals_for =models.TextField(null=True, blank=True)
    fulltime_lost =models.TextField(null=True, blank=True)
    fulltime_offsides =models.TextField(null=True, blank=True)
    fulltime_possession =models.TextField(null=True, blank=True)
    fulltime_redcards =models.TextField(null=True, blank=True)
    fulltime_shotsOnGoal_total =models.TextField(null=True, blank=True)
    fulltime_shotsTotal =models.TextField(null=True, blank=True)
    fulltime_yellowcards =models.TextField(null=True, blank=True)
    fulltime_win =models.TextField(null=True, blank=True)
    firsthalf_avg_corners =models.TextField(null=True, blank=True)
    firsthalf_avg_first_goal_conceded =models.TextField(null=True, blank=True)
    firsthalf_avg_first_goal_scored =models.TextField(null=True, blank=True)
    firsthalf_avg_goals_per_game_conceded =models.TextField(null=True, blank=True)
    firsthalf_avg_goals_per_game_scored =models.TextField(null=True, blank=True)
    firsthalf_avg_redcards =models.TextField(null=True, blank=True)
    firsthalf_avg_yellowcards =models.TextField(null=True, blank=True)
    firsthalf_biggest_defeat =models.TextField(null=True, blank=True)
    firsthalf_biggest_victory =models.TextField(null=True, blank=True)
    firsthalf_clean_sheet =models.TextField(null=True, blank=True)
    firsthalf_corners =models.TextField(null=True, blank=True)
    firsthalf_draw =models.TextField(null=True, blank=True)
    firsthalf_failed_to_score =models.TextField(null=True, blank=True)
    firsthalf_fouls =models.TextField(null=True, blank=True)
    firsthalf_goals_against =models.TextField(null=True, blank=True)
    firsthalf_goals_for =models.TextField(null=True, blank=True)

    firsthalf_lost =models.TextField(null=True, blank=True)

    firsthalf_offsides =models.TextField(null=True, blank=True)

    firsthalf_possession =models.TextField(null=True, blank=True)

    firsthalf_redcards =models.TextField(null=True, blank=True)

    firsthalf_shotsOnGoal =models.TextField(null=True, blank=True)

    firsthalf_shotsTotal =models.TextField(null=True, blank=True)

    firsthalf_yellowcards =models.TextField(null=True, blank=True)

    firsthalf_win =models.TextField(null=True, blank=True)

    secondhalf_avg_corners =models.TextField(null=True, blank=True)
    
    secondhalf_avg_first_goal_conceded =models.TextField(null=True, blank=True)
    
    secondhalf_avg_first_goal_scored =models.TextField(null=True, blank=True)
    
    
    secondhalf_avg_goals_per_game_conceded =models.TextField(null=True, blank=True)
    
    secondhalf_avg_goals_per_game_scored =models.TextField(null=True, blank=True)
    secondhalf_avg_redcards =models.TextField(null=True, blank=True)
    
    secondhalf_avg_yellowcards =models.TextField(null=True, blank=True)

    secondhalf_biggest_defeat =models.TextField(null=True, blank=True)

    secondhalf_biggest_victory =models.TextField(null=True, blank=True)

    secondhalf_clean_sheet =models.TextField(null=True, blank=True)

    secondhalf_corners =models.TextField(null=True, blank=True)

    secondhalf_draw =models.TextField(null=True, blank=True)

    secondhalf_failed_to_score =models.TextField(null=True, blank=True)

    secondhalf_fouls =models.TextField(null=True, blank=True)

    secondhalf_goals_against =models.TextField(null=True, blank=True)

    secondhalf_goals_for =models.TextField(null=True, blank=True)

    secondhalf_lost =models.TextField(null=True, blank=True)

    secondhalf_offsides =models.TextField(null=True, blank=True)

    secondhalf_possession =models.TextField(null=True, blank=True)

    secondhalf_redcards =models.TextField(null=True, blank=True)

    secondhalf_shotsOnGoal =models.TextField(null=True, blank=True)

    secondhalf_shotsTotal =models.TextField(null=True, blank=True)

    secondhalf_yellowcards =models.TextField(null=True, blank=True)

    secondhalf_win =models.TextField(null=True, blank=True)

    scoring_minutes  =models.TextField(null=True, blank=True)
    goals_conceded_minutes  =models.TextField(null=True, blank=True)
    redcard_minutes  =models.TextField(null=True, blank=True)

class PlayerGoalserve(models.Model):
    class Meta:
        db_table = 'player_goalserve'

    id= models.CharField(max_length=512, default='',primary_key=True)
    league_id = models.BigIntegerField(blank=True, null=True)
    league_name = models.CharField(max_length=255, default='')
    iscup = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255, default='')
    team_id = models.CharField(max_length=255, default='')    
    team_name = models.CharField(max_length=255, default='')    
    venue_id = models.CharField(max_length=255, default='')    
    venue_name = models.CharField(max_length=255, default='')    
    age = models.CharField(max_length=255, default='')    
    appearences = models.CharField(max_length=255, default='')    
    assists = models.CharField(max_length=255, default='')    
    blocks = models.CharField(max_length=255, default='')    
    clearances = models.CharField(max_length=255, default='')    
    crossesAccurate = models.CharField(max_length=255, default='')    
    crossesTotal = models.CharField(max_length=255, default='')    
    dispossesed = models.CharField(max_length=255, default='')    
    dribbleAttempts = models.CharField(max_length=255, default='')    
    dribbleSucc = models.CharField(max_length=255, default='')    
    duelsTotal = models.CharField(max_length=255, default='')    
    duelsWon = models.CharField(max_length=255, default='')    
    fouldDrawn = models.CharField(max_length=255, default='')    
    foulsCommitted = models.CharField(max_length=255, default='')    
    goals = models.CharField(max_length=255, default='')    
    goalsConceded = models.CharField(max_length=255, default='')    
    player_id = models.CharField(max_length=255, default='')    
    injured = models.CharField(max_length=255, default='')    
    insideBoxSaves = models.CharField(max_length=255, default='')    
    interceptions = models.CharField(max_length=255, default='')    
    isCaptain = models.CharField(max_length=255, default='')    
    keyPasses = models.CharField(max_length=255, default='')    
    lineups = models.CharField(max_length=255, default='')    
    minutes = models.CharField(max_length=255, default='')    
    name = models.CharField(max_length=255, default='')    
    number = models.CharField(max_length=255, default='')    
    pAccuracy = models.CharField(max_length=255, default='')    
    passes = models.CharField(max_length=255, default='')    
    penComm = models.CharField(max_length=255, default='')    
    penMissed = models.CharField(max_length=255, default='')    
    penSaved = models.CharField(max_length=255, default='')    
    penScored = models.CharField(max_length=255, default='')    
    penWon = models.CharField(max_length=255, default='')    
    position = models.CharField(max_length=255, default='')    
    rating = models.CharField(max_length=255, default='')    
    redcards = models.CharField(max_length=255, default='')    
    saves = models.CharField(max_length=255, default='')    
    shotsOn = models.CharField(max_length=255, default='')    
    shotsTotal = models.CharField(max_length=255, default='')    
    substitutes_on_bench = models.CharField(max_length=255, default='')    
    substitute_in = models.CharField(max_length=255, default='')    
    substitute_out = models.CharField(max_length=255, default='')    
    tackles = models.CharField(max_length=255, default='')    
    woordworks = models.CharField(max_length=255, default='')    
    yellowcards = models.CharField(max_length=255, default='')    
    yellowred = models.CharField(max_length=255, default='')

class PlayerStatisticsGoalserve(models.Model):
    class Meta:
        db_table = 'player_statistics_goalserve'

    id= models.CharField(max_length=512, default='',primary_key=True)
    player_id = models.CharField(max_length=255, default='')  
    category = models.CharField(max_length=255, default='')
    common_name = models.CharField(max_length=255, default='')
    age = models.CharField(max_length=255, default='')
    birthcountry = models.CharField(max_length=255, default='')
    birthdate = models.CharField(max_length=255, default='')
    birthplace = models.CharField(max_length=255, default='')
    firstname = models.CharField(max_length=255, default='')
    lastname = models.CharField(max_length=255, default='')
    height = models.CharField(max_length=255, default='')
    image = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, default='')
    nationality = models.CharField(max_length=255, default='')
    position = models.CharField(max_length=255, default='')
    weight = models.CharField(max_length=255, default='')
    team = models.CharField(max_length=255, default='')
    team_id = models.CharField(max_length=255, default='')
    
    statistics =  models.TextField(null=True, blank=True)
    statistic_club =  models.TextField(null=True, blank=True)
    statistic_popular_intl_club =  models.TextField(null=True, blank=True)
    statistic_international_club =  models.TextField(null=True, blank=True)
    overall_clubs =  models.TextField(null=True, blank=True)
    trophies =  models.TextField(null=True, blank=True)
    transfers =  models.TextField(null=True, blank=True)

class predictionH2HOddsGoalserve(models.Model):
    
    class Meta:
        db_table = 'prediction_h2h_odds_goalserve'
    id= models.CharField(max_length=512, default='',primary_key=True)
    match_id= models.BigIntegerField(blank=True, null=True)
    league_id= models.BigIntegerField(blank=True, null=True)
    match_name=models.CharField(max_length=255, default='')
    Home=models.CharField(max_length=255, default='')
    Away=models.CharField(max_length=255, default='')
    Predictions=models.CharField(max_length=255, default='')
    Home_score=models.CharField(max_length=255, default='')
    Away_score=models.CharField(max_length=255, default='')
    Probability=models.CharField(max_length=255, default='')
    under_2_5_goals_probability=models.CharField(max_length=255, default='')
    under_2_5_odds=models.CharField(max_length=255, default='')
    over_2_5_goals_probability=models.CharField(max_length=255, default='')
    over_2_5_odds=models.CharField(max_length=255, default='')
    home_handicap=models.CharField(max_length=255, default='')
    away_handicap=models.CharField(max_length=255, default='')
    
    prediction =models.CharField(max_length=255, default='')
    probability_percent_away_win=models.CharField(max_length=255, default='')
    probability_percent_draw=models.CharField(max_length=255, default='')
    probability_percent_home_win=models.CharField(max_length=255, default='')

    predicted_decimal_odds_away_odds=models.CharField(max_length=255, default='')
    predicted_decimal_odds_draw_odds=models.CharField(max_length=255, default='')
    predicted_decimal_odds_home_odds=models.CharField(max_length=255, default='')

    predicted_fractional_odds_away_odds=models.CharField(max_length=255, default='')
    predicted_fractional_odds_draw_odds=models.CharField(max_length=255, default='')
    predicted_fractional_odds_home_odds=models.CharField(max_length=255, default='')

    predicted_american_odds_away_odds=models.CharField(max_length=255, default='')
    predicted_american_odds_draw_odds=models.CharField(max_length=255, default='')
    predicted_american_odds_home_odds=models.CharField(max_length=255, default='')
    HST=models.CharField(max_length=255, default='')
    AST=models.CharField(max_length=255, default='')
    HTEloRatings=models.CharField(max_length=255, default='')
    ATEloRatings=models.CharField(max_length=255, default='')
    created = models.DateTimeField(auto_now_add=True)
    formated_date=models.DateTimeField(null=True)

class Banner(models.Model):
    class Meta:
        db_table = 'banner'
    id= models.CharField(max_length=512, default='',primary_key=True)
    title = models.CharField(max_length=255, default='')
    slug = models.CharField(max_length=255, default='')
    image = models.ImageField(upload_to='banner/', blank=True)
    description = models.TextField(null=True)
    is_active= models.BooleanField(default=False,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    class Meta:
        db_table = 'notification'
    id= models.CharField(max_length=512, default='',primary_key=True)
    slug = models.CharField(max_length=255, default='')    
    title = models.CharField(max_length=255, default='')
    description = models.TextField(null=True)
    is_active= models.BooleanField(default=False,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

class UserNotification(models.Model):
    class Meta:
        db_table = 'user_notification'
    id= models.CharField(max_length=512, default='',primary_key=True)
    notification_id = models.BigIntegerField(blank=True, null=True)    
    title = models.CharField(max_length=255, default='')
    description = models.TextField(null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    is_active= models.BooleanField(default=False,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

class UploadCSV(models.Model):
    class Meta:
        db_table = 'upload_csv'
    id= models.CharField(max_length=512, default='',primary_key=True)
    league = models.CharField(max_length=255, default='')
    csv_file = models.ImageField(upload_to='csv/', blank=True)
    is_active= models.BooleanField(default=False,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    is_process = models.BooleanField(default=False,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

class UploadExcel(models.Model):
    class Meta:
        db_table = 'upload_excel'
    id= models.CharField(max_length=512, default='',primary_key=True)
    league = models.CharField(max_length=255, default='')
    excel_file = models.ImageField(upload_to='excel/', blank=True)
    is_active= models.BooleanField(default=False,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    is_process = models.BooleanField(default=False,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
class SeasonsTennisSportrader(models.Model):
    class Meta:
        db_table = 'seasons_tennis_sportrader'
    id= models.CharField(max_length=512, default='',primary_key=True)
    season_id = models.CharField(max_length=512, default='')
    name = models.CharField(max_length=512, default='')
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    year = models.CharField(max_length=100, default='')
    competition_id = models.CharField(max_length=512, default='')
    is_active= models.BooleanField(default=False,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

class ComplexesTennisSportrader(models.Model):
    class Meta:
        db_table = 'tennis_complexes_sportrader'
    id= models.CharField(max_length=512, default='',primary_key=True)
    complexes_name = models.CharField(max_length=512, default='')
    complexes_id= models.CharField(max_length=512, default='')
    venues_id= models.CharField(max_length=512, default='')
    venues_name = models.CharField(max_length=512, default='')
    city_name= models.CharField(max_length=512, default='')
    country_name = models.CharField(max_length=512, default='')
    country_code = models.CharField(max_length=512, default='')
    is_active= models.BooleanField(default=False,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

class CompetitionsTennisSportrader(models.Model):
    class Meta:
        db_table = 'competitions_tennis_sportrader'
    
    id= models.CharField(max_length=512, default='',primary_key=True)
    competitions_name = models.CharField(max_length=512, default='')
    competitions_id= models.CharField(max_length=512, default='')
    competitions_type= models.CharField(max_length=512, default='')
    gender = models.CharField(max_length=512, default='')
    category_name = models.CharField(max_length=512, default='')
    category_id= models.CharField(max_length=512, default='')
    is_active= models.BooleanField(default=False,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

class TennisDataInputAI(models.Model):
    class Meta:
        db_table = 'tennis_data_input_ai'
    
    ai_id = models.CharField(max_length=512, default='',primary_key=True)
    player_one_id = models.CharField(max_length=512, default='')
    player_two_id = models.CharField(max_length=512, default='')
    player_one_name = models.CharField(max_length=512, default='')
    player_two_name = models.CharField(max_length=512, default='')
    surface_encoded = models.BigIntegerField(blank=True, null=True)
    player_one_ace = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    player_two_ace = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    player_one_df = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    player_two_df = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    player_one_rank = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    player_two_rank = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    player_one_rank_points = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    player_two_rank_points = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    player_one_elo_rating = models.CharField(max_length=512, default='')
    player_two_elo_rating = models.CharField(max_length=512, default='')
    
    is_active= models.BooleanField(default=False,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

class TennisEloRating(models.Model):
    class Meta:
        db_table = 'tennis_elo_rating'
    
    elo_id = models.CharField(max_length=512, default='',primary_key=True)
    player_id=models.CharField(max_length=512, default='')
    abbreviation = models.CharField(max_length=512, default='')
    country = models.CharField(max_length=512, default='')
    country_code = models.CharField(max_length=512, default='')
    player_name= models.CharField(max_length=512, default='')
    elo_rating= models.CharField(max_length=512, default='')
    is_active= models.BooleanField(default=False,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
class TennisSeasonCompitator(models.Model):
    class Meta:
        db_table = 'tennis_season_wise_compitator'
    
    tennis_season_wise_compitator_id = models.CharField(max_length=512, default='',primary_key=True)
    season_id = models.CharField(max_length=512, default='')
    compitator_id = models.CharField(max_length=512, default='')
    competitions_name = models.CharField(max_length=512, default='')
    short_name = models.CharField(max_length=512, default='')
    abbreviation = models.CharField(max_length=512, default='')
    is_active= models.BooleanField(default=False,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

#-------------------Sports Rader API--------------------

class SportsradarSoccerEloRating(models.Model):
    class Meta:
        db_table = 'league_competitor_elo_rating_sportsradar'
    
    compitator_id = models.CharField(max_length=512, default='',primary_key=True)
    sportsradar_competitor_id = models.CharField(max_length=512, default='')
    sportsradar_competitor_short_name = models.CharField(max_length=512, default='')
    clubelo_team_name = models.CharField(max_length=512, default='')
    betfair_team_name = models.CharField(max_length=512, default='')
    elo_rating = models.DecimalField(max_digits=15, decimal_places=8)
    form_points = models.CharField(max_length=512, default='')
    avg_shot_on_target = models.CharField(max_length=512, default='')
    Date = models.DateTimeField(auto_now_add=True)

class SportsradarMapping(models.Model):
    class Meta:
        db_table = 'league_competitor_mapping_sportsradar'
    
    sportsradar_competitor_id = models.CharField(max_length=512, default='')
    sportsradar_competitor_short_name = models.CharField(max_length=512, default='')
    clubelo_team_name = models.CharField(max_length=512, default='')
    betfair_team_name = models.CharField(max_length=512, default='')
    Date = models.DateTimeField(auto_now_add=True)

class LeagueSeasonCompetitorsSportsradar(models.Model):
    id =models.CharField(max_length=512, default='',primary_key=True)
    name = models.CharField(max_length=512, default='')
    short_name = models.CharField(max_length=512, default='')
    abbreviation = models.CharField(max_length=512, default='')
    season_id = models.CharField(max_length=512, default='')
    class Meta:
        db_table = 'league_season_competitors_sportsradar'

class LeagueSportsradar(models.Model):
    id = models.CharField(max_length=512, default='')
    competition_id = models.CharField(max_length=512, default='',primary_key=True)
    name = models.CharField(max_length=512, default='')
    gender = models.CharField(max_length=512, default='')
    parent_id = models.CharField(max_length=512, default='')
    category_id = models.CharField(max_length=512, default='')
    category_name = models.CharField(max_length=512, default='')
    country_code = models.CharField(max_length=512, default='')
    is_active = models.BooleanField(default=False,null=True,blank=True)
    class Meta:
        db_table = 'league_sportsradar'

class LeagueSeasonsSportsradar(models.Model):
    id = models.CharField(max_length=512, default='',primary_key=True)
    name = models.CharField(max_length=512, default='')
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    year = models.CharField(max_length=512, default='')
    competition_id = models.CharField(max_length=512, default='')
    class Meta:
        db_table = 'league_seasons_sportsradar'

class LeagueSeasonsScheduleSportsradar(models.Model):
    sport_event_id =models.CharField(max_length=512, default='',primary_key=True)
    sport_event_start_time = models.CharField(max_length=512, default='')
    sport_event_context_category_id = models.CharField(max_length=512, default='')
    sport_event_context_category_name =models.CharField(max_length=512, default='')
    sport_event_context_category_country_code=models.CharField(max_length=512, default='')
    sport_event_context_competition_id=models.CharField(max_length=512, default='')
    sport_event_context_competition_name=models.CharField(max_length=512, default='')
    sport_event_context_competition_gender=models.CharField(max_length=512, default='')
    sport_event_context_season_id=models.CharField(max_length=512, default='')
    sport_event_context_season_name =models.CharField(max_length=512, default='')

    sport_event_context_season_start_date=models.DateTimeField(null=True)
    sport_event_context_season_end_date=models.DateTimeField(null=True)
    sport_event_context_season_year=models.CharField(max_length=512, default='')

    sport_event_context_season_competition_id=models.CharField(max_length=512, default='')
    sport_event_context_stage_order=models.CharField(max_length=512, default='')
    sport_event_context_stage_type=models.CharField(max_length=512, default='')
    sport_event_context_stage_phase=models.CharField(max_length=512, default='')

    sport_event_context_stage_start_date=models.DateTimeField(null=True)
    sport_event_context_stage_end_date=models.DateTimeField(null=True)
    sport_event_context_stage_year=models.CharField(max_length=512, default='')

    sport_event_context_groups= models.TextField(null=True)
    sport_event_competitors= models.TextField(null=True)
    sport_event_venue= models.TextField(null=True)
    sport_event_status= models.TextField(null=True)
    
    class Meta:
        db_table = 'league_season_schedules_sportsradar'

class LeagueSeasonsCompetitorsProfileSportsradar(models.Model):
    competitor_id =models.CharField(max_length=512, default='',primary_key=True)
    competitor_name = models.CharField(max_length=512, default='')
    competitor_country = models.CharField(max_length=512, default='')
    competitor_country_code = models.CharField(max_length=512, default='')
    competitor_abbreviation = models.CharField(max_length=512, default='')
    competitor_gender = models.CharField(max_length=512, default='')
    category_id = models.CharField(max_length=512, default='')
    category_name = models.CharField(max_length=512, default='')
    category_country_code = models.CharField(max_length=512, default='')
    sport= models.TextField(null=True)
    jerseys= models.TextField(null=True)
    manager= models.TextField(null=True)
    venue= models.TextField(null=True)
    players= models.TextField(null=True)

    class Meta:
        db_table = 'league_season_competitors_profile_sportsradar'

class predictionOddsSportsradar(models.Model):
    
    class Meta:
        db_table = 'prediction_odds_sportsradar'
    match_id= models.CharField(max_length=512, default='',primary_key=True)
    country_code= models.CharField(max_length=255, default='')
    country_name=models.CharField(max_length=255, default='')
    competition_id= models.CharField(max_length=255, default='')
    competition_name=models.CharField(max_length=255, default='')
    home_team_id=models.CharField(max_length=255, default='')
    home_team_name=models.CharField(max_length=255, default='')
    away_team_id=models.CharField(max_length=255, default='')
    away_team_name=models.CharField(max_length=255, default='')
    competition_date=models.DateTimeField(null=True)

    Home_score=models.CharField(max_length=255, default='')
    Away_score=models.CharField(max_length=255, default='')

    Probability=models.CharField(max_length=255, default='')
    under_2_5_goals_probability=models.CharField(max_length=255, default='')
    under_2_5_odds=models.CharField(max_length=255, default='')
    over_2_5_goals_probability=models.CharField(max_length=255, default='')
    over_2_5_odds=models.CharField(max_length=255, default='')
    home_handicap=models.CharField(max_length=255, default='')
    away_handicap=models.CharField(max_length=255, default='')
    poision_prediction = models.CharField(max_length=255, default='')
    prediction = models.CharField(max_length=255, default='')
    probability_percent_away_win=models.CharField(max_length=255, default='')
    probability_percent_draw=models.CharField(max_length=255, default='')
    probability_percent_home_win=models.CharField(max_length=255, default='')
    predicted_decimal_odds_away_odds=models.CharField(max_length=255, default='')
    predicted_decimal_odds_draw_odds=models.CharField(max_length=255, default='')
    predicted_decimal_odds_home_odds=models.CharField(max_length=255, default='')
    predicted_fractional_odds_away_odds=models.CharField(max_length=255, default='')
    predicted_fractional_odds_draw_odds=models.CharField(max_length=255, default='')
    predicted_fractional_odds_home_odds=models.CharField(max_length=255, default='')
    predicted_american_odds_away_odds=models.CharField(max_length=255, default='')
    predicted_american_odds_draw_odds=models.CharField(max_length=255, default='')
    predicted_american_odds_home_odds=models.CharField(max_length=255, default='')
    ht_form_point=models.CharField(max_length=255, default='')
    at_form_point=models.CharField(max_length=255, default='')
    AVG_HST=models.CharField(max_length=255, default='')
    AVG_AST=models.CharField(max_length=255, default='')
    HTEloRatings=models.CharField(max_length=255, default='')
    ATEloRatings=models.CharField(max_length=255, default='')
    created = models.DateTimeField(auto_now_add=True)
    
class SportsradarTeamData(models.Model):
    class Meta:
        db_table = 'sportsradar_team_data'
    id = models.AutoField(primary_key=True)
    match_date = models.DateTimeField(null=True)
    competition_id= models.CharField(max_length=255, default='')
    competitor_id =models.CharField(max_length=512, default='')
    created = models.DateTimeField(auto_now_add=True)
    team_data= models.TextField(null=True)
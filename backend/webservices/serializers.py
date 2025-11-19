from rest_framework import serializers
from db_table.models import *
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.auth.password_validation import validate_password
from webservices.views.CommonFunction import *
from django.contrib.auth.hashers import make_password
import re

class ContactusSerializer(serializers.ModelSerializer):
    """ Serializer to represent the contactus model """
    class Meta:
        model = Contactus
        fields='__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Subscription model """
    class Meta:
        model = Subscriptions
        fields='__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields =["first_name","last_name","username","email","password"]
    def validate(self, attrs):
        username = attrs.get('username')
        email=attrs.get("email")
        password=attrs.get("password")
        if Users.objects.filter(username=username):
            raise serializers.ValidationError("username already exists")
        if Users.objects.filter(email=email):
            raise serializers.ValidationError("email already exists")
        errors = password_validation(password)
        if errors:
            raise serializers.ValidationError(errors)
        else:
            attrs["password"]=make_password(password)
        return super().validate(attrs)

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    retype_password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['new_password', "retype_password", 'token', 'uidb64']

    def validate(self, attrs):

        new_password = attrs.get('new_password')
        retype_password = attrs.get('retype_password')
        if new_password!=retype_password:
            raise serializers.ValidationError("passwords must be same")
        errors = password_validation(new_password)
        if errors:
            raise serializers.ValidationError(errors)
        else:
            attrs["new_password"]=make_password(attrs["new_password"])
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(id=user_id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed('The reset link is invalid', 401)
        user.password=attrs['new_password']
        user.save()
        return super().validate(attrs)

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


    def validate(self, attrs):
        password=attrs.get('new_password')
        errors = password_validation(password)
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(attrs)

def password_validation(password):
    return []
    # pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
    # result = re.findall(pattern, password)
    # if result:
    #     return []
    # else:
    #     return ["Should have minimum 8 characters.","Should have at least one number.","Should have at least one uppercase and one lowercase character.","Should have at least one special symbol."]

class ProfileSerializer(serializers.ModelSerializer):
    postal_code = serializers.IntegerField(required=False)
    address1 = serializers.CharField(required=False)
    address2 = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    mobile = serializers.IntegerField(required=False)
    photo = serializers.ImageField(required=False)
    class Meta:
        model = Users
        fields =["postal_code", "address1", "address2", "city", "country", "mobile", "photo"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        #fields =["username", "email","country","first_name",]
        fields='__all__'

class EditProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    postal_code = serializers.IntegerField(required=False)
    address1 = serializers.CharField(required=False)
    address2 = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    mobile = serializers.IntegerField(required=False)
    photo = serializers.ImageField(required=False)
    class Meta:
        model = Users
        fields =["first_name","last_name","postal_code", "address1", "address2", "city", "country", "mobile", "photo"]

class TeamDetailSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = Teams
        fields='__all__'
class TeamCountrySeasonSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Blogs model """
    country = serializers.SerializerMethodField(method_name= 'get_country')
    season = serializers.SerializerMethodField(method_name= 'get_season')
    class Meta:
        model = Teams
        fields='__all__'
    
    
    def get_country(self, player_obj):
        all_country = Countries.objects.all().filter(country_id=player_obj.country_id).first()
        if all_country:
            return  all_country.name
        else:
            return ''
    def get_season(self, player_obj):
        all_season = AllSeason.objects.all().filter(season_id=player_obj.season_id).first()
        if all_season:
            return  all_season.name
        else:
            return ''
class AllLeagueSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Leagues model """
    country = serializers.SerializerMethodField(method_name= 'get_country')
    class Meta:
        model = Leagues
        fields='__all__'

    def get_country(self, player_obj):
        all_country = Countries.objects.all().filter(country_id=player_obj.country_id).first()
        if all_country:
            return {'country_name': all_country.name,'country_logo_path':''}
        else:
            return {'country_name': '','country_logo_path':''}

class MatchFixtureUpdateSerializer(serializers.ModelSerializer):
    """ Serializer to represent the MatchFixtureUpdate model """
    class Meta:
        model = MatchFixtureUpdate
        fields='__all__'

class PlayersSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Players model """

    team = serializers.SerializerMethodField(method_name= 'get_team')
    # player = serializers.SerializerMethodField(method_name= 'get_playerstats')

    class Meta:
        model = Players
        fields = '__all__'

    def get_team(self, player_obj):
        all_team = Teams.objects.all().filter(team_id=player_obj.team_id).first()
        if all_team:
            return {'name': all_team.name,'logo_path':all_team.logo_path}
        else:
            return {'name': '','logo_path':''}
        

    # def get_playerstats(self, player_obj):
    #     try:
    #         player = PlayerStatistics.objects.filter(stats_player_id=player_obj.player_id)
    #         serializer1 = PlayerStatisticsSerializer(player)
    #         return serializer1.data
    #     except Players.DoesNotExist:
    #         return None

class SeasonSerializer(serializers.ModelSerializer):
    """ Serializer to represent theSeason model """
    class Meta:
        model =Season
        fields='__all__'

class AllPlayerSerializer(serializers.ModelSerializer):
    """ Serializer to represent Players model """
    class Meta:
        model =Players
        fields='__all__'

class CountrySerializer(serializers.ModelSerializer):
    """ Serializer to represent theCountries model """
    class Meta:
        model =Countries
        fields='__all__'

class BookmakerSerializer(serializers.ModelSerializer):
    """ Serializer to represent theBookmaker model """
    class Meta:
        model = Bookmaker
        fields='__all__'

class OddsdataSerializer(serializers.ModelSerializer):
    """ Serializer to represent theOddsdata model """
    class Meta:
        model = Oddsdata
        fields='__all__'


class OddsSerializer(serializers.ModelSerializer):
    """ Serializer to represent theOdds model """
    bookmaker = serializers.SerializerMethodField()
    oddsdata = serializers.SerializerMethodField()

    class Meta:
        model =Odds
        fields='__all__'

    def get_bookmaker(self, odds_obj):
        try:
            bookmaker = Bookmaker.objects.all().filter(parent_oddsid=odds_obj.id).first()
            serializer1 = BookmakerSerializer(bookmaker)
            return serializer1.data
        except IndexError:
            return None

    def get_oddsdata(self, odds_obj):
        try:
            oddsdata = Oddsdata.objects.all().filter(parent_oddsid=odds_obj.id).first()
            serializer1 = OddsdataSerializer(oddsdata)
            return serializer1.data
        except IndexError:
            return None


class PlayerStatisticsSerializer(serializers.ModelSerializer):
    """ Serializer to represent thePlayerStatistics model """

    # team = serializers.SerializerMethodField()
    # player = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()
    league = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    class Meta:
        model =PlayerStatistics
        fields='__all__'

    def get_team(self, player_obj):
        all_team = Teams.objects.all().filter(team_id=player_obj.team_id).first()
        if all_team:
            return {'name': all_team.name,'logo_path':all_team.logo_path}
        else:
            return {'name': '','logo_path':''}
    def get_league(self, player_obj):
        all_team = Leagues.objects.all().filter(league_id=player_obj.league_id).first()
        if all_team:
            return {'name': all_team.name,'logo_path':all_team.logo_path}
        else:
            return {'name': '','logo_path':''}
    def get_season(self, player_obj):
        all_team = Season.objects.all().filter(season_id=player_obj.season_id).first()
        if all_team:
            return all_team.name
        else:
            return ''

class LeaguesSerializer(serializers.ModelSerializer):
    """ Serializer to represent Players model """
    class Meta:
        model =Leagues
        fields='__all__'

class LeaguesPlayerSerializer(serializers.ModelSerializer):
    """ Serializer to represent Players model """
    class Meta:
        model =Leagues
        fields='__all__'

    def get_player(self, player_obj):
        try:
            player = Players.objects.get(player_id=player_obj.stats_player_id)
            serializer1 = PlayersSerializer(player)
            return serializer1.data
        except Players.DoesNotExist:
            return None

class HistoricDataSerializer(serializers.ModelSerializer):
    """ Serializer to represent the MatchSchedule model """
    class Meta:
        model = MatchFixtureUpdate
        fields='__all__'

    league = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
   
    def get_league(self, player_obj):
        all_team = Leagues.objects.all().filter(league_id=player_obj.league_id).first()
        if all_team:
            return {'name': all_team.name,'logo_path':all_team.logo_path}
        else:
            return {'name': '','logo_path':''}
    def get_season(self, player_obj):
        all_team = Season.objects.all().filter(season_id=player_obj.season_id).first()
        if all_team:
            return all_team.name
        else:
            return ''

class ThisweekMatchScheduleSerializer(serializers.ModelSerializer):
    """ Serializer to represent the ThisweekMatchSchedule model """
    class Meta:
        model = MatchFixtureUpdate
        fields='__all__'
    league = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()

    def get_league(self, player_obj):
        all_team = Leagues.objects.all().filter(league_id=player_obj.league_id).first()
        if all_team:
            return {'name': all_team.name, 'logo_path': all_team.logo_path}
        else:
            return {'name': '', 'logo_path': ''}

    def get_season(self, player_obj):
        all_team = Season.objects.all().filter(season_id=player_obj.season_id).first()
        if all_team:
            return all_team.name
        else:
            return ''

class MatchScheduleSerializer(serializers.ModelSerializer):
    """ Serializer to represent the MatchSchedule model """
    class Meta:
        model = MatchFixtureUpdate
        fields='__all__'

class FixerSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Fixure model """

    class Meta:
        model = Fixture
        fields='__all__'
    league = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    localteam = serializers.SerializerMethodField()
    visitorteam = serializers.SerializerMethodField()
    teamdetail = serializers.SerializerMethodField()
    def get_league(self, player_obj):
        all_team = Leagues.objects.all().filter(league_id=player_obj.league_id).first()
        if all_team:
            return {'name': all_team.name,'logo_path':all_team.logo_path}
        else:
            return {'name': '','logo_path':''}
    
    def get_season(self, player_obj):
        all_team = Season.objects.all().filter(season_id=player_obj.season_id).first()
        if all_team:
            return {'name': all_team.name,'stage_name':all_team.stage_name}
        else:
            return {'name': '','stage_name':''}
    
    def get_localteam(self, match_obj):
        all_team = Teams.objects.all().filter(team_id=match_obj.localteam_id).first()
        if all_team:
            return {'name': all_team.name,'logo_path':all_team.logo_path}
        else:
            return {'name': '','logo_path':''}

    def get_visitorteam(self, match_obj):
        all_team = Teams.objects.all().filter(team_id=match_obj.visitorteam_id).first()
        if all_team:
            return {'name': all_team.name,'logo_path':all_team.logo_path}
        else:
            return {'name': '','logo_path':''}
    def teamdetail(self, match_obj):
        all_team = TeamStatsDetails.objects.all().filter(team_id=match_obj.visitorteam_id).first()
        if all_team:
            return all_team
        else:
            return {'name': '','logo_path':''}
class FixtureSerializer(serializers.ModelSerializer):
    """ Serializer to represent the fixtureSchedule model """
    class Meta:
        model = Fixture
        fields='__all__'
    leage_name = serializers.SerializerMethodField()
    season_name = serializers.SerializerMethodField()
    localteam_name = serializers.SerializerMethodField()
    visitorteam_name = serializers.SerializerMethodField()
    match_name = serializers.SerializerMethodField()
    def get_leage_name(self, player_obj):
        all_team = Leagues.objects.all().filter(league_id=player_obj.league_id).first()
        if all_team:
            return all_team.name
        else:
            return ''
    def get_season_name(self, player_obj):
        all_team = Leagues.objects.all().filter(season_id=player_obj.season_id).first()
        if all_team:
            return all_team.name
        else:
            return ''
    def get_localteam_name(self, player_obj):
        all_team = Teams.objects.all().filter(team_id=player_obj.localteam_id).first()
        if all_team:
            return all_team.name
        else:
            return ''

    def get_visitorteam_name(self, player_obj):
        all_team = Teams.objects.all().filter(team_id=player_obj.visitorteam_id).first()
        if all_team:
            return all_team.name
        else:
            return ''

    def get_match_name(self,obj):
        localteam_name = self.get_localteam_name(obj)
        visitorteam_name = self.get_visitorteam_name(obj)
        return localteam_name + " vs " + visitorteam_name



# class AffiliateRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Affiliateusers
#         # fields = '__all__'
#         fields =["name","email","phone","country","password","confirm_password"]
#     def validate(self, attrs):
#         username = attrs.get('name')
#         email=attrs.get("email")
#         password=attrs.get("password")
#         confirm_password=attrs.get("confirm_password")
#         if Users.objects.filter(username=username):
#             raise serializers.ValidationError("username already exists")
#         if Users.objects.filter(email=email):
#             raise serializers.ValidationError("email already exists")
#         if password != confirm_password:
#             raise serializers.ValidationError("passwords must be same")
#         # errors = password_validation(password)
#         # if errors:
#         #     raise serializers.ValidationError(errors)
#         # else:
#         #     attrs["password"]=make_password(password)
#         return super().validate(attrs)

class AffiliateUserSerializer(serializers.ModelSerializer):
    """ Serializer to represent the AffiliateUser model """
    class Meta:
        model = AffiliateUser
        fields='__all__'


class CmsSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Cms model """
    class Meta:
        model = Cms
        fields='__all__'

class BlogsSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Blogs model """
    class Meta:
        model = Blogs
        fields='__all__'


class TeamSeasonStatsDetailsSerializer(serializers.ModelSerializer):
    from db_table.models import AllSeason
    from db_table.models import TeamStatsDetails
    
    """ Serializer to represent the TeamStatsDetails model """
    class Meta:
        model = TeamStatsDetails
        fields='__all__'
    season = serializers.SerializerMethodField()
    def get_season(self, teamS):
        # print(teamS.season_id)
        # print('----')
        all_team = AllSeason.objects.all().filter(season_id=teamS.season_id).first()
        if all_team:
            return all_team.name
        else:
            return ''

class UserSubscriptionPaymentSerializer(serializers.ModelSerializer):

    """Serializer to represent the UserSubscription model"""
    class Meta:
        model = UserSubscriptionPayment
        fields='__all__'

    subscriptions = serializers.SerializerMethodField()
    def get_subscriptions(self, subsc):
        # print(teamS.season_id)
        # print('----')
        all_team = Subscriptions.objects.all().filter(id=subsc.subscription_id).first()
        if all_team:
            return all_team.name
        else:
            return ''


class MessageSerializer(serializers.ModelSerializer):

    """Serializer to represent the UserSubscription model"""
    class Meta:
        model = Message
        fields='__all__'
    sendername = serializers.SerializerMethodField()
    receivername = serializers.SerializerMethodField()
    def get_sendername(self, smp):
        usrname = Users.objects.all().filter(id=smp.sender_id).first()
        if usrname:
            return usrname.username
        else:
            return ''

    def get_receivername(self, smp):
        usrname = Users.objects.all().filter(id=smp.receiver_id).first()
        if usrname:
            return usrname.username
        else:
            return ''

class TeamStatsDetailsTeamStatisticsSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Blogs model """
    class Meta:
        model = TeamStatistics
        fields='__all__'
    teamdetail = serializers.SerializerMethodField()
    
    def get_teamdetail(self, player_obj):
        all_team = TeamStatsDetails.objects.all().filter(team_id=player_obj.team_id).all()[:5]
        return (TeamStatsDetailsSerializer(all_team,many=True).data)

class SeasonMatchPlanSerializer(serializers.ModelSerializer):
    from db_table.models import SeasonMatchPlan
    class Meta:
        model = SeasonMatchPlan
        fields='__all__'
    league_name = serializers.SerializerMethodField()
    season_name = serializers.SerializerMethodField()
    home_team = serializers.SerializerMethodField()
    away_team = serializers.SerializerMethodField()
    match_name = serializers.SerializerMethodField()
    odd =serializers.SerializerMethodField()
    def get_league_name(self, smp):
        all_team = Leagues.objects.all().filter(league_id=smp.league_id,collection_datasource="www.worldfootball.net").first()
        if all_team:
            return all_team.name
        else:
            return ''
    def get_season_name(self, smp):
        all_team = AllSeason.objects.all().filter(season_id=smp.season_id,collection_datasource="www.worldfootball.net").first()
        if all_team:
            return all_team.name
        else:
            return ''
    def get_home_team(self, smp):
        all_team = Teams.objects.all().filter(team_id=smp.home_team_id,collection_datasource="www.worldfootball.net").first()
        if all_team:
            return all_team.name
        else:
            return ''
    def get_away_team(self, smp):
        all_team = Teams.objects.all().filter(team_id=smp.away_team_id,collection_datasource="www.worldfootball.net").first()
        if all_team:
            return all_team.name
        else:
            return ''
    def get_odd(self, smp):
        all_team = OddCalculation.objects.all().filter(match_id=smp.match_id,collection_datasource="www.worldfootball.net").first()
        # print(all_team.Home)
        if all_team:
            return {'HomeOdds': all_team.Home,'DrawOdds':all_team.Draw,'AwayOdds':all_team.Away}
        else:
            return ''
    def get_match_name(self,obj):
        localteam_name = self.get_home_team(obj)
        visitorteam_name = self.get_away_team(obj)
        return localteam_name + " vs " + visitorteam_name
    

class PlayerListSerializer(serializers.ModelSerializer):

    """Serializer to represent the UserSubscription model"""
    class Meta:
        model = PlayerList
        fields='__all__'
    team = serializers.SerializerMethodField(method_name= 'get_team')

    def get_team(self, player_obj):
        all_team = Teams.objects.all().filter(team_id=player_obj.now_team_id).first()
        if all_team:
            return {'name': all_team.name,'logo_path':all_team.logo_path}
        else:
            return {'name': '','logo_path':''}
class PlayerCareerSerializer(serializers.ModelSerializer):

    """Serializer to represent the PlayerCareer model"""
    class Meta:
        model = PlayerCareer
        fields='__all__'

class AllSeasonSerializer(serializers.ModelSerializer):

    """Serializer to represent the AllSeason model"""
    class Meta:
        model = AllSeason
        fields='__all__'
class PlayerCareerDetailSerializer(serializers.ModelSerializer):
    """ Serializer to represent thePlayerStatistics model """

    # team = serializers.SerializerMethodField()
    # player = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()
    league = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    class Meta:
        model =PlayerCareer
        fields='__all__'

    def get_team(self, player_obj):
        all_team = Teams.objects.all().filter(team_id=player_obj.team_id).first()
        if all_team:
            return {'name': all_team.name,'logo_path':all_team.logo_path}
        else:
            return {'name': '','logo_path':''}
    def get_league(self, player_obj):
        all_team = Leagues.objects.all().filter(league_id=player_obj.league_id).first()
        if all_team:
            return {'name': all_team.league_dname,'logo_path':all_team.logo_path}
        else:
            return {'name': '','logo_path':''}
    def get_season(self, player_obj):
        all_team = AllSeason.objects.all().filter(season_id=player_obj.season_id).first()
        if all_team:
            return all_team.name
        else:
            return ''

class OvaralTeamTeamDetailSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Fixure model """

    class Meta:
        model = MatchFixtureUpdate
        fields='__all__'
    
    localteam_name = serializers.SerializerMethodField()
    visitorteam_name = serializers.SerializerMethodField()
   
    def get_localteam_name(self, player_obj):
        all_team = Teams.objects.all().filter(team_id=player_obj.localteam_id).first()
        if all_team:
            return all_team.name
        else:
            return ''

    def get_visitorteam_name(self, player_obj):
        all_team = Teams.objects.all().filter(team_id=player_obj.visitorteam_id).first()
        if all_team:
            return all_team.name
        else:
            return ''

class CreamTeamSerializer(serializers.ModelSerializer):
    """ Serializer to represent thePlayerStatistics model """

    # team = serializers.SerializerMethodField()
    # player = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    class Meta:
        model =PlayerCareer
        fields='__all__'

    def get_team(self, player_obj):
        all_team = Teams.objects.all().filter(team_id=player_obj.team_id).first()
        if all_team:
            return {'name': all_team.name,'logo_path':all_team.logo_path}
        else:
            return {'name': '','logo_path':''}
    def get_season(self, player_obj):
        all_team = AllSeason.objects.all().filter(season_id=player_obj.season_id).first()
        if all_team:
            return all_team.name
        else:
            return ''

class MatchNameSerializer(serializers.ModelSerializer):
    from db_table.models import SeasonMatchPlan
    class Meta:
        model = SeasonMatchPlan
        fields='__all__'
    league_name = serializers.SerializerMethodField()
    season_name = serializers.SerializerMethodField()
    home_team = serializers.SerializerMethodField()
    away_team = serializers.SerializerMethodField()
    match_name = serializers.SerializerMethodField()
    
    def get_league_name(self, smp):
        all_team = Leagues.objects.all().filter(league_id=smp.league_id,collection_datasource="www.worldfootball.net").first()
        if all_team:
            return all_team.name
        else:
            return ''
    def get_season_name(self, smp):
        all_team = AllSeason.objects.all().filter(season_id=smp.season_id,collection_datasource="www.worldfootball.net").first()
        if all_team:
            return all_team.name
        else:
            return ''
    def get_home_team(self, smp):
        all_team = Teams.objects.all().filter(team_id=smp.home_team_id,collection_datasource="www.worldfootball.net").first()
        if all_team:
            return all_team.name
        else:
            return ''
    def get_away_team(self, smp):
        all_team = Teams.objects.all().filter(team_id=smp.away_team_id,collection_datasource="www.worldfootball.net").first()
        if all_team:
            return all_team.name
        else:
            return ''
    def get_match_name(self,obj):
        localteam_name = self.get_home_team(obj)
        visitorteam_name = self.get_away_team(obj)
        return localteam_name + " vs " + visitorteam_name
    
class ScrapToolSerializer(serializers.ModelSerializer):

    """Serializer to represent the UserSubscription model"""
    class Meta:
        model = ScrapTool
        fields='__all__'

class SeasonWiseTeamDetailSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Fixure model """

    class Meta:
        model = MatchFixtureUpdate
        fields='__all__'
    
    localteam_name = serializers.SerializerMethodField()
    visitorteam_name = serializers.SerializerMethodField()
    winnerteam_name = serializers.SerializerMethodField()
   
    def get_localteam_name(self, player_obj):
        goal =0
        total_match =[]
        total_win = []
        total_draw = []
        total_lost = []
        goal_for =[]
        goals_against =[]
        
        all_team = Teams.objects.all().filter(team_id=player_obj.localteam_id).first()
        teamDetail = TeamStatsDetails.objects.all().filter(team_id=player_obj.localteam_id).first()
        if teamDetail:
            total_win = json.loads(teamDetail.win)
            total_draw = json.loads(teamDetail.draw)
            total_lost = json.loads(teamDetail.lost)
            total_match = total_win['total'] + total_draw['total'] + total_lost['total']
            goal_for = json.loads(teamDetail.goals_for)
            goals_against=json.loads(teamDetail.goals_against)
        if all_team:
           
            return {'name': all_team.name,'win':total_win,'draw':total_draw,'lost':total_lost,'goal_for':goal_for,'goals_against':goals_against} 
        else:
            return {'name': '','win':total_win,'draw':total_draw,'lost':total_lost,'goal_for':goal_for,'goals_against':goals_against} 

    def get_visitorteam_name(self, player_obj):
        goal =0
        total_match =[]
        total_win = []
        total_draw = []
        total_lost = []
        goal_for =[]
        goals_against =[]
        
        all_team = Teams.objects.all().filter(team_id=player_obj.visitorteam_id).first()
        teamDetail = TeamStatsDetails.objects.all().filter(team_id=player_obj.visitorteam_id).first()
        if teamDetail:
            total_win = json.loads(teamDetail.win)
            total_draw = json.loads(teamDetail.draw)
            total_lost = json.loads(teamDetail.lost)
            total_match = total_win['total'] + total_draw['total'] + total_lost['total']
            goal_for = json.loads(teamDetail.goals_for)
            goals_against=json.loads(teamDetail.goals_against)
        if all_team:
           
            return {'name': all_team.name,'win':total_win,'draw':total_draw,'lost':total_lost,'goal_for':goal_for,'goals_against':goals_against} 
        else:
            return {'name': '','win':total_win,'draw':total_draw,'lost':total_lost,'goal_for':goal_for,'goals_against':goals_against} 

    def get_winnerteam_name(self, player_obj):
        all_team = Teams.objects.all().filter(team_id=player_obj.winnerteam_id).first()
        if all_team:
            return all_team.name
        else:
            return ''

class TeamStatsDetailsSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = TeamStatsDetails
        fields='__all__'
        
class TeamAndTeamStatisticsDetailSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Blogs model """
    class Meta:
        model = Teams
        fields='__all__'
    
    teamdetail = serializers.SerializerMethodField()    
    def get_teamdetail(self, player_obj):
        all_team = TeamStatsDetails.objects.all().filter(team_id=player_obj.team_id).all()
        return (TeamStatsDetailsSerializer(all_team,many=True).data)

class HistoricDataSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = HistoricData
        fields='__all__'

class LeagueGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = LeagueGoalserve
        fields='__all__'

class SeasonGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = SeasonGoalserve
        fields='__all__'

class MatchGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = MatchGoalserve
        fields='__all__'

class TeamStatisticsGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = TeamStatisticsGoalserve
        fields='__all__'

class TeamPlayerSquadGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = TeamPlayerSquadGoalserve
        fields='__all__'

class MatchByTeamGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = MatchGoalserve
        fields='__all__'
    localteam = serializers.SerializerMethodField()
    visitorteam = serializers.SerializerMethodField()

    def get_localteam(self, player_obj):
        print('localteam_id',player_obj.localteam_id)
        localteamDetail = TeamStatisticsGoalserve.objects.all().filter(team_id=int(player_obj.localteam_id))[:1]
        if localteamDetail:
            return (TeamStatisticsGoalserveSerializer(localteamDetail,many=True).data)
        else:
            return ''

    def get_visitorteam(self, player_obj):
        print('visitorteam_id')
        visitorteamDetail = TeamStatisticsGoalserve.objects.all().filter(team_id=int(player_obj.visitorteam_id))[:1]
        if visitorteamDetail:
            print(player_obj.visitorteam_id)
            print(visitorteamDetail)
            return (TeamStatisticsGoalserveSerializer(visitorteamDetail,many=True).data)
        else:
            return ''
class MatchByTeamGoalserveSerializerOptional(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = MatchGoalserve
        fields='__all__'
    localteam = serializers.SerializerMethodField()
    visitorteam = serializers.SerializerMethodField()

    def get_localteam(self, player_obj):
        print('localteam_id',player_obj.localteam_id)
        localteamDetail = TeamStatisticsGoalserve.objects.all().filter(team_id=int(player_obj.localteam_id)).first()
        if localteamDetail:
            
            return ({'name':localteamDetail.name,'image':localteamDetail.image,'venue_name':localteamDetail.venue_name,'venue_address':localteamDetail.venue_city})
        else:
             return ({'name':'','image':'','venue_name':'','venue_city':'','venue_address':''})

    def get_visitorteam(self, player_obj):
        print('visitorteam_id')
        visitorteamDetail = TeamStatisticsGoalserve.objects.all().filter(team_id=int(player_obj.visitorteam_id)).first()
        if visitorteamDetail:
            print(player_obj.visitorteam_id)
            print(visitorteamDetail)
            return ({'name':visitorteamDetail.name,'image':visitorteamDetail.image,'venue_name':visitorteamDetail.venue_name,'venue_address':visitorteamDetail.venue_city})
        else:
             return ({'name':'','image':'','venue_name':'','venue_city':'','venue_address':''})
class TeamPlayerTransferINGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = TeamPlayerTransferINGoalserve
        fields='__all__'

class TeamPlayerTransferOutGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = TeamPlayerTransferOUTGoalserve
        fields='__all__'


class TeamHeadtoHeadGoalserveGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = TeamHeadtoHeadGoalserve
        fields='__all__'


class LeagueGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = LeagueGoalserve
        fields='__all__'

class PlayerGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = PlayerGoalserve
        fields='__all__'
class PlayerStatisticsGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = PlayerStatisticsGoalserve
        fields='__all__'
    teamimage = serializers.SerializerMethodField()
    
    def get_teamimage(self, player_obj):
        teamDetail = TeamStatisticsGoalserve.objects.all().filter(team_id=player_obj.team_id)[:1]
        if teamDetail:
            return teamDetail[0].image

        else:
            return ''

class predictionH2HOddsGoalserveSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = predictionH2HOddsGoalserve
        fields='__all__'

class BannerSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = Banner
        fields='__all__'          

class NotificationSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = Notification
        fields='__all__' 

class UploadCSVSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = UploadCSV
        fields='__all__' 

class EloRatingSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Team model """
    class Meta:
        model = TennisEloRating
        fields='__all__' 

class SportsradarMappingSerializer(serializers.ModelSerializer):
    """ Serializer to represent the SportsradarMapping model """
    class Meta:
        model = SportsradarMapping
        fields='__all__'

class SportsradarSoccerEloRatingSerializer(serializers.ModelSerializer):
    """ Serializer to represent the SportsradarMapping model """
    class Meta:
        model = SportsradarSoccerEloRating
        fields='__all__'

class SportsradarTeamDataSerializer(serializers.ModelSerializer):
    """ Serializer to represent the SportsradarMapping model """
    class Meta:
        model = SportsradarTeamData
        fields='__all__'

class PlaceOrdersBetfairSerializer(serializers.ModelSerializer):
    """ Serializer to represent the SportsradarMapping model """
    class Meta:
        model = PlaceOrdersBetfair
        fields='__all__'        
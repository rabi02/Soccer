from django.contrib import admin
from db_table.models import *
from db_table.forms import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from django.utils.html import format_html
# from rest_framwork import serializers
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils.html import format_html
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.urls import path
from django.shortcuts import render,redirect
from django.db.models import Q
from BetfairUpdater.SoccerCalculation import *
# user manager
@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'date_joined', 'last_login', 'is_active')
    list_filter = ('is_active','is_verifed_email')
    search_fields = ['first_name','email' ]
    ordering = ("email",)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'username')}),
        ('User type', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        ('Location Information', {'fields': ('postal_code', 'address1','address2','city','country','mobile','photo')}),
        ('Group', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
        ('email verification', {'fields': ('is_verifed_email',)}),
        ('notification', {'fields': ('email_notification','sms_notification','whatsapp_notification','phone_notification','site_notification')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('Add  User', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # def image_tag(self, obj):
    #     return format_html('<img src="{}" />'.format(obj.photo))
    #
    # image_tag.short_description = 'Image'



    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = Users.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:

            obj.set_password(obj.password)
        obj.save()

from django.contrib.auth.models import User, Group
admin.site.unregister(Group)



# from rest_framework.authtoken.models import Token
# admin.site.unregister(Token)

# from rest_framework.authtoken.models import TokenProxy
# admin.site.unregister(TokenProxy)

#Country manager
class CountriesModelAdmin(admin.ModelAdmin):
    model = Countries
    list_display = ('name', 'continent', 'sub_region', 'world_region', 'longitude','latitude')
    list_filter = ('continent','name',)
    search_fields = ['name', ]
    # list_per_page = 10

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    # fields = ('country_id', 'name', 'image_path', 'continent', 'sub_region',
    #                     'world_region', 'fifa', 'iso', 'iso2', 'longitude', 'latitude', 'flag')


# Leagues manager
def active_true(modeladmin,request,queryset):
    queryset.update(active=True)
active_true.short_description = "Publlish"
def active_false(modeladmin,request,queryset):
    queryset.update(active=False)
active_false.short_description = "Unpublish"

class LeaguesModelAdmin(admin.ModelAdmin):
    model = Leagues
    list_display = ('image_tag', 'name', 'slug_name','active')
    list_filter = ('active',)
    search_fields = ['name',]
    actions = (active_true, active_false)

    def image_tag(self, obj):
        return format_html('<img src="{}" width="60px" height="60px" />'.format(obj.logo_path))

    image_tag.short_description = 'Image'

    # def country(self, obj):
    #     try:
    #         country_id = obj.country_id
    #         country = Countries.objects.get(country_id=country_id)
    #         return country.name
    #     except:
    #         return None
    #     # except Countries.ObjectDoesNotExist:
    #     #     return None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs=super(LeaguesModelAdmin, self).get_queryset(request)
        # print(datetime.today().strftime('%Y-%m-%d'))
        return qs.filter(collection_datasource="www.worldfootball.net",name__isnull=False)

# Team manager
def active_true(modeladmin,request,queryset):
    queryset.update(is_active=True)
active_true.short_description = "Publlish"
def active_false(modeladmin,request,queryset):
    queryset.update(is_active=False)
active_false.short_description = "Unpublish"

class TeamsModelAdmin(admin.ModelAdmin):
    model = Teams
    list_display = ('team_id','image_tag', 'name', 'league','is_active','probability')
    list_filter = ('is_active',)
    search_fields = ['name', ]
    actions = (active_true, active_false)

    def image_tag(self, obj):
        return format_html('<img src="{}" width="60px" height="60px"/>'.format(obj.logo_path))

    image_tag.short_description = 'Image'

    def country(self, obj):
        try:
            country_id = obj.country_id
            country = Countries.objects.get(country_id=country_id)
            return country.name
        except:
            return None
    def league(self, obj):
        try:
            league_id = obj.league_id
            league = Leagues.objects.get(league_id=league_id)
            return league.name
        except:
            return None       
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    def get_queryset(self, request):
        qs=super(TeamsModelAdmin, self).get_queryset(request)
        # print(datetime.today().strftime('%Y-%m-%d'))
        return qs.filter(collection_datasource="www.worldfootball.net",league_id__isnull=False) 
    def probability(self, obj):
        url = '/admin/db_table/probability/'+ str(obj.team_id)
        return format_html(
            
            '<a class="button" href="'+url+'">probability</a>',
            
        )

    probability.short_description = "Probability"
    probability.allow_tags = True
 

# Player manager
def active_true(modeladmin,request,queryset):
    queryset.update(is_active=True)
active_true.short_description = "Publlish"
def active_false(modeladmin,request,queryset):
    queryset.update(is_active=False)
active_false.short_description = "Unpublish"

class PlayersModelAdmin(admin.ModelAdmin):
    model = Players
    list_display = ('image_tag', 'fullname', 'country','is_active')
    list_filter = ('is_active',)
    search_fields = ['fullname', ]
    actions = (active_true, active_false)
    # fields = ('image_tag',)
    # readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        return format_html('<img src="{}" width="60px" height="60px"/>'.format(obj.image_path))

    def country(self, obj):
        return obj.nationality

    image_tag.short_description = 'Image'
    country.short_description = 'Country'


    # list_display = ['image_tag', ]

    # def status(self, obj):
    #     status = obj.is_active
    #     return status


    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# Match popular

# import datetime
# from django.utils import timezone
# from django.contrib import admin
# from django.contrib.admin.filters import DateFieldListFilter
# from django.utils.translation import gettext_lazy as _
#
#
# class MyDateTimeFilter(DateFieldListFilter):
#     def __init__(self, *args, **kwargs):
#         super(MyDateTimeFilter, self).__init__(*args, **kwargs)
#
#         now = timezone.now()
#         # When time zone support is enabled, convert "now" to the user's time
#         # zone so Django's definition of "Today" matches what the user expects.
#         if timezone.is_aware(now):
#             now = timezone.localtime(now)
#
#         today = now.date()
#
#         self.links += ((
#             (_('Next 7 days'), {
#                 self.lookup_kwarg_since: str(today),
#                 self.lookup_kwarg_until: str(today + datetime.timedelta(days=7)),
#             }),
#         ))

# class BookAdmin(admin.ModelAdmin):
#     list_filter = (
#         ('published_at', MyDateTimeFilter),
#     )
def popular_true(modeladmin,request,queryset):
    queryset.update(is_popular=True)
popular_true.short_description = "Popular"
def popular_false(modeladmin,request,queryset):
    queryset.update(is_popular=False)
popular_false.short_description = "Unpopular"

class MatchModelAdmin(admin.ModelAdmin):
    model = MatchFixtureUpdate
    list_display = ('matchid','match_name','league_name','country_name','time_date','is_popular')
    # list_filter = (('time_date', MyDateTimeFilter),'is_popular')
    list_filter = ('is_popular',)
    # search_fields = ['matchid', ]
    actions = (popular_true, popular_false)

    # def date(self,obj):
    #     return obj.created_at
    # def get_queryset(self,request):
    #     qs=super(MatchModelAdmin, self).get_queryset(request)
    #     one_week_ago = datetime.today() + timedelta(days=7)
    #     return qs.filter(time_date__gte=datetime.today(),time_date__lte=one_week_ago)

    def league_name(self,obj):
        try:
            league_id=obj.league_id
            
            league=Leagues.objects.get(~Q(collection_datasource='www.worldfootball.net'),Q(league_id=league_id))
            return league.name
        except AttributeError:
            return None
       

    def country_name(self,obj):
        try:
            league_id=obj.league_id
            league=Leagues.objects.get(~Q(collection_datasource='www.worldfootball.net'),Q(league_id=league_id))
            country_id=league.country_id
            country = Countries.objects.get(country_id=country_id)
            return country.name
        except AttributeError:
            return None
        # except Leagues.ObjectDoesNotExist:
        #     return None

    def match_name(self,obj):
        try:
            lid=obj.localteam_id
            vid=obj.visitorteam_id
            team1=Teams.objects.filter(team_id=lid).first()
            team2=Teams.objects.filter(team_id=vid).first()
            if team1 and team2:
                return (team1.name) + " vs " + (team2.name)
            else:
                return None
        except AttributeError:
            return None



    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class BetslipModelAdmin(MatchModelAdmin):
    list_display = ('matchid', 'match_name','season_name', 'league_name', 'country_name', 'time_date', 'action')
    list_filter = ['matchid',]
    search_fields = ['matchid',]
    # actions = ()

    def season_name(self, obj):
        try:
            season_id = obj.season_id
            season = Season.objects.get(season_id=season_id)
            return season.name
        except:
            return None

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:matchid>/betslipview/',
                self.admin_site.admin_view(self.betslip_action),
                name='account-bet',
            ),
            # url(
            #     r'^(?P<account_id>.+)/withdraw/$',
            #     self.admin_site.admin_view(self.process_withdraw),
            #     name='account-withdraw',
            # ),
        ]
        return custom_urls + urls

    def action(self, obj):
        return format_html(
            # '<a class="button" href="{}">Deposit</a>&nbsp;'
            '<a class="button" href="{}">Bet slip</a>',
            reverse('admin:account-bet', args=[obj.pk]),
            # reverse('admin:account-withdraw', args=[obj.pk]),
        )

    action.short_description = 'Generate'
    action.allow_tags = True

    def betslip_action(self, request, matchid, *args, **kwargs):
        return render(request,'admin/betslip.html')
        #     self.process_action(
        #     request=request,
        #     matchid=matchid,
        #     # action_form=DepositForm,
        #     # action_title='Deposit',
        # )

    def get_queryset(self, request):
        from datetime import datetime
        qs=super(MatchModelAdmin, self).get_queryset(request)
        one_week_ago = datetime.today() + timedelta(days=7)
        return qs.filter(time_date__gte=datetime.today(),time_date__lte=one_week_ago)


    # def has_add_permission(self, request):
    #     return True
    #
    # def has_delete_permission(self, request, obj=None):
    #     return True
    #
    # def has_change_permission(self, request, obj=None):
    #     return True

    # def get_queryset(self, request):
    #     return self.model.objects.filter(user = request.user)

# Season manager
def active_true(modeladmin,request,queryset):
    queryset.update(is_active=True)
active_true.short_description = "Publlish"
def active_false(modeladmin,request,queryset):
    queryset.update(is_active=False)
active_false.short_description = "Unpublish"

class SeasonModelAdmin(admin.ModelAdmin):
    model = Season
    list_display = ('name', 'league', 'round_name', 'type', 'is_active')
    list_filter = ('is_active',)
    search_fields = ['name',]
    actions = (active_true, active_false)

    def league(self, obj):
        try:
            league_id = obj.league_id
            league = Leagues.objects.get(league_id=league_id)
            return league.name
        except:
            return None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

from django.contrib import messages

# Then, when you need to error the user:
# messages.error(request, "The message")
#Subscription
def active_true(modeladmin,request,queryset):
    if Subscriptions.objects.filter(is_active=True):
        queryset.update(is_active=False)
        messages.error(request, "Subscriptions can't have more than 1 active contact at same time.")
        # raise ValidationError("Subscriptions can't have more than 1 active contact at same time.")
    else:
        queryset.update(is_active=True)
active_true.short_description = "Active"
def active_false(modeladmin,request,queryset):
    queryset.update(is_active=False)
active_false.short_description = "Inactive"
class SubscriptionModelAdmin(admin.ModelAdmin):
    model = Subscriptions
    fields = ('name', 'price')
    list_display = ('id', 'name', 'price', 'created_at','is_active')
    list_filter = ('is_active',)
    search_fields = ['name', ]
    actions = (active_true, active_false)

    # def active(self, obj):
    #     return obj.is_active == 1
    #
    # active.boolean = True

#Blogs(news)
def active_true(modeladmin,request,queryset):
    queryset.update(is_published=True)
active_true.short_description = "Publlish"
def active_false(modeladmin,request,queryset):
    queryset.update(is_published=False)
active_false.short_description = "Unpublish"
class BlogsModelAdmin(admin.ModelAdmin):
    model = Blogs
    list_display = ('title', 'slug', 'less_description','is_published')
    list_filter = ('is_published','is_blocked')
    search_fields = ['title','slug' ]
    actions = (active_true, active_false)

    def less_description(self,obj):
        # print(obj)
        return obj.description[:100]


#Cms
def active_true(modeladmin,request,queryset):
    queryset.update(is_published=True)
active_true.short_description = "Publlish"
def active_false(modeladmin,request,queryset):
    queryset.update(is_published=False)
active_false.short_description = "Unpublish"
class CmsModelAdmin(admin.ModelAdmin):
    model = Cms
    list_display = ('title', 'slug', 'less_description','is_published')
    list_filter = ('is_published','is_blocked')
    search_fields = ['title', 'slug']
    actions = (active_true, active_false)

    def less_description(self,obj):
        # print(obj)
        return obj.description[:100]


# odds popular
def popular_true(modeladmin,request,queryset):
    queryset.update(is_popular=True)
popular_true.short_description = "Popular"
def popular_false(modeladmin,request,queryset):
    queryset.update(is_popular=False)
popular_false.short_description = "Unpopular"
class OddsModelAdmin(admin.ModelAdmin):
    model = Odds
    list_display = ('id', 'name', 'date','is_popular')
    list_filter = ('is_popular',)
    # search_fields = ['name', ]
    actions = (popular_true,popular_false)
    def date(self,obj):
        return obj.created_at

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False




# Match Ranking
class MatchRankingAdmin(admin.ModelAdmin):
    model = MatchRankings
    form = MatchRankingForm
    list_display = ('id','ranking','created_at','max_value','min_value',)
    list_filter = ('min_value',)
    # fields = ('ranking',)


#Affiliateuser Manager
def popular_true(modeladmin,request,queryset):
    queryset.update(is_active=True)
popular_true.short_description = "Active"
def popular_false(modeladmin,request,queryset):
    queryset.update(is_active=False)
popular_false.short_description = "Inactive"
class AffiliateusersModelAdmin(admin.ModelAdmin):
    model = AffiliateUser
    add_form = AffiliateUserForm
    change_form = AffiliateChangeForm
    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(AffiliateusersModelAdmin, self).get_form(request, obj, **kwargs)

    list_display = ('name', 'email', 'phone', 'country','is_active')
    list_filter = ('is_active',)
    search_fields = ['name',]
    actions = (popular_true, popular_false)
    ordering = ("name",)

    # def active(self, obj):
    #     return obj.is_active == 1
    #
    # active.boolean = True

    # fields = ('name', 'email', 'phone', 'country', 'password','confirm_password')
    def save_model(self, request, obj, form, change):
        if obj.pk:
            pass
            # orig_obj = AffiliateUser.objects.get(pk=obj.pk)
            # if obj.password != orig_obj.password:
            #     obj.set_password(obj.password)
            # else:
            #     pwd = form.cleaned_data.get("password")
            #     obj.password = make_password(pwd)
            #     obj.confirm_password = make_password(pwd)
            # obj.save()

        else:
            pwd = form.cleaned_data.get("password")
            obj.password = make_password(pwd)
            obj.confirm_password = make_password(pwd)
            obj.is_active=True
        obj.save()

# Popular match
class PopularMatchAdmin(admin.ModelAdmin):
    model = PopularMatch
    list_display = ('id','match','date','is_popular',)
    list_filter = ('is_popular',)

    # def save_model(self, request, obj, form, change):
    #     if obj.pk:
    #         pass
    #
    #     else:
    #         obj.is_popular = True
    #     obj.save()


# Popular odds
class PopularOddsAdmin(admin.ModelAdmin):
    model = PopularOdds
    list_display = ('id','odds_name','date','is_popular',)
    list_filter = ('is_popular',)

    def odds_name(self, obj):
        # print(obj)
        return obj.odds.name
    # def save_model(self, request, obj, form, change):
    #     if obj.pk:
    #         pass
    #
    #     else:
    #         obj.is_popular = True
    #     obj.save()



# Statistics odds
class StatisticsAdmin(admin.ModelAdmin):
    model = Statistics
    list_display = ('id','ranking','created_at','max_value','min_value',)
    list_filter = ('min_value',)
    # fields = ('ranking',)


# Statistics odds
# class MatchStatisticsAdmin(admin.ModelAdmin):
#     model = MatchStatistics
#     list_display = ('id','ranking','created_at','max_value','min_value',)
#     list_filter = ('min_value',)
#     # fields = ('ranking',)



# Message
class MessageModelAdmin(admin.ModelAdmin):
    model = Message
    list_display = ("user_id", "user_name", "message", "created_date", "reply")
    # list_filter = ['matchid',]
    # search_fields = ['matchid',]
    # actions = ()

    def user_id(self, obj):
        return obj.sender.id

    def user_name(self, obj):
        return obj.sender.username

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:id>/messageview/",
                self.admin_site.admin_view(self.message_details),
                name="details-msg",
            ),
            path(
                "create/message/<int:to>",
                self.admin_site.admin_view(self.create_message),
                name="create_message",
            ),
            # url(
            #     r'^(?P<account_id>.+)/withdraw/$',
            #     self.admin_site.admin_view(self.process_withdraw),
            #     name='account-withdraw',
            # ),
        ]
        return custom_urls + urls

    def reply(self, obj):
        return format_html(
            # '<a class="button" href="{}">Deposit</a>&nbsp;'
            '<a class="button" href="{}">reply</a>',
            reverse("admin:details-msg", args=[obj.pk]),
            # reverse('admin:account-withdraw', args=[obj.pk]),
        )

    reply.short_description = "Reply"
    reply.allow_tags = True

    def get_queryset(self, request):
        qs = super(MessageModelAdmin, self).get_queryset(request)
        return qs

    # def get_queryset(self, request):
    #     qs = super(MessageModelAdmin, self).get_queryset(request)
    #     # return qs
    #     return qs.filter().distinct("sender_id")

    def message_details(self, request, id, *args, **kwargs):
        all_objs = self.get_queryset(request)
       
        obj = all_objs.get(id=id)
        sender_id = obj.sender.id
        admin_id = request.user.id
        msgs = all_objs.filter(sender_id=sender_id)
        msg_id=id
        return render(request, "admin/message_detail.html", {"msg_id":msg_id,"msgs": msgs,"sender_id":sender_id,"admin_id":admin_id})

    def create_message(self, request, to, *args, **kwargs):
        msg = request.POST.get("msg", None)
        print(msg)
        print("555")
        data = Message(receiver_id=to, sender_id=request.user.id, message=msg)
        data.save()
        return redirect("/admin/db_table/message/")


# live scores
import json

def active_true(modeladmin,request,queryset):
    queryset.update(is_active=True)
active_true.short_description = "Active"
def active_false(modeladmin,request,queryset):
    queryset.update(is_active=False)
active_false.short_description = "Inactive"


class FixtureModelAdmin(admin.ModelAdmin):
    model = Fixture
    # pass
    list_display = ("fixture_id", "league","season", "match", "schedule", "is_active")
    actions = (active_true, active_false)
    search_fields = ['fixture_id','league','match' ]
    # list_display_links = ("fixture_id","league_name", "locaolteam_name", "visitorteam_name", "datetime","local_score","vistor_score")

    
    def get_queryset(self, request):
        from datetime import datetime
        qs=super(FixtureModelAdmin, self).get_queryset(request)
        # print(datetime.today().strftime('%Y-%m-%d'))
        return qs.filter(time__contains=datetime.today().strftime('%Y-%m-%d'))
        
    def season(self, obj):
        try:
            season_id = obj.season_id
            season = Season.objects.get(season_id=season_id)
            return season.name
        except:
            return None
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:fixture_id>/livescoresview/',
                self.admin_site.admin_view(self.livescores_action),
                name='live-scores',
            ),
            # url(
            #     r'^(?P<account_id>.+)/withdraw/$',
            #     self.admin_site.admin_view(self.process_withdraw),
            #     name='account-withdraw',
            # ),
        ]
        return custom_urls + urls

    def action(self, obj):
        return format_html(
            # '<a class="button" href="{}">Deposit</a>&nbsp;'
            '<a class="button" href="{}">View</a>',
            reverse('admin:live-scores', args=[obj.pk]),
            # reverse('admin:account-withdraw', args=[obj.pk]),
        )

    action.short_description = 'Live Scores'
    action.allow_tags = True

    def livescores_action(self, request, fixture_id, *args, **kwargs):
        return render(request,'admin/livescores.html')



    def league(self,obj):
        try:
            league_id=obj.league_id
            league=Leagues.objects.get(league_id=league_id)
            return league.name
        except AttributeError:
            return None
        

    def schedule(self,obj):
        try:
            time = json.loads(obj.time)
            return time["starting_at"]["date_time"]
        except:
            return None

    def match(self, obj):
        try:
            lid = obj.localteam_id
            vid = obj.visitorteam_id
            team1 = Teams.objects.filter(team_id=lid).first()
            team2 = Teams.objects.filter(team_id=vid).first()
            if team1 and team2:
                return (team1.name) + " vs " + (team2.name)
            else:
                return None
        except AttributeError:
            return None
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return False
    # def locaolteam_name(self,obj):
    #     try:
    #         localteam_id=obj.localteam_id
    #         team=Teams.objects.filter(team_id=localteam_id).first()
    #         return team.name
    #     except AttributeError:
    #         return None
    #     # except Leagues.ObjectDoesNotExist:
    #     #     return None
    #
    # def visitorteam_name(self, obj):
    #     try:
    #         visitorteam_id = obj.visitorteam_id
    #         team = Teams.objects.filter(team_id=visitorteam_id).first()
    #         return team.name
    #     except AttributeError:
    #         return None

    # def local_score(self,obj):
    #     try:
    #         score = json.loads(obj.scores)
    #         return score["localteam_score"]
    #     except:
    #         return None
    #
    # def vistor_score(self,obj):
    #     try:
    #         score = json.loads(obj.scores)
    #         return score["visitorteam_score"]
    #     except:
    #         return None


class SeasonMatchPlanAdmin(admin.ModelAdmin):
    model = SeasonMatchPlan
    # pass
    list_display = ("match_id", "league","season", "home_team","total_home_score", "away_team","total_away_score")
    # actions = (active_true, active_false)
    search_fields = ['fixture_id','league' ]
    # list_display_links = ("fixture_id","league_name", "locaolteam_name", "visitorteam_name", "datetime","local_score","vistor_score")

    
    # def get_queryset(self, request):
    #     qs=super(FixtureModelAdmin, self).get_queryset(request)
    #     # print(datetime.today().strftime('%Y-%m-%d'))
    #     return qs.filter(time__contains=datetime.today().strftime('%Y-%m-%d'))
    def league(self, obj):
        try:
            league_id = obj.league_id
            #print("**************")
            league = Leagues.objects.get(league_id=league_id,collection_datasource="www.worldfootball.net")
            # print(league)
            return league.name
        except:
            return None
    def home_team(self, obj):
        try:
            team_id = obj.home_team_id
            team = Teams.objects.get(team_id=team_id,collection_datasource="www.worldfootball.net")
            return team.name
        except:
            return None 
    def away_team(self, obj):
        try:
            team_id = obj.away_team_id
            team = Teams.objects.get(team_id=team_id,collection_datasource="www.worldfootball.net")
            return team.name
        except:
            return None 
    def season(self, obj):
        try:
            season_id = obj.season_id
            season = AllSeason.objects.get(season_id=season_id,collection_datasource="www.worldfootball.net")
            return season.name
        except:
            return None
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:fixture_id>/livescoresview/',
                self.admin_site.admin_view(self.livescores_action),
                name='live-scores',
            ),
            # url(
            #     r'^(?P<account_id>.+)/withdraw/$',
            #     self.admin_site.admin_view(self.process_withdraw),
            #     name='account-withdraw',
            # ),
        ]
        return custom_urls + urls

    def action(self, obj):
        return format_html(
            # '<a class="button" href="{}">Deposit</a>&nbsp;'
            '<a class="button" href="{}">View</a>',
            reverse('admin:live-scores', args=[obj.pk]),
            # reverse('admin:account-withdraw', args=[obj.pk]),
        )

    action.short_description = 'Season Match'
    action.allow_tags = False

    def livescores_action(self, request, fixture_id, *args, **kwargs):
        return render(request,'admin/livescores.html')

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return False
    # def locaolteam_name(self,obj):
    #     try:
    #         localteam_id=obj.localteam_id
    #         team=Teams.objects.filter(team_id=localteam_id).first()
    #         return team.name
    #     except AttributeError:
    #         return None
    #     # except Leagues.ObjectDoesNotExist:
    #     #     return None
    #
    # def visitorteam_name(self, obj):
    #     try:
    #         visitorteam_id = obj.visitorteam_id
    #         team = Teams.objects.filter(team_id=visitorteam_id).first()
    #         return team.name
    #     except AttributeError:
    #         return None

    # def local_score(self,obj):
    #     try:
    #         score = json.loads(obj.scores)
    #         return score["localteam_score"]
    #     except:
    #         return None
    #
    # def vistor_score(self,obj):
    #     try:
    #         score = json.loads(obj.scores)
    #         return score["visitorteam_score"]
    #     except:
    #         return None

class SmpAdmin(admin.ModelAdmin):

    def get_urls(self):

        # get the default urls
        urls = super(SmpAdmin, self).get_urls()

        # define security urls
        security_urls = [
            url(r'^smp/$', self.admin_site.admin_view(self.security_configuration))
            # Add here more urls if you want following same logic
        ]

        # Make sure here you place your added urls first than the admin default urls
        return security_urls + urls

    # Your view definition fn
    def security_configuration(self, request):
        context = dict(
            self.admin_site.each_context(request), # Include common variables for rendering the admin template.
            something="test",
        )
        return TemplateResponse(request, "season_match_plan.html", context)


# AllSeason manager
def active_true(modeladmin,request,queryset):
    queryset.update(is_active=True)
active_true.short_description = "Publlish"
def active_false(modeladmin,request,queryset):
    queryset.update(is_active=False)
active_false.short_description = "Unpublish"

class AllSeasonModelAdmin(admin.ModelAdmin):
    model = AllSeason
    list_display = ('season_id','name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ['name',]
    actions = (active_true, active_false)

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Countries, CountriesModelAdmin)
admin.site.register(Leagues, LeaguesModelAdmin)
admin.site.register(Teams, TeamsModelAdmin)
admin.site.register(Players, PlayersModelAdmin)
admin.site.register(MatchFixtureUpdate, MatchModelAdmin)
admin.site.register(Season, SeasonModelAdmin)
admin.site.register(Subscriptions, SubscriptionModelAdmin)
admin.site.register(Blogs, BlogsModelAdmin)
admin.site.register(AffiliateUser, AffiliateusersModelAdmin)
admin.site.register(Cms, CmsModelAdmin)
admin.site.register(Odds, OddsModelAdmin)
admin.site.register(MatchRankings,MatchRankingAdmin)
admin.site.register(Betslip, BetslipModelAdmin)
admin.site.register(Message, MessageModelAdmin)
admin.site.register(Fixture, FixtureModelAdmin)

admin.site.register(PopularMatch,PopularMatchAdmin)
admin.site.register(PopularOdds,PopularOddsAdmin)
admin.site.register(Statistics,StatisticsAdmin)
admin.site.register(SeasonMatchPlan,SeasonMatchPlanAdmin)

admin.site.register(AllSeason,AllSeasonModelAdmin)
# admin.site.register(Smp,SmpAdmin)



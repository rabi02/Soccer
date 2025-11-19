from db_table.models import *
import redis
# def season_save(res):
#     redis_instance.set("season", res)
#     json_res = json.loads(res)
#     for resp in json_res["data"]:
#         try:
#             Season.objects.get(name=resp["name"])
#         except Season.DoesNotExist:
#             Season.objects.create(
#                 seasonid=resp["id"],
#                 name=resp["name"],
#                 league_id=resp["league_id"],
#                 season_id=resp["season_id"],
#                 round_id=resp["round_id"],
#                 round_name=resp["round_name"],
#                 type=resp["type"],
#                 stage_id=resp["stage_id"],
#                 stage_name=resp["stage_name"],
#                 resource=resp["resource"],
#                 standings=resp["standings"])
#     return json.loads(res)

# def countries_save(res):
#     redis_instance.set("country", res)
#     json_res = json.loads(res)
#     for resp in json_res["data"]:
#         try:
#             continent = resp["extra"]["continent"]
#         except TypeError:
#             continent = None
#         try:
#             sub_region = resp["extra"]["sub_region"]
#         except TypeError:
#             sub_region = None
#         try:
#             world_region = resp["extra"]["world_region"]
#         except TypeError:
#             world_region = None
#         try:
#             fifa = resp["extra"]["fifa"]
#         except TypeError:
#             fifa = None
#         try:
#             iso = resp["extra"]["iso"]
#         except TypeError:
#             iso = None
#         try:
#             iso2 = resp["extra"]["iso2"]
#         except TypeError:
#             iso2 = None
#         try:
#             longitude = resp["extra"]["longitude"]
#         except TypeError:
#             longitude = None
#         try:
#             latitude = resp["extra"]["latitude"]
#         except TypeError:
#             latitude = None
#         try:
#             flag = resp["extra"]["flag"]
#         except TypeError:
#             flag = None
#         try:
#             Countries.objects.get(name=resp["name"])
#         except Countries.DoesNotExist:
#             Countries.objects.create(
#                 country_id=resp["id"],
#                 name=resp["name"],
#                 image_path=resp["image_path"],
#                 continent=continent,
#                 sub_region=sub_region,
#                 world_region=world_region,
#                 fifa=fifa,
#                 iso=iso,
#                 iso2=iso2,
#                 longitude=longitude,
#                 latitude=latitude,
#                 flag=flag,
#             )
#     return json.loads(res)
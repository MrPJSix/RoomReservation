from rest_framework.views import APIView
from rest_framework.response import Response
from Model.serializers import RoomSerializer
from Model.models import *
import datetime
from django.http import QueryDict
from System.tasks import create_reservation_task

# Create your views here.

"""条件查询自习室"""


class RoomsByCondition(APIView):
    def get(self, request, format=None):
        try:
            rooms = Room.objects
            query = request.query_params.get('campus_id')
            if query != None:
                rooms = rooms.filter(building__campus__campus_id__contains=query)

            query = request.query_params.get('building_id')
            if query != None:
                rooms = rooms.filter(building__building_id__contains=query)

            query = request.query_params.get('type')
            if query != None:
                rooms = rooms.filter(type=query)

            query = request.query_params.get('room_name')
            if query != None:
                rooms = rooms.filter(room_name__contains=query)

            query = request.query_params.get('have_seats')
            if query != None:
                flag = True if query == 'True' or query == 'true' else False
                if flag:
                    rooms = rooms.filter(number_of_seats__gt=0)

            query = request.query_params.get('have_charge')
            if query != None:
                rooms = rooms.filter(have_charge=int(query))

            query = request.query_params.get('close_time')
            if query != None:
                rooms = rooms.filter(close_time__hour=datetime.time(hour=query))

            query = request.query_params.get('is_allnight')
            if query != None:
                flag = True if query == 'True' or query == 'true' else False
                rooms = rooms.filter(is_allnight=flag)

            query = request.query_params.get('is_available')
            if query != None:
                flag = True if query == 'True' or query == 'true' else False
                rooms = rooms.filter(is_available=flag)
            rooms = rooms.all()

        except Room.DoesNotExist:
            data = {
                'success': False,
                'code': 400,
                'data': '数据不存在！'
            }
            return Response(data)

        serializer = RoomSerializer(rooms, many=True)
        data = {
            'success': True,
            'code': 100,
            'data': serializer.data
        }
        return Response(data)


""" 查看选定时间当前自习室座位状态 """


# 获取座位状态函数
def get_status_str(time_diff, sign):
    if time_diff == 0:
        return chr(ord('A') + sign)
    elif time_diff == 1:
        return chr(ord('B') + sign)
    elif time_diff == 2:
        return chr(ord('C') + sign)
    elif time_diff == 3:
        return chr(ord('D') + sign)
    else:
        return chr(ord('E') + sign)


def get_seat_status(room_id, seat_id, time_get, sign):
    reservations = Reservation.objects.filter(
        date=datetime.date.today(),
        seat_id=seat_id,
        reservation_status__in=('0', '1')
    ).all()
    room = Room.objects.get(room_id=room_id)
    room_close_time = room.close_time.hour
    time_diff = room_close_time - time_get.hour
    if time_diff <= 0:
        return chr(ord('A') + sign)
    if len(reservations) == 0:
        return get_status_str(time_diff, sign)
    for reservation in reservations:
        start_time = reservation.reservation_time
        end_time = (datetime.datetime.combine(datetime.datetime.min, start_time) +
                    datetime.timedelta(hours=reservation.reservation_hours)).time()
        if start_time <= time_get <= end_time:
            return chr(ord('A') + sign)
        if end_time <= time_get:
            continue
        else:
            time_diff = start_time.hour - time_get.hour
    time_diff = min(time_diff, room_close_time - time_get.hour)
    return get_status_str(time_diff, sign)


class SeatsStatusList(APIView):
    def get(self, request):
        try:
            seats = Seat.objects
            query = request.query_params.get('room_id')
            if query != None:
                seats = seats.filter(room_id=int(query))
            seats = seats.all()
        except Seat.DoesNotExist:
            data = {
                'success': False,
                'code': 400,
                'data': '数据不存在！'
            }
            return Response(data)

        query = request.query_params.get('time_start')
        time_get = datetime.time(hour=int(query))
        seats_status = []
        for seat in seats:
            sign = 0 if seat.can_charge else 32
            status = get_seat_status(seat.room_id, seat.seat_id, time_get, sign)
            seats_status.append((status, int(seat.seat_number)))
        seats_status.sort(key=lambda x: x[1])
        result = "".join([item[0] for item in seats_status])
        data = {
            'success': True,
            'code': 100,
            'data': result
        }
        return Response(data)


""" 
401 预约座位失败：信用值不及格！
402 预约座位失败：座位已被预定！
403 预约座位失败：预约时间过长！
"""


# 预约座位
class ReservationBook(APIView):
    def post(self, request):
        query = request.data
        user = User.objects.get(user_id=query['user_id'])
        if user.credits < 60:
            data = {
                'success': False,
                'code': 401,
                'msg': "你的信誉值太低，无法预约！"
            }
            return Response(data)
        # ------------------- 判断预约时间是否在自习室开放时间，否则无法预约
        reservation_time = datetime.time(hour=int(query['reservation_time']))
        room_id = int(query['room_id'])
        # =================== 判断是否有未生效的预约，否则无法再次预约
        room = Room.objects.get(room_id=room_id)
        if not (room.open_time < reservation_time < room.close_time):
            data = {
                'success': False,
                'code': 406,
                'msg': "预约时间不在教室开放时间，无法预约！"
            }
            return Response(data)
        reservations = Reservation.objects.filter(user=user, date=datetime.date.today(),
                                                  reservation_status__in=['0', '1']).all()
        if len(reservations) != 0:
            data = {
                'success': False,
                'code': 405,
                'msg': "存在未结束/未取消预约，没办法再次预约！"
            }
            return Response(data)

        seat_number = query['seat_number']
        reservation_hours = int(query['reservation_hours'])

        seat = Seat.objects.filter(room=room_id, seat_number=seat_number).first()
        tag = get_seat_status(room_id, seat.seat_id, reservation_time, 32)
        if tag == 'a':
            data = {
                'success': False,
                'code': 402
            }
        elif tag == 'b' and reservation_hours > 1:
            data = {
                'success': False,
                'code': 403
            }
        elif tag == 'c' and reservation_hours > 2:
            data = {
                'success': False,
                'code': 403
            }
        elif tag == 'd' and reservation_hours > 3:
            data = {
                'success': False,
                'code': 403
            }
        else:
            reservation = Reservation.objects.create(user=user, room_id=room_id, seat=seat,
                                                     reservation_time=reservation_time,
                                                     reservation_hours=reservation_hours)
            create_reservation_task(reservation)
            data = {
                'success': True,
                'code': 100
            }
        return Response(data)


"""
700 取消预约失败：该预约记录不存在！
701 取消预约失败：该预约已生效！
702 取消预约失败：该预约已取消！
703 取消预约失败：该预约已违约！
704 取消预约失败：该预约已结束！
"""


# 取消预约
class ReservationCancel(APIView):
    def put(self, request):
        date1 = {"success": 0}
        if request.method == "PUT":
            put = QueryDict(request.body)
            reservation_id = put.get('reservation_id')
            try:
                # 说明文档中此处传入数据为order_id 而非 reservation_id，需注意
                reservation = Reservation.objects.filter(reservation_id=reservation_id).first()
            except Reservation.DoesNotExist:
                data = {
                    'success': False,
                    'code': 700
                }
                return Response(data)
            if reservation is None:
                data = {
                    'success': False,
                    'code': 400,
                    'data': '数据为空！'
                }
                return Response(data)
            if reservation.reservation_status == 1:
                data = {
                    'success': False,
                    'code': 701
                }
            elif reservation.reservation_status == 2:
                data = {
                    'success': False,
                    'code': 702
                }
            elif reservation.reservation_status == 3:
                data = {
                    'success': False,
                    'code': 703
                }
            elif reservation.reservation_status == 4:
                data = {
                    'success': False,
                    'code': 704
                }
            else:
                obj = Reservation.objects.filter(reservation_id=reservation.reservation_id).first()
                obj.reservation_status = 2
                obj.save()
                data = {
                    'success': True,
                    'code': 100
                }
            return Response(data)

        return Response(date1)


# 查询用户所有的预约记录
class ReservationAll(APIView):
    def get(self, request):
        # query = request.data
        query = request.query_params.get('user_id')
        print("查询用户所有的预约记录==========")
        try:
            if query is not None:
                reservations = Reservation.objects.filter(user=query)
            # reservations = Reservation.objects.filter(user=query['user_id']).all()
            else:
                reservations = Reservation.objects.all()
        except Reservation.DoesNotExist:
            data = {
                'success': False,
                'code': 400,
                'data': '数据不存在！'
            }
            return Response(data)

        redata = []
        for reservation in reservations:
            room_name = reservation.room.room_name
            room_id = reservation.room.room_id
            campus_name = reservation.room.building.campus.campus_name
            building_name = reservation.room.building.building_name
            reservation_id = reservation.reservation_id
            date = reservation.date
            reservation_time = reservation.reservation_time
            reservation_hours = reservation.reservation_hours
            reservation_status = reservation.reservation_status
            seat_number = reservation.seat.seat_number
            tmpdate = {
                "reservation_id": reservation_id,
                "date": date,
                "reservation_time": reservation_time,
                "reservation_hours": reservation_hours,
                "reservation_status": reservation_status,
                "room_name": room_name,
                "room_id": room_id,
                "seat_number": seat_number,
                "campus_name": campus_name,
                "building_name": building_name
            }
            redata.append(tmpdate)
        #    serializer = ReservationSerializer(reservations, many=True)
        data = {
            'success': True,
            'code': 100,
            'data': redata
        }
        return Response(data)


# 查询用户未生效的预约记录
class ReservationInvalid(APIView):
    def get(self, request):
        print("=======查询用户未生效的预约记录=======")
        query = request.query_params.get('user_id')
        try:
            reservation = Reservation.objects.filter(user=query, reservation_status='0').first()
        except Reservation.DoesNotExist:
            data = {
                'success': False,
                'code': 400,
                'data': '数据不存在！'
            }
            return Response(data)
        if reservation is None:
            data = {
                'success': False,
                'code': 400,
                'data': '数据为空！'
            }
            return Response(data)
        room_name = reservation.room.room_name
        room_id = reservation.room.room_id
        campus_name = reservation.room.building.campus.campus_name
        building_name = reservation.room.building.building_name
        reservation_id = reservation.reservation_id
        date = reservation.date
        reservation_time = reservation.reservation_time
        reservation_hours = reservation.reservation_hours
        reservation_status = reservation.reservation_status
        seat_number = reservation.seat.seat_number
        data = {
            'success': True,
            'code': 100,
            'data': {
                "reservation_id": reservation_id,
                "date": date,
                "reservation_time": reservation_time,
                "reservation_hours": reservation_hours,
                "reservation_status": reservation_status,
                "room_name": room_name,
                "room_id": room_id,
                "seat_number": seat_number,
                "campus_name": campus_name,
                "building_name": building_name
            }
        }
        return Response(data)


"""
801 签到失败：该预约记录不存在！
802 签到失败：该预约已生效！
803 签到失败：该预约已取消！
804 签到失败：该预约已违约！
805 签到失败：该预约已结束！
"""


# 签到
class SignIn(APIView):
    def get(self, request):
        query = request.query_params.get('reservation_id')
        try:
            reservation = Reservation.objects.filter(reservation_id=query).first()
        except Reservation.DoesNotExist:
            data = {
                'success': False,
                'code': 801
            }
            return Response(data)

        if reservation.reservation_status == 1:
            data = {
                'success': False,
                'code': 802
            }
        elif reservation.reservation_status == 2:
            data = {
                'success': False,
                'code': 803
            }
        elif reservation.reservation_status == 3:
            data = {
                'success': False,
                'code': 804
            }
        elif reservation.reservation_status == 4:
            data = {
                'success': False,
                'code': 805
            }
        else:
            obj = Reservation.objects.filter(reservation_id=reservation.reservation_id).first()
            obj.reservation_status = 1
            obj.save()
            obj.refresh_from_db()
            create_reservation_task(obj)
            room_name = obj.room.room_name
            room_id = obj.room.room_id
            campus_name = obj.room.building.campus.campus_name
            building_name = obj.room.building.building_name
            reservation_id = obj.reservation_id
            date = obj.date
            reservation_time = obj.reservation_time
            reservation_hours = obj.reservation_hours
            reservation_status = obj.reservation_status
            seat_number = obj.seat.seat_number
            data = {
                'success': True,
                'code': 100,
                'data': {
                    "reservation_id": reservation_id,
                    "date": date,
                    "reservation_time": reservation_time,
                    "reservation_hours": reservation_hours,
                    "reservation_status": reservation_status,
                    "room_name": room_name,
                    "room_id": room_id,
                    "seat_number": seat_number,
                    "campus_name": campus_name,
                    "building_name": building_name
                }
            }
        return Response(data)

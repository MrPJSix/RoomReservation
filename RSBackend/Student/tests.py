from datetime import time
from rest_framework.test import APITestCase, APIClient
from Model.models import Campus, Building, Room, Seat, Reservation, User
from System.tasks import *
from freezegun import freeze_time
from unittest.mock import patch
import time as t

class RoomAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/studyroom/'
        self.campus1 = Campus.objects.create(campus_id='HP', campus_name='黄浦校区')
        self.building1 = Building.objects.create(building_id='HPA', building_name='第一教学楼', campus=self.campus1)
        self.room1 = Room.objects.create(building=self.building1, room_name='HPA101')
        self.room2 = Room.objects.create(building=self.building1, room_name='HPA102')
        print("\n ===== Starting tests for RoomsByCondition APIView... ===== ")

    def tearDown(self):
        print(" ===== Tests finished for RoomsByCondition APIView... ===== ")

    def test_get_room_by_buildingid(self):
        response = self.client.get(self.url, {'building_id': self.building1.building_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 2)
        # 判断room_name
        response_room_name = []
        for v in response.data['data']:
            response_room_name.append(v['room_name'])
        self.assertIn(self.room1.room_name, response_room_name)
        self.assertIn(self.room2.room_name, response_room_name)


class SeatAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/studyroom/seatstatus/'
        self.campus1 = Campus.objects.create(campus_id='HP', campus_name='黄浦校区')
        self.building1 = Building.objects.create(building_id='HPA', building_name='第一教学楼', campus=self.campus1)
        self.room1 = Room.objects.create(building=self.building1, room_name='HPA101')
        self.seat1 = Seat.objects.create(room=self.room1, seat_number="1", can_charge=True)
        self.seat2 = Seat.objects.create(room=self.room1, seat_number="2", can_charge=False)
        self.seat3 = Seat.objects.create(room=self.room1, seat_number="3", can_charge=True)
        print("\n ===== Starting tests for SeatsStatusList APIView... ===== ")

    def tearDown(self):
        print(" ===== Tests finished for SeatsStatusList APIView... ===== ")

    def test_get_seat_status(self):
        # 测试1：没有预约记录干扰，在教室关闭时间至少4个小时的座位状态
        response1 = self.client.get(self.url, {'room_id': self.room1.room_id, 'time_start': 10})
        self.assertEqual(response1.status_code, 200)
        self.assertEqual("EeE", response1.data['data'])

        # 测试2：没有预约记录干扰，在教室关闭时间前3个小时的座位状态
        response2 = self.client.get(self.url, {'room_id': self.room1.room_id, 'time_start': 19})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual("DdD", response2.data['data'])

        # 测试3：没有预约记录干扰，在教室关闭时间前2个小时的座位状态
        response3 = self.client.get(self.url, {'room_id': self.room1.room_id, 'time_start': 20})
        self.assertEqual(response3.status_code, 200)
        self.assertEqual("CcC", response3.data['data'])

        # 测试4：没有预约记录干扰，在教室关闭时间前1个小时的座位状态
        response4 = self.client.get(self.url, {'room_id': self.room1.room_id, 'time_start': 21})
        self.assertEqual(response4.status_code, 200)
        self.assertEqual("BbB", response4.data['data'])

        # 测试5：没有预约记录干扰，在教室关闭时间的座位状态
        response5 = self.client.get(self.url, {'room_id': self.room1.room_id, 'time_start': 22})
        self.assertEqual(response5.status_code, 200)
        self.assertEqual("AaA", response5.data['data'])

        # 测试6：有预约记录干扰，在教室开放时间段的座位状态
        user1 = User.objects.create_user(user_id='123', email='123@qq.com')
        user2 = User.objects.create_user(user_id='456', email='456@qq.com')
        Reservation.objects.create(user=user1, room=self.room1, seat=self.seat1, reservation_time=time(13, 0))
        Reservation.objects.create(user=user2, room=self.room1, seat=self.seat2, reservation_time=time(12, 0))
        response6 = self.client.get(self.url, {'room_id': self.room1.room_id, 'time_start': 10})
        self.assertEqual(response6.status_code, 200)
        self.assertEqual("DcE", response6.data['data'])


class ReservationAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.base_url = '/reservations'
        self.campus1 = Campus.objects.create(campus_id='HP', campus_name='黄浦校区')
        self.building1 = Building.objects.create(building_id='HPA', building_name='第一教学楼', campus=self.campus1)
        self.room1 = Room.objects.create(building=self.building1, room_name='HPA101')
        self.seat1 = Seat.objects.create(room=self.room1, seat_number="1", can_charge=True)
        self.seat2 = Seat.objects.create(room=self.room1, seat_number="2", can_charge=False)
        self.user1 = User.objects.create_user(user_id='123', email='123@qq.com')
        self.user2 = User.objects.create_user(user_id='456', email='456@qq.com')

    def test_info(self):  # 测试查询所有预约记录
        Reservation.objects.create(user=self.user1, room=self.room1, seat=self.seat1, reservation_time=time(10, 0))
        Reservation.objects.create(user=self.user1, room=self.room1, seat=self.seat2, reservation_time=time(15, 0))
        rsp = self.client.get(self.base_url + '/info', {'user_id': self.user1.user_id})
        res = rsp.json()
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(len(res['data']), 2)

    def test_sign_end(self):
        rev = Reservation.objects.create(user=self.user1, room=self.room1, seat=self.seat2, reservation_time=time(11, 0))
        print("...测试签到后数据...")
        self.assertEqual(int(rev.reservation_status), 0)
        rev.reservation_status = '1'
        rev.save()
        self.assertEqual(int(rev.reservation_status), 1)
        hand_reservation_end(rev.reservation_id)
        rev.refresh_from_db()
        self.assertEqual(int(rev.reservation_status), 4)

    def test_invaild(self):
        rev = Reservation.objects.create(user=self.user1, room=self.room1, seat=self.seat1, reservation_time=time(10, 0))
        rsp = self.client.get(self.base_url + '/invalid', {'user_id': self.user1.user_id})
        res = rsp.json()
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(res['data']['reservation_id'], rev.reservation_id)
        self.assertEqual(int(res['data']['reservation_status']), 0)

    def test_cancel(self):
        print("...测试取消预约...")
        rev = Reservation.objects.create(user=self.user1, room=self.room1, seat=self.seat1, reservation_time=time(10, 0))
        rsp = self.client.put(self.base_url + '/cancel',  {'reservation_id': rev.reservation_id}, format='multipart')
        res = rsp.json()
        self.assertEqual(rsp.status_code, 200)
        rev.refresh_from_db()
        self.assertEqual(rev.reservation_status, '0')

    @freeze_time('10:15')
    def test_booking(self):
        print("...测试预约...")
        url = 'http://127.0.0.1:8000/studyroom/booking'
        #rsp1 = self.client.post(url, {'user_id': self.user2.user_id, 'room_id': 1, 'seat_number': 1, 'reservation_time': 11,
        #                             'reservation_hours': 2})
        rev = Reservation.objects.create(user=self.user1, room=self.room1, seat=self.seat2, reservation_time=time(11, 0))
        self.assertEqual(rev.reservation_status, '0')
        with freeze_time('11:15'):
            handle_reservation_default(rev.reservation_id)
            rev.refresh_from_db()
            self.assertEqual(rev.reservation_status, '3')
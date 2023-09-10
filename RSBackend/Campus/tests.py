from rest_framework.test import APITestCase, APIClient
from Model.models import Campus, Building


class CampusViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/campus/'
        self.campus1 = Campus.objects.create(campus_id='HP', campus_name='黄浦校区')
        self.campus2 = Campus.objects.create(campus_id='MH', campus_name='闵行校区')
        print("\n ===== Starting tests for AllCampusList APIView... ===== ")

    def tearDown(self):
        print(" ===== Tests finished for AllCampusList APIView... ===== ")

    def test_get_all_campuses(self):
        # self.shortDescription = '测试获取全部Campus功能'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 2)
        # 判断campus_id
        response_campuses_id = []
        for v in response.data['data']:
            response_campuses_id.append(v['campus_id'])
        self.assertIn(self.campus1.campus_id, response_campuses_id)
        self.assertIn(self.campus2.campus_id, response_campuses_id)
        # 判断campus_id
        response_campuses_name = []
        for v in response.data['data']:
            response_campuses_name.append(v['campus_name'])
        self.assertIn(self.campus1.campus_name, response_campuses_name)
        self.assertIn(self.campus2.campus_name, response_campuses_name)


class BuildingViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/building/'
        self.campus1 = Campus.objects.create(campus_id='HP', campus_name='黄浦校区')
        self.building1 = Building.objects.create(building_id='HPA', building_name='第一教学楼', campus=self.campus1)
        self.building2 = Building.objects.create(building_id='HPB', building_name='第二教学楼', campus=self.campus1)
        print("\n ===== Starting tests for BuildingByCampusId APIView... ===== ")

    def tearDown(self):
        print(" ===== Tests finished for BuildingByCampusId APIView... ===== ")

    def test_get_building_by_campuseid(self):
        response = self.client.get(self.url, {'campus_id': self.campus1.campus_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 2)
        # 判断building_id
        response_building_id = []
        for v in response.data['data']:
            response_building_id.append(v['building_id'])
        self.assertIn(self.building1.building_id, response_building_id)
        self.assertIn(self.building2.building_id, response_building_id)
        # 判断building_name
        response_building_name = []
        for v in response.data['data']:
            response_building_name.append(v['building_name'])
        self.assertIn(self.building1.building_name, response_building_name)
        self.assertIn(self.building2.building_name, response_building_name)

from rest_framework.test import APITestCase, APIClient
from Model.models import User

# 注册
class RegisterCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/register/'
        
        print("\n ===== Starting tests for Rsgister APIView... ===== ")

    def tearDown(self):
        print(" ===== Tests finished for Rsgister APIView... ===== ")

    def test_register(self):
        user_id = '22210240000'
        user_name = 'Jackson'
        password = '123'
        email = '22210240000@m.fudan.edu.cn'
        # 注册新用户 - 账号未存在
        response = self.client.post(self.url, {
            'user_id': user_id, 'user_name': user_name,
            'password': password, 'email': email
        })
        res = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['success'], True)
        # 注册新用户 - 账号已被使用
        response2 = self.client.post(self.url, {'user_id': user_id, 'user_name': 'Julia',
                                               'password': '123456', 'email': '22210240000@m.fudan.edu.cn'})
        res2 = response2.json()
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(res2['success'], False)
        self.assertEqual(res2['message'], 'User is existing')

class LoginCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/login/'
        print("\n ===== Starting tests for Login APIView... ===== ")

    def tearDown(self):
        print(" ===== Tests finished for Login APIView... ===== ")

    def test_login(self):
        # 先注册一个账号
        user_id = '112233'
        user_name = 'James'
        password = '123'
        email = '112233@m.fudan.edu.cn'
        self.client.post('/register/', {
            'user_id': user_id, 'user_name': user_name,
            'password': password, 'email': email
        })
        # 账号、密码正确
        response1 = self.client.post(self.url, {'user_id': user_id, 'password': password})
        res1 = response1.json()
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(res1['success'], True)
        self.assertEqual(res1['data']['user_id'], user_id)

        # 账号不正确、密码正确
        response2 = self.client.post(self.url, {'user_id': '11223', 'password': password})
        res2 = response2.json()
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(res2['success'], False)
        self.assertEqual(res2['message'], 'User not found')
        
        # 账号正确、密码不正确
        response3 = self.client.post(self.url, {'user_id': user_id, 'password': '123456'})
        res3 = response3.json()
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(res3['success'], False)
        self.assertEqual(res3['message'], 'Incorrect password')

# 查看用户所有信息
class UserInfoCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/userInfo/'
        self.username = 'Jackson'
        self.password = '123'
        self.userid = '22210240000'
        self.email = '22210240000@m.fudan.edu.cn'
        User.objects.create(user_name=self.username, password=self.password, user_id=self.userid, email=self.email)
        print("\n ===== Starting tests for UserInfo APIView... ===== ")

    def tearDown(self):
        print(" ===== Tests finished for UserInfo APIView... ===== ")

    def test_user_info(self):
        response = self.client.get(self.url, {'user_id': self.userid})
        res = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['success'], True)

        self.assertEqual(res['data']['user_id'], self.userid)
#
# 用户信息更新
class UserInfoUpdateCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/userInfo/update/'
        self.username = 'Jackson'
        self.password = '123'
        self.userid = '22210240000'
        self.email = '22210240000@m.fudan.edu.cn'
        User.objects.create(user_name=self.username, password=self.password, user_id=self.userid, email=self.email)
        print("\n ===== Starting tests for UserInfoUpdate APIView... ===== ")

    def tearDown(self):
        print(" ===== Tests finished for UserInfoUpdate APIView... ===== ")

    def test_user_info_update(self):
        cases = [
            {'user_name': 'Wang',
             'email': ''},
             {'user_name': '',
             'email': '123@qq.com'},
             {
                'user_name': 'Jackson Wang',
                'email': '123123@qq.com'
             }
        ]

        for case in cases:
            response = self.client.get(self.url, {'user_id': self.userid, 'user_name': case['user_name'], 'email': case['email']})
            res = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(res['success'], True)

            self.assertEqual(res['data']['user_id'], self.userid)
            if case['user_name'] != '':
                self.assertEqual(res['data']['user_name'], case['user_name'])
            if case['email'] != '':
                self.assertEqual(res['data']['email'], case['email'])

# 信誉查询 userInfo/credits/
class UserCreditsInfoCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/userInfo/credits/'
        self.username = 'Jackson'
        self.password = '123'
        self.userid = '22210240000'
        self.email = '22210240000@m.fudan.edu.cn'
        User.objects.create(user_name=self.username, password=self.password, user_id=self.userid, email=self.email)
        print("\n ===== Starting tests for UserCreditsInfo APIView... ===== ")

    def tearDown(self):
        print(" ===== Tests finished for UserCreditsInfo APIView... ===== ")

    def test_user_info_update(self):
        response = self.client.get(self.url, {'user_id': self.userid})
        res = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['success'], True)

        self.assertEqual(res['data']['user_id'], self.userid)
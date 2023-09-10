from Model.models import Campus, Building
from Model.serializers import CampusSerializer, BuildingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


""" 全部查询校区 """
class AllCampusList(APIView):
    def get(self, request):
        try:
            campuses = Campus.objects.all()
        except Campus.DoesNotExist:
            data = {
                'success': False,
                'code':400,
                'data': '数据不存在！'
            }
            return Response(data)
        serializer = CampusSerializer(campuses, many=True)
        data = {
            'success': True,
            'code': 100,
            'data': serializer.data
        }
        return Response(data)

""" 条件查询教学楼 """
class BuildingsByCondition(APIView):
    def get(self, request, format=None):
        query = request.query_params.get('campus_id')
        try:
            buildings = Building.objects
            if query != None:
                buildings = buildings.filter(campus__campus_id__contains=query)
            else:
                buildings = buildings.all()
        except Building.DoesNotExist:
            data = {
                'success': False,
                'code': 400,
                'data': '数据不存在',
            }

        serializer = BuildingSerializer(buildings, many=True)
        data = {
            'success': True,
            'code': 100,
            'data': serializer.data
        }
        return Response(data)

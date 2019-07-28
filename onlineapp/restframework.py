# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from onlineapp.serializers import *
#
# @api_view(['GET','POST'])
# def college_list(request):
#     if request.method=='GET':
#         colleges = College.objects.all()
#         serializer = Collegeserializer(colleges, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         clg
#         serializer=Collegeserializer(colleges, many=True)
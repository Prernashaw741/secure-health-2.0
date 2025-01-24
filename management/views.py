from rest_framework.response import Response
from rest_framework.views import APIView
from openai import OpenAI
import base64,json

from authentication.models import User
from management.serializer import TESTSerializer, UploadSerializer
from .models import Uploads, tests as TEST

class UploadView(APIView):
    def encode_image(self,image_binary):
        
        return base64.b64encode(image_binary.read()).decode("utf-8")

    def post(self, request):
        file = request.FILES.get('file', None)
        if(file == None):
            return Response(data = {
                'message' : 'Please upload a file'
            }, status = 400)
        else:
            # OpenAI Stuffs
            client = OpenAI()
            image = self.encode_image(file)
            chat_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text":"You're a smart helpful AI assistent. I want you to extract TEST DESCRIPTION, RESULT, REF. RANGE, UNIT  from the given file in json format."},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                            },
                        ],
                    }
                ],

                response_format={ "type": "json_object" }
            )
            uid = request.COOKIES.get('uid',None)
            if uid:
                user = User.objects.get(id=uid)
                db = Uploads.objects.create(file = file, created_by=user)
                print(db.pk)
                return Response(
                    json.loads(chat_completion.choices[0].message.content)   
                )
            else:
                return Response(
                    {
                        "status":400
                    },status=400
                )

class SaveView(APIView):
    def post(self, request):
        tests = request.data.get('tests', None)
        fileid = request.data.get('files', None)

        for test in tests:
            description = test['TEST DESCRIPTION']
            result = test['RESULT']
            range = test['REF. RANGE']
            unit = test['UNIT']
            file = Uploads.objects.get(id = fileid)
            db = TEST.objects.create(description = description, result = result, range = range, unit = unit, file = file)
            
            
        
        return Response()
    

class ViewUploadsView(APIView):
    def get(self, request):
        db = Uploads.objects.all()
        data = UploadSerializer(db, many = True)
        return Response(data.data)
    

    def delete(self, request):
        uploadId = request.data.get('id',None)
        db = Uploads.objects.filter(id = uploadId)
        db.delete()
        return Response(data = {
            'message' : 'Your file has been deleted'
        }, status=200 )    

class ViewTestsView(APIView):
    def get(self, request):
        fileId = request.GET.get("id", None)
        db = TEST.objects.filter(file = fileId)
        data = TESTSerializer(db, many = True)
        return Response(data.data)
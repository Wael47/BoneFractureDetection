from django.shortcuts import render
import base64
from .forms import ImageUploadForm
from .image_classification import torchModel
from rest_framework import status
from rest_framework.response import Response
from .models import predictions
from .serializers import BoneFractureDetectionSerializers
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView


def index(request):
    imageURL = predictions = None
    form = ImageUploadForm()
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_bytes = image.file.read()
            encoded_img = base64.b64encode(image_bytes).decode('ascii')
            imageURL = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)

            predictions = torchModel.getPredictions(image_bytes)

            # file = request.FILES["image"]
            # file_name = default_storage.save(file.name, file)
            # file_url = default_storage.path(file_name)
            if predictions == 0:
                predictions = 'Normal'
            else:
                predictions = 'Fractured'

    context = {
        'form': form,
        'imageURL': imageURL,
        'predictions': predictions
    }

    return render(request, 'index.html', context=context)


class BoneFractureDetectionAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = BoneFractureDetectionSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data["image"]
            image_bytes = uploaded_file.file.read()
            prediction = torchModel.getPredictions(image_bytes)
            serializer.validated_data['prediction'] = prediction
            serializer.save()
            response = {
                'image': serializer.data['image'],
                'prediction': prediction[0]
            }
            return Response(
                response,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

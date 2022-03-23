import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import base64
from django import forms
from django.shortcuts import render
from .forms import ImageUploadForm, Loginform
from django.core.files import File
from django.core.files.storage import default_storage
import datetime
from .models import crop_analysis
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

model = tf.keras.models.load_model("C:/Users/bkimathi/Desktop/Crop Disease/Models/2022-03-02-12_07-cropdetectionmodel (1).h5")

model_2 = tf.keras.models.load_model('C:/Users/bkimathi/Desktop/Crop Disease/Models/20220125-14571643122660-trained-mobinetv5.h5',
                                   custom_objects={'KerasLayer': hub.KerasLayer})

unique=('Tomato:Bacterial_Spot','Tomato:Early_Blight','Tomato:Healthy')
class_labels ={0:'jute', 1:'maize', 2:'rice', 3:'sugarcane', 4:'tomato', 5:'wheat'}
image_size = 224
""""
def loginpage(request):
    uservalue=''
    passwordvalue=''

    form = Loginform(request.POST or None)
    if form.is_valid():
        uservalue = form.cleaned_data.get('username')
        passwordvalue = form.cleaned_data.get('password')

        user = authenticate(username = uservalue,password = passwordvalue)
        if user is not None:
            login(request, user)
            context={'form':form,'error':'Successful Login'}

            return render(request,'login.html',context)
        else:
            context={'form':form, 'error':'Username or Password is incorrect'}
            return render(request,'login.html',context)
    else:
        context = {'form':form}
        return render (request,'login.html',context)
"""
def import_and_predict_bytes(image_bytes):

    global detect_disease_label
    image = tf.image.decode_jpeg(image_bytes, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, (image_size,image_size))
    image = np.expand_dims(image,axis=0)
    prediction = model.predict(image)
    prediction_label = class_labels[np.argmax(prediction)]
    #if prediction_label == 'tomato':
    #    detect_disease = model_2.predict(image)
     #   detect_disease_label = unique[np.argmax(detect_disease)]
     #   probability = int(np.max(detect_disease)*100)
      #  return detect_disease_label , str(probability) + '%'
    #else:
     #   prediction_label = print('Crop currently not in prediction list')
     #   return prediction_label

    return prediction_label

def index(request):
    image_uri = None
    predicted_label = None
    if request.method == 'POST':
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_bytes = image.file.read()
            encoded_img = base64.b64encode(image_bytes).decode('ascii')
            image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)
            # get predicted label
            try:
                predicted_label = import_and_predict_bytes(image_bytes)
                post = crop_analysis()
                post.Analysis_REF_No = Analysis_REF_No
                post.Crop = Crop
                post.Status = Status
                post.Date_created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                post.save()

            except RuntimeError as re:
                print(re)

    else:
       form = ImageUploadForm()


    context = {'form': form,
            'image_uri': image_uri,
            'predicted_label': predicted_label
        }
    return render(request, 'index.html', context)
def dashboard(request):
    
    return render(request, 'Cropdetection/index.html')    

def report_table(request):
    analysis_table = crop_analysis.objects.all()
    context = {'analysis_table':analysis_table}

    return render(request, 'Cropdetection/data.html', context)






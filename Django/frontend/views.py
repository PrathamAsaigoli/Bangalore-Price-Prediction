from django.shortcuts import render,HttpResponse
import json
import pickle
import sklearn
import numpy as np

# Create your views here.

location = 0
columns = None
model = None


def load_file():

    global location
    global columns
    global model
    
    
    with open("G:\\Machine_Learning_projects\\Front End\\frontend\\bangalore_home_price_prediction_model.pickle",'rb') as f:
        model = pickle.load(f)

    with open("G:\\Machine_Learning_projects\\Front End\\frontend\\columns.json",'r') as j:
        columns = json.load(j)

    
    local_location = list(columns['data_columns'])
    location = local_location[4:]
    return location

def get_estimated_price(location,sqft,bath_room,balcony,bhk):
    global columns
    load_file()
    local_columns = list(columns['data_columns'])
    try:
        loc_index = local_columns.index(location.lower())
    except:
        loc_index = -1
    x = np.zeros(len(local_columns))  # Creating a vector(containing zeros) having length same as length of X
    # print('length of x is',x)
    x[0] = sqft
    x[1] = bath_room
    x[2] = balcony
    x[3] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    predicted_value  = round(model.predict([x])[0],2)
    # print(predicted_value)
    return predicted_value

def index(request):

    area = bhk = bathrooms = balcony = Location = 0
    
    if request.method == "POST":

        area = request.POST['Squareft']
        bhk = request.POST['uiBHK']
        bathrooms = request.POST['uiBathrooms']
        balcony = request.POST['uiBalcony']
        Location = request.POST['Location']
        # area = request.POST.get('Squareft')
        # bhk = request.POST.get('uiBHK')
        # bathrooms = request.POST.get('uiBathrooms')
        # balcony = request.POST.get('uiBalcony')
        # location = request.POST.get('Location')       


    calculated_area_price  = get_estimated_price(Location,area,bathrooms,balcony,bhk)
    print(calculated_area_price)

    locations = load_file()
    # print(area)
    data = {
        'locations' : locations,
        'calculated_price' : calculated_area_price
    }
    
    return render(request,'app.html',data)





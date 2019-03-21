from django.shortcuts import render
import json
from analysisapp.forms import upload_file_form
from analysisapp.file_upload.file_upload_handling import handle_upload_file
from django.http import HttpResponseRedirect

#from analysisapp.working_code2 import pre_process as prep
from analysisapp.working_code2 import pre_process

# Create your views here.
# from analysisapp.working_code.cleaning import clean_data
# from analysisapp.working_code.createDatabase import create_database_excel


# def splash(request):
#     create_database_excel(100, 175)
#     clean_data()
#     return render(request, 'splash-screen.html')

def index(request):
    return render(request, 'index.html')

def start(request):
    return render(request, 'start.html')

def table(request):
    return render(request, 'data-tables.html')

def Maps(request):
         lat_long=pre_process.maps()
         print(lat_long)
         # print(json.dumps(lat_long))
         return render(request, 'map-vector.html',{
             'lat_long':json.dumps(lat_long,indent=2,sort_keys=True)
         })

def charts(request):

    # pre_process.load_data()
    occupationListCount,occupationList=pre_process.occupation()
    educationListCount, educationList = pre_process.education()
    sexListCount, sexList = pre_process.sex()
    ageListCount,ageList=pre_process.age()

    print(occupationListCount,occupationList)
    return render(request, 'chart-charts.html',{
        'occupationList':json.dumps(occupationList),
        'occupationListCount':json.dumps(occupationListCount),
        'educationList':json.dumps(educationList),
        'educationListCount':json.dumps(educationListCount),
        'sexList':json.dumps(sexList),
        'sexListCount':json.dumps(sexListCount),
        'ageList':ageList,
        'ageListCount':ageListCount,

    })
# #    pre_process.read_data()
#  #   occupationList,occupationListCount=pre_process.occupation()
#
#
#
#
#     return render(request, 'chart-charts.html',{
#         'occupationList':json.dumps(occupationList),
#         'occupationListCount':json.dumps(occupationListCount)
#
#     })

def charts2(request):

    pre_process.get_data()
    accuracy_headers, accuracy = pre_process.analysis_accuracy()
    print(accuracy_headers, accuracy)

    ogLabel = ["Original Data-Not Fraud", "Original Data-Fraud"]
    preLabel = ["Predicted Data-Not Fraud", "Predicted Data-Fraud"]
    original_count, predicted_count = pre_process.analysis_chart_data()
    print("sds", original_count, predicted_count)

    return render(request, 'chart-morris.html',{
        'accuracy_headers':json.dumps(accuracy_headers),
        'accuracy':json.dumps(accuracy),
        'original_count': json.dumps(original_count),
        'predicted_count':json.dumps(predicted_count),
        'ogLabel':json.dumps(ogLabel),
        'preLabel':json.dumps(preLabel)
    })
def table(request):
    data=pre_process.tableData()
    return render(request,'data-tables.html',{
        'data':data,
        'range':range(200)
    })

def morris(request):
    # data=[
    #     ['Credit','Debit','Value'],
    #     [12,30,20],
    # ]
    # data_source=SimpleDataSource(data=data)
    # chart=DonutChart(data_source)
    # context={'chart':chart}
    return render(request, 'chart-morris.html')


def fileforms(request):
    form = upload_file_form()

    # if request.method == "POST":
    #     form = upload_file_form(request.POST, request.FILES)
    #
    #     if form.is_valid():
    #         handle_upload_file(request.FILES['file'])
    #         return HttpResponseRedirect('success.html')
    #     # else:
    #     #     form = upload_file_form()
    #     #     return render(request, 'forms.html', {'form': form})

    return render(request, 'forms.html', context={'form':form})
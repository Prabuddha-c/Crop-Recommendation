from django.shortcuts import render
import requests

# Create your views here.

def Index(request):
    try:
        data = 0
        if request.method == "POST":
            N = request.POST.get('N')
            P = request.POST.get('P')
            K = request.POST.get('K')
            T = request.POST.get('T')
            H = request.POST.get('H')
            PH = request.POST.get('PH')
            R = request.POST.get('R')

            # print(N,P,K,T,H,PH,R)

            N = int(N)
            P = int(P)
            K = int(K)
            T = float(T)
            H = float(H)
            PH = float(PH)
            R = float(R)

            
            if R:

                API_KEY = "s1W4cm3TNrIOfnwTkbA09vXgwOOgJCMibdFHOJGTKl3y"

                token_response = requests.post(
                    'https://iam.cloud.ibm.com/identity/token',
                    data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
                )

                if token_response.status_code != 200:
                    print("Error fetching token:", token_response.json())
                    exit()

                mltoken = token_response.json().get("access_token")



                header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

                payload_scoring = {
                    "input_data": [
                        {
                            "fields": ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"],
                            "values": [[N, P, K, T, H, PH, R]]
                        }
                    ]
                }


                response_scoring = requests.post(
                    'https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/2ad60985-f9db-49d3-b6e5-b2eef3792363/predictions?version=2021-05-01',
                    json=payload_scoring,
                    headers=header,
                    
                )

                print(response_scoring)

                

                if response_scoring.status_code != 200:
                    print("Error in prediction:", response_scoring.json())
                    data = "Error"
                else:
                    # print("Scoring response:", response_scoring.json())
                    print(response_scoring.json()['predictions'][0]['values'][0][0])
                    data = response_scoring.json()['predictions'][0]['values'][0][0]
        
                    
        context = {'prediction':data}
    except:
        data = 0
        context = {'prediction':data}



    return render(request,'index.html', context)

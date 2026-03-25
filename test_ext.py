import urllib.request
import urllib.parse
import json

url = "http://127.0.0.1:5000/predict"
data = {
    "Tenure Months": 12,
    "Monthly Charges": 70.0,
    "Total Charges": 2000.0,
    "Gender": "Male",
    "Senior Citizen": 0,
    "Internet Service": "DSL",
    "Contract": "Month-to-month",
    "Payment Method": "Electronic check"
}
encoded_data = urllib.parse.urlencode(data).encode('utf-8')
try:
    req = urllib.request.Request(url, data=encoded_data)
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        res = response.read().decode('utf-8')
        print("Length:", len(res))
        if "Internal Server Error" in res:
            print("Error found in HTML.")
        else:
            print("Successfully rendered HTML.")
except Exception as e:
    print("Error:", e)

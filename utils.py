'''from kavenegar import *'''

def send_otp_code(phone_number, code):
    pass
'''
    try:
        api = KavenegarAPI('62572B316B5464595767584E7A30645156626D7538426B68515963346436777A43657875314133683178493D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'کد تایید شما برای ورود به *** {code}'
        }

        response = api.sms_send(params)
        print("Response:", response)
    except APIException as e:
        print(f"APIException: {e}")
    except HTTPException as e:
        print(f"HTTPException: {e}")

# نمونه استفاده


class PaymentView(View):
    def post(self, request, order_id):



        
        data = {
            'UserName': 
            'Password': 
            'Mobile': 
            'CodeLength': 
            'OptionalCode':
        }
        
        response = requests.post('https://panel.aqayepardakht.ir/api/v2/create', data=data)
        json_data = json.loads(response.text)

        if response.status_code == 200 and json_data.get('status') == 'success':
            transid = json_data.get('transid')
            if transid:
                return redirect(f'https://panel.aqayepardakht.ir/startpay/sandbox/{transid}')
      
        return render(request, 'orders/load.html')




import requests

# Define the API URL
url = "https://portal.amootsms.com/rest/SendSimple"

# Prepare the payload data
payload = {
    'token': 'xxxx',
    'Mobiles': '091xxxx',
    'SendDateTime': '0',
    'SMSMessageText': 'xxxx',
    'LineNumber': 'Public'
}

# Set the request headers
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Send the POST request
response = requests.post(url, headers=headers, data=payload)

# Print the response text
print(response.text)'''
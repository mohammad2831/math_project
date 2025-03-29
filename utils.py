import requests
from django.conf import settings

class KavenegarSMS:
    API_URL = "https://api.kavenegar.com/v1/{api_key}/sms/send.json"

    def __init__(self):
        self.api_key = '7A596E7A7163534C667836493676706D484674715A54356C3631662F6C646D48396E4E564D6D3757522F553D'

    def send_sms(self, receptor, message):
        """
        ارسال پیامک با استفاده از API کاوه نگار
        :param receptor: شماره گیرنده (مثال: '09123456789')
        :param message: متن پیامک (مثال: 'کد تایید شما: 123456')
        :return: پاسخ JSON از API کاوه نگار
        """
        url = self.API_URL.format(api_key=self.api_key)
        payload = {
            "receptor": receptor,
            "message": message
        }
        try:
            response = requests.post(url, data=payload)
            response_data = response.json()
            if response.status_code == 200 and response_data.get("return", {}).get("status") == 200:
                return response_data
            else:
                return {"error": response_data}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

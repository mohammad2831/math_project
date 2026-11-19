import requests
from django.conf import settings

from sms_ir import SmsIr


def send_message_to_mohammad():
    api_key = getattr(settings, 'SMSIR_API_KEY', '')
    line_number = getattr(settings, 'SMSIR_LINE_NUMBER', '')
    recipient_number = '09033438205'
    message = 'سلام محمد! این یک پیام تستی است.'

    if not api_key or not line_number:
        return {"error": "SMSIR_API_KEY or SMSIR_LINE_NUMBER is not configured"}

    sms_ir = SmsIr(api_key, line_number)
    response = sms_ir.send_sms(recipient_number, message, line_number)
    return response


class KavenegarSMS:
    API_URL = "https://api.kavenegar.com/v1/{api_key}/sms/send.json"

    def __init__(self, api_key=None):
        self.api_key = api_key or getattr(settings, 'KAVENEGAR_API_KEY', '')

    def send_sms(self, receptor, message):
        """
        ارسال پیامک با استفاده از API کاوه نگار
        :param receptor: شماره گیرنده (مثال: '09123456789')
        :param message: متن پیامک (مثال: 'کد تایید شما: 123456')
        :return: پاسخ JSON از API کاوه نگار
        """
        if not self.api_key:
            return {"error": "KAVENEGAR_API_KEY is not configured"}
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

# from ronglian_sms_sdk import SmsSDK
from . import SmsSDK

accId = '8a216da880d67afb018139b2e8a30f6d'
accToken = 'adf832422e5c4907bf80ad3d21550a7d'
appId = '8a216da880d67afb018139b2e9a00f74'


def send_message(tid, mobile, datas):
    sdk = SmsSDK(accId, accToken, appId)
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)


if __name__ == '__main__':
    tid = '1'
    mobile = '18956536914'
    datas = ('6666', 2)
    send_message(tid, mobile, datas)




import requests
import json

# demo: https://www.yunpian.com/doc/zh_CN/introduction/demos/python.html
class YunPian(object):
	def __init__(self, api_key):
		self.api_key = api_key
		# 接口
		self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

	def send_sms(self, code, mobile):
		# 参数
		parmas = {
			"apikey": self.api_key,
			"mobile": mobile,
			"text": "【生鲜超市】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
		}

		response = requests.post(self.single_send_url, data=parmas)
		re_dict = json.loads(response.text)
		return re_dict


# 测试
if __name__ == "__main__":
	yun_pian = YunPian("2b65704bc23ae4ed25f1aa59d61563c1")
	yun_pian.send_sms("2018", "15215212143")
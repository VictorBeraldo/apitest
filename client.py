
import requests

#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file

url = "http://localhost:5000/"
fin = open('00001.wav', 'rb')
files = {'file': fin}
try:
  r = requests.post(url, files=files)
	print (r)
finally:
	fin.close()
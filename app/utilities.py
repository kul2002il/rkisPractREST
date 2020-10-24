from datetime import datetime
from os.path import splitext
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token


def checkAuth(request):
	if not request:
		return Response({'error': 'NotRequest'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
	if 'token' not in request.data:
		return Response({'error': 'NotToken'}, status=HTTP_400_BAD_REQUEST)
	key = request.data['token']
	if not Token.objects.filter(key=key):
		return Response({'error': 'TokenNotAuthorisation'}, status=HTTP_401_UNAUTHORIZED)
	return False
"""{
	"token": "6477f36bdecd56c6150c2e2419116044cd97fb3c",
	"title": "dfdgfkkjdfuvuiic",
	"anons": "Неожиданно",
	"text": "Очень неожиданно"
}
{
	"token": "6477f36bdecd56c6150c2e2419116044cd97fb3c",
	"title": "Изменённый пост",
	"anons": "Неожиданно",
	"text": "Очень неожиданно"
}
{
	"token": "6477f36bdecd56c6150c2e2419116044cd97fb3c",
	"title": "Новый пост",
	"anons": "Неожиданно",
	"text": "Очень неожиданно",
	"tag": [3],
	"image": "https://www.viakoo.com/wp-content/uploads/2018/02/new.png"
}"""


def get_timestamp_path(instance, filename):
	return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])

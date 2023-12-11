from Lcu import LcuRequest

lcu = LcuRequest()
session = lcu.getdata('/swagger/v2/swagger.json').json()
#/data-store/v1/install-dir
print(session)

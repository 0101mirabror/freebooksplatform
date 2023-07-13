FROM python:3.8-slim-buster 
# slim-buster image turi; 3.8 python versiyasi

WORKDIR /app
# app nomli work direcctory yaratadi

COPY requirements.txt requirements.txt
# o'rnatiladigan packagelarni requirements.txt fayldan o'zining 
# yaratgan Workdirdagi requirements.txt faylga ko'chirib oladi

RUN pip3 install -r requirements.txt
#linux os bo'lgani uchun pip3 va python3; requirements.txt #fayldan packagelarni o'rnatish

COPY . .
# ikki nuqta birinchisi root directorydagi barcha fayllarni olib # yaratgan directoryga fayllarni to'liq ko'chiradi

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# CMDda projectni run qilish uchun command va localhost, port

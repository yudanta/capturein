# Captureindonk

## Overview

**captureindonk** merupakan sebuah service untuk melakukan webscreenshoot pada halaman web, dan dapat diakses melalui **API**, hasil image dari web yang di screenshoot disimpan pada storage **amazon s3**.

> Situ pengen mana yang di screenshoot, kita ambilin deh :p

## App requirements
Aplikasi ini membutuhkan celery sebagai message queue dan redis sebagai brokernya

aplikasi ini juga membutuhkan mongodb sebagai database

## Installation

### install dependency 

```
pip install -r requirements.txt
```

### runing app
Runing app

```
python run.py 
```

Runing celery

```
celery -A app.celery worker
```


## Api Definition
nah ini yang paling penting mungkin yak, berikut api definition + flow dari capturiein donk.

*  **Register**

every activity in **capturein** need token key sebagai authenticated method, untuk mendapatkan token key silahkan mendaftar dengan menggunakan username, email dan password.
### Api endpoint
[http://localhost:5000/apis/adduser](http://localhost:5000/apis/adduser)

### method
**POST**

### params
username 	[string][required]

email		[valid email][required]

password	[string][required]

### return
```
{
  "data": {
    "token_key": "g6wFqZCmclvBMZgHJDALIJtuKlY8X2Bb"
  }, 
  "messages": "Success add you as user :p", 
  "response_code": 200
}
```

* **Auth**

untuk mendapatkan token key kembali, pengguna cukup memanggil method auth dengan parameter username/email dan password yang telah di registrasikan 

### Api endpoint
[http://localhost:5000/apis/auth](http://localhost:5000/apis/auth)

### Method
**POST**

### params
username/email 	[string/valid email][required]

password	[string][required]

### return
```
{
    "data": {
        "token_key": "vEKwtwn8uj2ckAtREpN6rNQm7O3JMws5"
    },
    "messages": "Yay... you have been authenticate, please use your token wisely",
    "response_code": 200
}
```

*  **Capture image**

Untuk melakukan capture image pengguna cukup melakukan post pada api endpoint capture dengan parameter token key dan url dari halaman web yang ingin di screenshoot. API akan mengembalikan img_key yang dapat digunakan untuk mengambil data-data image dari web yang di screenshoot, dikarenakan proses pemrosesan yang dilakukan dengan metode asynchronous dan queue, proses pengambilan gambar bisa saja membutuhkan waktu selama beberapa detik/menit. nantinya hasil gambar dapat diambil dengan menggunakan img_key dari output api endpoint ini

### Api endpoint
[http://localhost:5000/apis/capture](http://localhost:5000/apis/capture)

### Method
**POST**

### params
token 		[valid token][required]

url			[valid http url][required]

### return
```
{
    "data": {
        "img_key": "edf36933-790a-4b73-b50a-502db3e7307f"
    },
    "messages": "Success :p",
    "response_code": 200
}
```

* **get captured image by img_code**

Setelah melakukan permintaan untuk mengcapture sebuah halaman web melalui api **capture** dan mendapat kembalian berupa img_key, pengguna dapat mengecek dan mengambil data-data image hasil proses screenshoot halaman web dengan img_key tersebut.

### Api endpoint
[http://localhost:5000/apis/get_image](http://localhost:5000/apis/get_image)

### Method
**GET**

### params
token 		[valid token][required]

img_key			[string][required]

### return
```
{
    "data": {
        "aws_path": "https://s3.amazonaws.com/tolong.capture.donk/public/storage/edf36933-790a-4b73-b50a-502db3e7307f.png",
        "captured_at": null,
        "created_at": "Mon, 15 Sep 2014 04:27:30 GMT",
        "filename": "edf36933-790a-4b73-b50a-502db3e7307f.png",
        "img_key": "edf36933-790a-4b73-b50a-502db3e7307f",
        "is_captured": 1,
        "status": 1,
        "url": "http://ngomongapa.com/~KiQnrqa"
    },
    "messages": "we found it :p",
    "response_code": 200
}
```

* **get all image captured by user**

Untuk melihat daftar atau history halaman yang di screenshoot oleh seorang user dapat mengunakan api get list image dengan memasukkan parametr token. **API** akan mereturn list dari daftar web yang pernah diminta untuk di screenshoot oleh pengguna.

### Api endpoint
[http://localhost:5000/apis/all_images](http://localhost:5000/apis/all_images)

### Method
**GET**

### params
token 		[valid token][required]

limit		[int][optional]

page		[int][optional]

### return
```
{
    "data": {
        "images": [
            {
                "aws_path": "https://s3.amazonaws.com/tolong.capture.donk/public/storage/edf36933-790a-4b73-b50a-502db3e7307f.png",
                "captured_at": null,
                "created_at": "Mon, 15 Sep 2014 04:27:30 GMT",
                "filename": "edf36933-790a-4b73-b50a-502db3e7307f.png",
                "img_key": "edf36933-790a-4b73-b50a-502db3e7307f",
                "is_captured": 1,
                "status": 1,
                "url": "http://ngomongapa.com/~KiQnrqa"
            }
        ]
    },
    "messages": "We found it!",
    "response_code": 200
}
```
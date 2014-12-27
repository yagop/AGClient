AGClient
========

UC3M [AulaGlobal](http://aulaglobal.uc3m.es) (Moodle) from console.

Backup: Can download all files from every course into cursos/id folder.

Of course, this is Open Source, you can checkout the source code and see how secure is.

Usage
----------------------
Backup all your course files:
```
wget https://raw.githubusercontent.com/yagop/AGClient/master/AGClient.py
python AGClient.py -u <NIA> -p <Password>
```

Requirements
----------------------
Python (2.7) is required.

```
sudo apt-get install python
```

Moodle API
----------------------
[Creating a web service client](http://docs.moodle.org/dev/Creating_a_web_service_client)

[Web Services](http://docs.moodle.org/dev/Web_services)

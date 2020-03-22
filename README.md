# Deutschlandkarte à la Bahn
This is a Django-App for [FahrplanDatenGarten](https://github.com/jugendhackt/fahrplandatengarten).

To run it, please first set up a FahrplanDatenGarten dev-enviroment, like described here: https://github.com/Jugendhackt/FahrplanDatenGarten/blob/master/README.md up to (and including) the point `Import Stations from DB`.

After that, you also need to populate the travel-times, with this command:
```
python manage.py netzkarte_distanceimport
```
Now you can run `python manage.py runserver` to start the local webserver, reachable at http://127.0.0.1:8000/netzkarte/

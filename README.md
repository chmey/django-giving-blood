# How to contribute

Make sure you have the required dependencies installed:
- python3
- venv module for python
- pip


```
git clone https://github.com/chrisdpk/django-giving-blood
cd django-giving-blood
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py createcachetable
python manage.py migrate

```

If everything worked without errors, you can now start the django server using

```python manage.py runserver```

Note: In every new shell session you need to source `.venv/bin/activate` again.

Open the web app in your browser: http://localhost:8000

[![Build Status](https://travis-ci.org/chrisdpk/django-giving-blood.svg?branch=dev)](https://travis-ci.org/chrisdpk/django-giving-blood)
[![Coverage Status](https://coveralls.io/repos/github/chrisdpk/django-giving-blood/badge.svg?branch=dev)](https://coveralls.io/github/chrisdpk/django-giving-blood?branch=dev)

#!/bin/bash

source /lemon/virtualenvs/oncallpack/bin/activate
cd /lemon/code/oncallpack
python manage.py runserver 0.0.0.0:8000 --settings=config.settings.production

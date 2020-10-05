#!/bin/bash

echo "Flushing and repopulating lemon server..."

PYTHON=/lemon/virtualenvs/oncallpack/bin/python
MANAGE_FILE=/lemon/code/oncallpack/manage.py
PROJECT_DIR=/lemon/code/oncallpack
POSTGRES_USER=postgres
DB_NAME=oncallpack
DJANGO_SETTINGS_MODULE=config.settings.local

# Stop any running Django development server
echo "Stopping server..."
pkill -f "manage.py"

# Activate the virtual environment
cd $PROJECT_DIR
source /lemon/virtualenvs/oncallpack/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$PROJECT_DIR:$PYTHONPATH

# Drop and re-create the database
echo "Dropping and recreating $DB_NAME..."
sudo -u $POSTGRES_USER bash << EOF
psql -c "DROP DATABASE IF EXISTS $DB_NAME"
psql -c "CREATE DATABASE $DB_NAME"
EOF

# Migrate the database
echo "Migrating $DB_NAME..."
$PYTHON $MANAGE_FILE migrate

# Load new data
#echo "Loading test data into $DB_NAME..."
#cd $PROJECT_DIR
#$PYTHON $MANAGE_FILE loaddata fixtures/data.json

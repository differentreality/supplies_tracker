# Installation on fedora (27)

```bash
# Install system dependencies
sudo dnf install python3-devel redhat-rpm-config

# Create virtual environment
mkvirtualenv --python=/usr/bin/python3 supplier_tracker
pip install -r requirements.txt         # Install dependencies

python manage.py makemigrations         # Create the DB migrations
python manage.py migrate                # Create the DB
python manage.py createsuperuser        # Create a superuser
```
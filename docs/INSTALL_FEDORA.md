# Installation on fedora (27)

```bash
# Install system dependencies
sudo dnf install python3-devel redhat-rpm-config

# Create virtual environment
mkvirtualenv --python=/usr/bin/python3 supplier_tracker
pip install -r requirements.txt         # Install dependencies

python bin/create_dev_database.py       # Create the DB migrations, create the DB with test data, and create a superuser.

User Login: username=testuser password=password
```

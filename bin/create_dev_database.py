# -- Set up Django environment -- #

import sys
import os
import shutil

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supplies_tracker.settings")

import django
django.setup()

# ------------------------------- #


from django.core.management import call_command

from supplies_tracker.models import Item, Items_Storage, Space, Storage, User

# Copy images to media dir
media_dir = '{}/media/'.format(root)
if not os.path.exists(media_dir):
    os.makedirs(media_dir)

img_dir = "{}/bin/imgs/".format(root)
imgs = os.listdir(img_dir)
for img in imgs:
    current_location = '{}/{}'.format(img_dir, img)
    new_location = '{}/{}'.format(media_dir, img)
    shutil.copy(current_location, new_location)

# Delete existing db
existing_db = os.path.join(root, 'db.sqlite3')
os.remove(existing_db)

# Run Migrations
call_command('makemigrations')
call_command('migrate')

# Create Test User
user = User.objects.create_superuser('testuser', 'test@test.com', 'password')

# Create Spaces
house = Space.objects.create(
    name='House',
    description='the pad',
    address="123 Rainbow Rd",
    user=user,
    image="{}/media/house.jpeg".format(root))
office = Space.objects.create(
    name='Office',
    description='Main office.',
    address="456 Jerry Ln",
    user=user,
    image="{}/media/office.jpeg".format(root))
storage = Space.objects.create(
    name='Storage',
    description='storage unit 1',
    address="789 Green Place",
    user=user,
    image="{}/media/storage.jpeg".format(root))

# Create Items
beer = Item.objects.create(
    name="Beer",
    description="The Good Stuff",
    price_bought=2.50,
    image="{}/media/beer.jpeg".format(root))
candy = Item.objects.create(
    name="Candy",
    description="Chocolate",
    price_bought=5.00,
    image="{}/media/candy.jpeg".format(root))
bread = Item.objects.create(
    name="Bread",
    description="Eat with everything",
    price_bought=1.00,
    image="{}/media/bread.jpeg".format(root))

# Create Storage
house_s = Storage.objects.create(
    name='Refrigerator',
    space=house,
    image="{}/media/fridge.jpeg".format(root))
office_s = Storage.objects.create(
    name='Refrigerator',
    space=office,
    image="{}/media/fridge.jpeg".format(root))
storage_s = Storage.objects.create(
    name='Refrigerator',
    space=storage,
    image="{}/media/fridge.jpeg".format(root))

# Link items to storage
storages = [house_s, office_s, storage_s]
items = [beer, candy, bread]
for s in storages:
    for i in items:
        Items_Storage.objects.create(item=i, storage=s, quantity=10)

print(house.image.path)

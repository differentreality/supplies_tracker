# supplies_tracker
Django project for tracking home and office supplies

![](http://cutmypic.com/uploads/title14657817.png)

# What is Supplies Tracker ? 
Supplies tracker is a Django Web Application designed to help people track their supplies in a specific place. The main purpose is to automate the subtraction procedure of Ιtems in Spaces where people interact. 
User manages his Spaces which include "Storages". In Storages , you can add Items , manage & track the quantity of each Item , insert not only cost of each Item but also price of future reimbursement. When an Item is picked out of Storage, quantity is reduced even if the person who picks the Item is not a user of the app.
In the company's office employees share the same Refrigerator and probably it's not easy for everyone to know what's inside when everyone is free to pick anything.
In a HackerSpace which donations are necessary members want to know cost of refrigerator's items and future profit from these items in order to fulfill Space's needs. 
In this manner , Supplies Tracker wants to provide a better goods management and help people collaborate peacefully. 
### History
Supplies Tracker is a project of Software Development Course for MSc in Applied Informatics of Technological Institute of Serres , Greece. 
Coding started at December,2017 

At the moment you can find Supplies Tracker at http://suppliestracker.pythonanywhere.com/


* **This tool is released under the MIT license. You can run, copy, distribute, study, change and improve it. Feel free to contribute and join us. Soon Supplies tracker will have his own domain.**
* The main idea is to create a mobile Application in order to interact with the web, making user's life easier.
* A dream to come true is the connection between refrigerator and a hardware device that reduces easily the quantity when picking an item. It's very exciting having access to your refrigerator  when buying home supplies or to your warehouse if you need something. In road to work, track shared supplies between coworkers. 

* **Installation**

 * Python version 3.6
 * Django Version 1.11.8

Some linux distros may need to define different pip or python. I.e pip3 or pip3.6 instead of pip or python3 or python 3.6 instead of python.
 * Additional packages needed are included in the requirements.txt and can be installed locally typing the command : _pip install --user -r requirements.txt_
 * Creation of tables is necessary : _python manage.py migrate_ and then starting the server : 
_python manage.py runserver_

 * HAML is used instead of simple HTML trying to avoid too much lines of code making our life easier :+1: 



# Welcome To EpicEvents CRM

1. Why

   Develop a secure CRM system internal to the company EpicEvents. A Fronted part managed with Django Admin and a Backend part with API endpoint management.
   3 user profiles have been created: MANAGE - SALES - SUPPORT with different levels of accreditation

2. Getting Started

   This project uses the following technologies:

   - [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
   [![Python badge](https://img.shields.io/badge/Python->=3.10-blue.svg)](https://www.python.org/)


   - [Django](https://www.djangoproject.com)

     Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

   - [Django REST Framwork](https://www.django-rest-framework.org)

     Django REST framework is a powerful and flexible toolkit for building Web APIs.

   - [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

     This ensures you'll be able to install the correct packages without interfering with Python on your machine.

     Before you begin, please ensure you have this installed globally.



3. Installation
   ```shell
   git clone https://github.com/Litibe/p12.git
   ```

   - After cloning, change into the directory and type 
   ```shell
   python3.10 -m venv env
   ```
   <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

   - Next, type 
   ```
      source env/bin/activate
      ```
      You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

   - Rather than hunting around for the packages you need, you can install in one step. Type 
      ```
      pip install -r requirements.txt
      ```
      This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is 
         ```
         pip freeze > requirements.txt
         ```

   - You should now be ready to test the application. In the directory, type either 
      ```
      python manage.py runserver
      ```
      The app should respond with an address you should be able to go to using your browser.  [http://127.0.0.1:8000](http://127.0.0.1:8000])

4. Current Setup SQL database

   You have thus installed the local server on your machine. For the proper functioning of the CRM, the Django server uses a PostGreSQL Database hosted in the "Cloud" for data centralization. No settings for you, just to launch the server with an internet connection on your machine required.
   Warning, an IPV6 internet connection is required for the remote connection to the PostGreSQL database. You can test your internet connection with [Ipleak](https://ipleak.net).


5. Testing

   The test framework used is pytest for tests.
   The [coverage](https://coverage.readthedocs.io/en/6.3.2/) framework is installed to know the coverage of the code under test with settings_file "setup.cfg".

   To run Pytest with tested code coverage: 
   ```
   pytestpytest
   ```

   To run Pytest with export report coverage HTML with verbose mode and details:

   ```
   pytest --cov --cov-report html -v -s
   ```

6. Respect PEP8 PYTHON:
         - Convention Name
            For Python => snake_case
         - Convention Language Python : PEP8
      
      For Flake8 and to have an html report without Python generation error, Open the file env/lib/ptyhon3.10/site_packages/flake8-html/plugin.py, on line 25 remove Markup and insert below : 
       ```
         from markupsafe import Markup
       ```
      
      After activating the virtual environment, you can enter the following command:

      ```
      flake8 --format=html --htmldir=flake_rapport --config=flake8.ini
      ```

      A report in HTML format will be generated in the "flake_rapport" folder, with the argument "max-line-length" set by default to 79 characters per line if not specified.
       In the "flake8.ini" configuration file, the env/ folder is excluded.

7. API Access point : [Documentation PostMan](https://documenter.getpostman.com/view/16769688/Uyr7HyL3) 

| URL                                                                       | METHOD ACCEPTED  | Action                                                                                |   |   |
|---------------------------------------------------------------------------|------------------|---------------------------------------------------------------------------------------|---|---|
| http://127.0.0.1:8000/api/authenticate/login/                             | POST             | Get login token                                                                       
| http://127.0.0.1:8000/api/authenticate/signup/                            | POST             | Creation of a new user, if profile manage                                            
| http://127.0.0.1:8000/api/crm/customer/                                   | GET,POST         | Get list of all customers into DB or create it                                        |   |   |
| http://127.0.0.1:8000/api/crm/customer/id/<id_customer>/                  | GET, PUT, DELETE | Get a customer by this ID, update informations or delete.                             |   |   |
| http://127.0.0.1:8000/api/crm/customer/name/                              | GET              | Search a customer by last_name, first_name or last+first_name                         |   |   |
| http://127.0.0.1:8000/api/crm/customer/mail/<mail_customer>/              | GET              | Search a customer by this mail                                                        |   |   |
| http://127.0.0.1:8000/api/crm/customer/salescontact/<mail_sales_contact>/ | GET              | Search all Customer assigned for a Sale Contact by this mail (profile_staff=="Sales") |   |   |
| http://127.0.0.1:8000/api/crm/customer/supportcontact/<mail_support_contact>/ | GET              | Search all Customer assigned for a Support Contact by this mail (profile_staff=="Support") |   |   |
| http://127.0.0.1:8000/api/crm/contract/                                   | GET, POST        | Get all contracts into DB or create it                                                |   |   |
| http://127.0.0.1:8000/api/crm/contract/amount/<amount_contract>/                   | GET              | Get contract by amount (with or without $)                                            |   |   |
| http://127.0.0.1:8000/api/crm/contract/id/<id_contract>/                  | GET,PUT, DELETE  | Get a contract by this ID, update informations or delete.                             |   |   |
| http://127.0.0.1:8000/api/crm/contract/date/start/<date_start>/                 | GET              | Search a contract by date_start                                                            |   |   |
| http://127.0.0.1:8000/api/crm/contract/date/end/<date_end>/                 | GET              | Search a contract by date_end                                                              |   |   |
| http://127.0.0.1:8000/api/crm/contract/mail/<mail_customer>/                 | GET              | Search contract by mail customer                                                              |   |   |
| http://127.0.0.1:8000/api/crm/contract/name/                 | GET              | Search a contract by last_name, first_name or last+first_name customer                                                           |   |   |
| http://127.0.0.1:8000/api/crm/event/                 | GET,  POST              | Get all events into DB or create it                                                       |   |   |
| http://127.0.0.1:8000/api/crm/event/id/<id_event>/                 | GET, PUT, DELETE             | Get a event by this ID, update informations or delete.                                                       |   |   |
| http://127.0.0.1:8000/api/crm/event/date/start/<date_start>/                 | GET              | Search a event by date_start                                                            |   |   |
| http://127.0.0.1:8000/api/crm/event/date/end/<date_end>/                 | GET              | Search a event by date_end                                                              |   |   |
| http://127.0.0.1:8000/api/crm/event/mail/<mail_customer>/                 | GET              | Search event by mail customer                                                              |   |   |
| http://127.0.0.1:8000/api/crm/event/supportcontact/<mail_support_contact>/                 | GET              | Search event by mail support_contact assigned                                                              |   |   |
| http://127.0.0.1:8000/api/crm/event/name/                 | GET              | Search a event by last_name, first_name or last+first_name customer                                                         |   |   |
| http://127.0.0.1:8000/api/crm/need/                 | GET,  POST              | Get all needs into DB or create it                                                       |   |   |
| http://127.0.0.1:8000/api/crm/need/id/<id_need>/                 | GET, PUT, DELETE             | Get a need by this ID, update informations or delete.                                                       |   |   |
# Welcome To EpicEvents CRM

1. Why

   Elaborer un système CRM sécurisé interne à l'entreprise EpicEvents. Une partie Fronted gérée avec Django Admin et une partie Backend avec la gestion de points de terminaison API.
   3 Profils utilisateurs ont été créé : MANAGE - SALES - SUPPORT avec les différents niveaux d'accréditation

2. Getting Started

   This project uses the following technologies:

   - [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
   [![Python badge](https://img.shields.io/badge/Python->=3.9-blue.svg)](https://www.python.org/)


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
   python3 -m venv env
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
      The app should respond with an address you should be able to go to using your browser. defaut: [http://127.0.0.1:8000](http://127.0.0.1:8000])

4. Current Setup SQL database

   You have thus installed the local server on your machine. For the proper functioning of the CRM, the Django server uses a PostGreSQL Database hosted in the "Cloud" for data centralization. No settings for you, just to launch the server with an internet connection on your machine required.


5. Testing

   The test framework used is pytest for tests.
   The [coverage](https://coverage.readthedocs.io/en/6.3.2/) framework is installed to know the coverage of the code under test with settings_file "setup.cfg".

   To run Pytest with tested code coverage with verbose mode and details: 
   ```
   pytest --cov -v -s
   ```

   To run Pytest with export report coverage HTML :

   ```
   pytest --cov --cov-report html -v -s
   ```

6. Respect PEP8 PYTHON:
         - Convention Name
            For Python => snake_case
         - Convention Language Python : PEP8
         
      After activating the virtual environment, you can enter the following command:

      ```
      flake8 --format=html --htmldir=flake_rapport --config=flake8.ini
      ```

      A report in HTML format will be generated in the "flake_rapport" folder, with the argument "max-line-length" set by default to 79 characters per line if not specified.
       In the "flake8.ini" configuration file, the env/ folder is excluded.


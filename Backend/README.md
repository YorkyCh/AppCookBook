# Mexican Cookbook

This is a Django project for managing and sharing Mexican recipes.

## Getting Started

These instructions will help you set up the project on your local machine.

### Prerequisites

Make sure you have the following software installed:

- Python 3.8 or higher
- pip
- virtualenv

### Installing

Follow these steps to set up the project:

Clone the repository:
git clone https://github.com/yourusername/mexican_cookbook.git

Create a virtual environment and activate it:
#pouzi terminal a vytvor virtual environment
cd Backend # cd do adresare kde je requirements.txt
python3 -m venv venv # On Windows: py -3 -m venv venv, On MAC: python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`, On MAC: source venv/bin/activate

Install the required dependencies:
pip install -r requirements.txt # On Windows: py -m pip install -r requirements.txt, , On MAC: pip install -r requirements.txt

Apply the migrations:
python3 manage.py migrate # On Windows: py manage.py migrate, , On MAC: python manage.py migrate

Start the development server:
python3 manage.py runserver # On Windows: py manage.py runserver, On MAC: python manage.py runserver

The server should now be running at http://127.0.0.1:8000/.


# Voting API for restaurant menus
Employees will vote for the menu before leaving for lunch on a mobile app
for whom the backend has to be implemented. There are users who did not
update the app to the latest version and the backend has to support both
versions. The mobile app always sends the build version in headers

## Functionality  
* To participate in the voting, you must be a registered user.

* User authentication and validation are done using JWT tokens.

* Each employee can vote for a menu only once per day.

* Menu files, restaurants, and their addresses can be manually updated.

* Support for the old version of the application.

## Tech

* DRF
* PostgreSQL
* Docker
* drf-spectacular

## Installation via GitHub
To install the application using GitHub, follow these steps:
1. Navigate to the folder on your computer where you want to clone the project.
2. Execute the following command:
```shell
git clone https://github.com/VladyslavCherkashyn/restaurant_API.git
```
3. Change into the cloned project directory:
```shell
cd Binance-Data-Collector-and-Visualization
```
4. Create a virtual environment for the project:
```shell
python -m venv venv
```
5. Activate the virtual environment:
* On Windows:
```shell
venv\Scripts\activate
```
* On macOS:
```shell
source venv/bin/activate
```
6. Install the dependencies:
```shell
pip install -r requirements.txt
```
7. Create the migrations and migrate:
```shell
python manage.py makemigrations
python manage.py migrate
```

## Configuration
To work with the application, you need to create a .env file in the project's root folder and set the following environment variables:

* POSTGRES_HOST: {PostgreSQL database host}
* POSTGRES_DB: {PostgreSQL database name}
* POSTGRES_USER: {PostgreSQL database user}
* POSTGRES_PASSWORD: {PostgreSQL database password}

## Installation via Docker

* make sure you have installed [Docker](https://www.docker.com/products/docker-desktop/)
* Run ```docker-compose up --build```

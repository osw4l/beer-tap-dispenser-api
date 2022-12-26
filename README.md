# Beer tap dispenser API

Anyone who goes to a festival at least one time knows how difficult is to grab some drinks from the bars. They are
crowded and sometimes queues are longer than the main artist we want to listen!

That's why some promoters are developing an MVP for new festivals. Bar counters where you can go and serve yourself
a beer. This will help make the waiting time much faster, making festival attendees happier and concerts even more
crowded, avoiding delays!

<p align="center">
    <img alt="Tap dispenser" width="300px" src="https://media.tenor.com/zYmG5cqTm-AAAAAC/beer-beer-tap.gif" />
</p>

## How it works?

The aim of this API is to allow organizers to set up these bar counters allowing the attendees self-serving.

So, once an attendee wants to drink a beer they just need to open the tap! The API will start counting how much flow
comes out and, depending on the price, calculate the total amount of money.

You could find the whole description of the API in the [OpenAPI description file](/api.spec.yaml) and send request to a
mock server with [this URL](https://rviewer.stoplight.io/docs/beer-tap-dispenser/juus8uwnzzal5-beer-tap-dispenser)

### Workflow

The workflow of this API is as follows:

1. Admins will **create the dispenser** by specifying a `flow_volume`. This config will help to know how many liters of
   beer come out per second and be able to calculate the total spend.
2. Every time an attendee **opens the tap** of a dispenser to puts some beer, the API will receive a change on the
   corresponding dispenser to update the status to `open`. With this change, the API will start counting how much time
   the tap is open and be able to calculate the total price later
3. Once the attendee **closes the tap** of a dispenser, as the glass is full of beer, the API receives a change on the
   corresponding dispenser to update the status to `close`. At this moment, the API will stop counting and mark it
   closed.

At the end of the event, the promoters will want to know how much money they make with this new approach. So, we have to
provide some information about how many times a dispenser was used, for how long, and how much money was made with each
service.

> ⚠️ The promoters could check how much money was spent on each dispenser while an attendee is taking beer!
> So you have to control that by calculating the time diff between the tap opening and the request time

---

## What are we looking for?

* **A well-designed solution and architecture.** Avoid duplication, extract re-usable code
  where makes sense. We want to see that you can create an easy-to-maintain codebase.
* **Test as much as you can.** One of the main pain points of maintaining other's code
  comes when it does not have tests. So try to create tests covering, at least, the main classes.
* **Document your decisions**. Try to explain your decisions, as well as any other technical requirement (how to run the
  API, external dependencies, etc ...)

This repository is a Python skeleton with Django & PostgreSQL designed for quickly getting started developing an API.
Check the [Getting Started](#getting-started) for full details.

## Technologies

* [Python 3.9](https://www.python.org/downloads/release/python-390/)
* [Django](https://docs.djangoproject.com/en/4.0/releases/4.0/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [Poetry](https://python-poetry.org/)
* [Coverage](https://coverage.readthedocs.io/en/6.3.1/)
* [Docker](https://www.docker.com/)
* [Make](https://www.gnu.org/software/make/manual/make.html)

## Getting Started

Within the [Makefile](Makefile) you can handle the entire flow to get everything up & running:

1. Install `make` on your computer, if you do not already have it.
2. Build the Docker image: `make build`
3. Migrate any DB pending task: `make migrate`
4. Start the application: `make up`

--- 

# Technical Decisions

### Packages installed 

<img width="490" alt="Captura de Pantalla 2022-11-17 a la(s) 4 32 43 p m" src="https://user-images.githubusercontent.com/8086136/202675754-8687f579-c847-49fb-87ef-8ae6d57d948a.png">

- [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) swagger implementation **easy to implement** on **Django** projects, api docs available on -> http://0.0.0.0:5050/, this library was used to generate api docs 
<img width="1459" alt="Captura de Pantalla 2022-11-18 a la(s) 3 54 32 a m" src="https://user-images.githubusercontent.com/8086136/202680672-7f556eb5-ee05-4ece-8b4d-8469fc0624d3.png">

the api docs contains the schemes for all the projects

- [factory-boy](https://factoryboy.readthedocs.io/en/stable/) to create mocked data using django models through factories
- [django-extensions](https://github.com/django-extensions/django-extensions) for the aliases of the urls (to use **reverse('api:url')** instead of **/api/url'**), because is safer than use the link in the code, this package was used just on development (already removed)
<img width="886" alt="Captura de Pantalla 2022-11-18 a la(s) 11 06 00 a m" src="https://user-images.githubusercontent.com/8086136/202676296-112ed33e-8afa-436b-a9ce-a4e235132ebd.png">

### aliases of urls in the console
<img width="821" alt="Captura de Pantalla 2022-11-17 a la(s) 4 32 08 p m" src="https://user-images.githubusercontent.com/8086136/202675420-f27b9d2c-168f-48c6-a568-a8306af495d4.png">

### pyproject.toml after finish development
<img width="523" alt="Captura de Pantalla 2022-11-18 a la(s) 11 17 42 a m" src="https://user-images.githubusercontent.com/8086136/202678744-2909daa3-7228-477e-9986-33d26cb1ce71.png">


### Commands added

- static command was added to the make file and to the up command also because we need to run this commands to see the api docs that requires static files

<img width="602" alt="Captura de Pantalla 2022-11-18 a la(s) 3 54 16 a m" src="https://user-images.githubusercontent.com/8086136/202675520-0305af64-9a30-45d6-b3c6-f013672c66ac.png">

<img width="588" alt="Captura de Pantalla 2022-11-18 a la(s) 11 38 54 a m" src="https://user-images.githubusercontent.com/8086136/202684431-18658dd1-eacb-449e-8818-f23cc011f3e7.png">

- **django.contrib.staticfiles** added, because is required to use **drf-yasg**

<img width="698" alt="Captura de Pantalla 2022-11-18 a la(s) 11 31 24 a m" src="https://user-images.githubusercontent.com/8086136/202681806-007f7add-7777-4107-a538-8b8a076cb685.png">

<img width="1137" alt="Captura de Pantalla 2022-11-18 a la(s) 11 32 10 a m" src="https://user-images.githubusercontent.com/8086136/202682064-f069ee85-477c-439d-929f-b106643de520.png">

- **PRICE_BY_LITER** and **TIME_ZONE** added to the settings 
<img width="1141" alt="Captura de Pantalla 2022-11-18 a la(s) 11 33 31 a m" src="https://user-images.githubusercontent.com/8086136/202682542-539bd7b8-cc4f-4cea-bc8e-f536cbf88933.png">

- **COERCE_DECIMAL_TO_STRING** added to **REST_FRAMEWORK** settings, to send decimals as number instead of string 

<img width="1217" alt="Captura de Pantalla 2022-11-18 a la(s) 11 35 40 a m" src="https://user-images.githubusercontent.com/8086136/202683269-e8e00f08-ac71-4e56-9db8-2d80a13b1494.png">

<img width="545" alt="Captura de Pantalla 2022-11-18 a la(s) 11 35 57 a m" src="https://user-images.githubusercontent.com/8086136/202683401-609a81c5-270d-4ad0-98d3-413a80bd1bd5.png">

- ports added to **postgres-skeleton-db** container in order to connect outside the container

<img width="534" alt="Captura de Pantalla 2022-11-18 a la(s) 11 37 15 a m" src="https://user-images.githubusercontent.com/8086136/202683839-78b4a81b-9f3f-44e7-9905-4aade7190e0f.png">
<img width="1325" alt="Captura de Pantalla 2022-11-18 a la(s) 11 42 21 a m" src="https://user-images.githubusercontent.com/8086136/202685696-03433ea3-fed2-4d74-bc80-399a53d1d955.png">
<img width="691" alt="Captura de Pantalla 2022-11-18 a la(s) 11 42 38 a m" src="https://user-images.githubusercontent.com/8086136/202685765-728625ee-8019-4deb-8789-e5b08c62d89d.png">

- UUID as primary key 

<img width="663" alt="Captura de Pantalla 2022-11-18 a la(s) 11 54 16 a m" src="https://user-images.githubusercontent.com/8086136/202689036-a5bee8b4-5b27-4abf-9b20-3df28f9f0e1e.png">

- TextChoices to status values
<img width="552" alt="Captura de Pantalla 2022-11-18 a la(s) 11 54 51 a m" src="https://user-images.githubusercontent.com/8086136/202689184-867020a1-bef3-46bf-80f6-52c1f2da23f3.png">

<img width="772" alt="Captura de Pantalla 2022-11-18 a la(s) 11 55 21 a m" src="https://user-images.githubusercontent.com/8086136/202689288-39ee33be-9014-47fd-9210-f0af64146861.png">

- migrations folder created

<img width="181" alt="Captura de Pantalla 2022-11-18 a la(s) 11 56 23 a m" src="https://user-images.githubusercontent.com/8086136/202689489-c2799996-e9df-461c-992d-a5322235e4df.png">

### testing 

33 tests added successfully 

<img width="956" alt="Captura de Pantalla 2022-11-18 a la(s) 11 51 59 a m" src="https://user-images.githubusercontent.com/8086136/202688607-35d96b7f-0c16-4635-bd06-1bc91b3a849c.png">

100% of coverage 🚀 🔥 😎

<img width="511" alt="Captura de Pantalla 2022-11-18 a la(s) 12 03 59 p m" src="https://user-images.githubusercontent.com/8086136/202691078-c4e3eaa9-a5d6-4791-9e92-eba6d5b654cb.png">

- I've added **# pragma: no cove**r to these methods because are not being used

<img width="737" alt="Captura de Pantalla 2022-11-18 a la(s) 12 05 08 p m" src="https://user-images.githubusercontent.com/8086136/202691191-1e0b08c5-f9cf-4f70-acf2-e297a5644800.png">

<p align="center">
  Made with ❤️ by <a href="https://github.com/osw4l">osw4l</a>
</p>

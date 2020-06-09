- [Mealvery App](#mealvery-app)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [App Description](#App-Business-Logic-Description)
- [API Documentation](#api-documentation)

## Mealvery App

Mealvery app is an API, to let people create dishes and menus, in order to send them to any slack team (with previous configuration), in order users that receive the link, can enter to the API and sign-up and make an order, with those dishes that daily basis menus offer.

## Installation

### Clone Repository

`git clone https://github.com/AlonsoSalas/Backend-Test-Salas.git`

`cd Backend-Test-Salas`

### Starting the app

#### Environment Variables

In this repository there is a `.env.example` with these variables, you have to create a `.env` file and fill these variables

| Variable              | Description                                                                                 |
| --------------------- | ------------------------------------------------------------------------------------------- |
| `SECRET_KEY`          | Django secret_key                                                                           |
| `PSQL_ENGINE`         | The PSQL Database engine                                                                    |
| `PSQL_DATABASE`       | The database name                                                                           |
| `PSQL_USER`           | The database user                                                                           |
| `PSQL_PASSWORD`       | The database password                                                                       |
| `PSQL_HOST`           | The database host                                                                           |
| `PSQL_PORT`           | The database port                                                                           |
| `SLACK_TOKEN`         | Bot Token from slack used to send message to the team                                       |
| `TODAY_MENU_URL`      | This is going to be the URL that the users are going to receive through slack               |
| `AMPQ_URI`            | The amqp uri that is going to work as a broker with the worker to send message periodically |
| `LIMIT_HOUR_TO_ORDER` | this is set to stablish a limit hour to receive orders                                      |

- Lets create those containers
  `docker-compose up`

- Once our containers are running lets migrate the database
  `docker exec -it backend-test-salas_app_1 python manage.py migrate`

- Creating the admin user
  `docker exec -it backend-test-salas_app_1 python manage.py createsuperuser`

- Running unit tests
  `docker exec -it backend-test-salas_app_1 python -m pytest -v`

#### Slack Setup

In order to connect our worker to your slack team, We need a [slack bot token](https://api.slack.com/authentication/token-types#bot). In order to get that you have to create a new slack app, and then obtain the slack bot token.

After that you have to give to that Bot Token the following Auth Scopes:

- [`users:read`](https://api.slack.com/scopes/users:read)
- [`channels:manage`](https://api.slack.com/scopes/channels:manage)
- [`groups:write`](https://api.slack.com/scopes/groups:write)
- [`im:write`](https://api.slack.com/scopes/im:write)
- [`mpim:write`](https://api.slack.com/scopes/mpim:write)
- [`chat:write`](https://api.slack.com/scopes/chat:write)

And that is it, we are ready to consume our API

## App Business Logic Description

**Administrator (Nora):**

Nora as admin will create the dishes, and the Menus. She will set the dishes to those menus, and the dishes can belong to any Menu. As an admin user she will see all the orders that the regular users will be sending.

**Regular users:**

In order to become regular users, the users will have to signup on the platform. Once they are on the platform the can create orders on the todays menu. Also they can see all the orders they have created.

Regarding the initial requirements, these are the features this app come with:

## API Documentation

For the Api documentation I used the [Swagger Editor](https://editor.swagger.io/). The file `api-docs.yml` contains the description of the API based on OpenApi specifications. copy the content of `api-docs.yml` and paste on the [Swagger Editor](https://editor.swagger.io/)

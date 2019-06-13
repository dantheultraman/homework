# Homework Event Management App

### Requirements
[docker-compose](https://docs.docker.com/compose/install/) is required to run this app.

### Configuration
If custom configuration is required, edit **docker-compose.yml** file and amend environment variables for **app** as desired (i.e. line 16-17).
e.g.
```
environment:
  - notice_email=daniel.lin.821@gmail.com
  - smtp_sender=event_organiser@gmail.com
```

### Start
To start the application, run:
```sh
docker-compose up
```

### REST endpoints
To interact with the application, the following endpoints are available:

##### List all events
GET /events
e.g.
```sh
$ curl http://0.0.0.0:5000/events
```

##### Get an event
GET /events/{event_id}
e.g.
```sh
$ curl http://0.0.0.0:5000/events/1
```

##### Create an event
POST /events

| Attributes  | Format |
| ------------- | ---------------- |
| name  | STR  |
| location  | STR  |
| start | %Y-%m-%d %H:%M |
| end | %Y-%m-%d %H:%M |

e.g.
```sh
$ curl -X POST http://0.0.0.0:5000/events -H "Content-Type: application/json" -d '{"name": "Daniel Birthday Party", "location": "Tokyo", "start": "2019-08-21 20:00", "end": "2019-08-22 00:00"}'
```

##### Delete an event
DELETE /events/{event_id}
e.g.
```sh
$ curl -X DELETE http://0.0.0.0:5000/events/1
```

##### List all users
GET /users
e.g.
```sh
$ curl http://0.0.0.0:5000/users
```

##### Create a new user
POST /users

| Attributes | Example |
| ------ | ----------------- |
| email | daniel@gmail.com |

e.g.
```sh
$ curl -X POST http://0.0.0.0:5000/users -H "Content-Type: application/json" -d '{"email": "daniel@gmail.com"}'
```

##### Delete a user
DELETE /users

| Attributes | Example |
| ------ | ----------------- |
| email | daniel@gmail.com |

e.g.
```sh
$ curl -X DELETE http://0.0.0.0:5000/users -H "Content-Type: application/json" -d '{"email": "daniel@gmail.com"}'
```

##### Subscribe a user to an event
POST /events/{event_id}/subscribe

| Attributes | Example |
| ------ | ----------------- |
| email | daniel@gmail.com |

e.g.
```sh
$ curl -X POST localhost:5000/events/1/subscribe -H "Content-Type: application/json" -d '{"email": "daniel@gmail.com"}'
```

##### Subscribe a user to an event
POST /events/{event_id}/unsubscribe

| Attributes | Example |
| ------ | ----------------- |
| email | daniel@gmail.com |

e.g.
```sh
$ curl -X POST localhost:5000/events/1/unsubscribe -H "Content-Type: application/json" -d '{"email": "daniel@gmail.com"}'
```

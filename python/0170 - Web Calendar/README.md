This is the *Web Calendar* project I made myself.


<p>Afraid to miss something interesting? Don't worry, you won't! Create an app that will save all your events to the database. You will access the events with the help of REST endpoints.</p><br/><br/>Learn more at <a href="https://hyperskill.org/projects/170?utm_source=ide&utm_medium=ide&utm_campaign=ide&utm_content=project-card">https://hyperskill.org/projects/170</a>

Here's the link to the project: https://hyperskill.org/projects/170

Check out my profile: https://hyperskill.org/profile/1254124


Usage

Example 1
```
curl --location 'http://10.2.0.2:5000/event'
```
```json
{
    "message": "The event doesn't exist!"
}
```
Example 2
```
curl --location 'http://10.2.0.2:5000/event' \
--form 'date="2023-10-24"' \
--form 'event="Hello, world 1"'
```
```json
{
    "date": "2023-10-24",
    "event": "Hello, world 1",
    "message": "The event has been added!"
}
```
Example 3
```
curl --location 'http://10.2.0.2:5000/event' \
--form 'date="2023-10-25"' \
--form 'event="Random 1"'
```
```json
{
    "date": "2023-10-25",
    "event": "Random 1",
    "message": "The event has been added!"
}
```
Example 4
```
curl --location 'http://10.2.0.2:5000/event' \
--form 'date="2023-10-25"' \
--form 'event="Random 2"'
```
```json
{
    "date": "2023-10-25",
    "event": "Random 2",
    "message": "The event has been added!"
}
```
Example 5
```
curl --location 'http://10.2.0.2:5000/event' \
--form 'date="2023-10-26"' \
--form 'event="Random 3"'
```
```json
{
    "date": "2023-10-26",
    "event": "Random 3",
    "message": "The event has been added!"
}
```
Example 6
```
curl --location 'http://10.2.0.2:5000/event'
```
```json
[
    {
        "date": "2023-10-24",
        "event": "Hello, world 1",
        "id": 1
    },
    {
        "date": "2023-10-25",
        "event": "Random 1",
        "id": 2
    },
    {
        "date": "2023-10-25",
        "event": "Random 2",
        "id": 3
    },
    {
        "date": "2023-10-26",
        "event": "Random 3",
        "id": 4
    }
]
```
Example 7
```
curl --location 'http://10.2.0.2:5000/event/today'
```
```json
[
    {
        "date": "2023-10-25",
        "event": "Random 1",
        "id": 2
    },
    {
        "date": "2023-10-25",
        "event": "Random 2",
        "id": 3
    }
]
```

Example 8
```
curl --location 'http://10.2.0.2:5000/event?start_time=2023-10-25&end_time=2023-10-26'
```
```json
[
    {
        "date": "2023-10-25",
        "event": "Random 1",
        "id": 2
    },
    {
        "date": "2023-10-25",
        "event": "Random 2",
        "id": 3
    },
    {
        "date": "2023-10-26",
        "event": "Random 3",
        "id": 4
    }
]
```

Example 9
```
curl --location --request DELETE 'http://10.2.0.2:5000/event/3'
```
```json
{
    "message": "The event has been deleted!"
}
```

Example 10
```
curl --location 'http://10.2.0.2:5000/event/2'
```
```json
{
    "date": "2023-10-25",
    "event": "Random 1",
    "id": 2
}
```
Example 11
```
curl --location 'http://10.2.0.2:5000/event'
```
```json
[
    {
        "date": "2023-10-24",
        "event": "Hello, world 1",
        "id": 1
    },
    {
        "date": "2023-10-25",
        "event": "Random 1",
        "id": 2
    },
    {
        "date": "2023-10-26",
        "event": "Random 3",
        "id": 4
    }
]
```

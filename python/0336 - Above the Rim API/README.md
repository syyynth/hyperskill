This is the *Above the Rim API* project I made myself.


<p>As a huge basketball fan, you host the local sports news site <em>Above the Rim</em> on the school's website. You don't have any problems with publishing the NBA or European league because they are available, but the varsity league results are hard to find. That's why you decided to create an API where other enthusiasts like you can post games result right after a match is over!</p><br/><br/>Learn more at <a href="https://hyperskill.org/projects/336?utm_source=ide&utm_medium=ide&utm_campaign=ide&utm_content=project-card">https://hyperskill.org/projects/336</a>

Here's the link to the project: https://hyperskill.org/projects/336

Check out my profile: https://hyperskill.org/profile/1254124

### Usage:

Example 1
```text
curl --location 'http://10.2.0.2:5000/api/v1/teams'
```
```json
{
    "data": {},
    "success": true
}
```
Example 2
```
curl --location 'http://10.2.0.2:5000/api/v1/teams' \
--header 'Content-Type: application/json' \
--data '{
    "short": "PRW",
    "name": "Prague Wizards"
}'
```
```json
{
    "data": "Team has been added",
    "success": true
}
```

Example 3
```
curl --location 'http://10.2.0.2:5000/api/v1/teams' \
--header 'Content-Type: application/json' \
--data '{
    "short": "CHG",
    "name": "Chicago Gulls"
}'
```
```json
{
    "data": "Team has been added",
    "success": true
}
```
Example 4
```
curl --location 'http://10.2.0.2:5000/api/v1/teams'
```
```json
{
    "data": {
        "CHG": "Chicago Gulls",
        "PRW": "Prague Wizards"
    },
    "success": true
}
```
Example 5
```
curl --location 'http://10.2.0.2:5000/api/v1/games' \
--header 'Content-Type: application/json' \
--data '{
    "home_team": "CHG",
    "visiting_team": "PRW",
    "home_team_score": 123,
    "visiting_team_score": 89
}'
```
```json
{
    "data": "Game has been added",
    "success": true
}
```
Example 6
```
curl --location 'http://10.2.0.2:5000/api/v1/games' \
--header 'Content-Type: application/json' \
--data '{
    "home_team": "PRW",
    "visiting_team": "CHG",
    "home_team_score": 76,
    "visiting_team_score": 67
}'
```
```json
{
    "data": "Game has been added",
    "success": true
}
```
Example 7
```
curl --location 'http://10.2.0.2:5000/api/v1/games'
```
```json
{
    "data": {
        "1": "Chicago Gulls 123:89 Prague Wizards",
        "2": "Prague Wizards 76:67 Chicago Gulls"
    },
    "success": true
}
```
Example 8
```
curl --location 'http://10.2.0.2:5000/api/v1/games' \
--header 'Content-Type: application/json' \
--data '{
    "home_team": "CHG",
    "visiting_team": "PRS",
    "home_team_score": 123,
    "visiting_team_score": 89
}'
```
```json
{
    "data": "Wrong team short",
    "success": false
}
```
Example 9
```
curl --location 'http://10.2.0.2:5000/api/v1/team/PRW'
```
```json
{
    "data": {
        "lost": 1,
        "name": "Prague Wizards",
        "short": "PRW",
        "win": 1
    },
    "success": true
}
```

Example 10
```
curl --location 'http://10.2.0.2:5000/api/v1/team/PRS'
```
```json
{
    "data": "There is no team PRS",
    "success": false
}
```
Example 11
```
curl --location 'http://10.2.0.2:5000/api/v2/games' \
--header 'Content-Type: application/json' \
--data '{"home_team": "PRW", "visiting_team": "CHG"}'
```
```json
{
    "data": 3,
    "success": true
}
```
Example 12
```
curl --location 'http://10.2.0.2:5000/api/v2/games'
```
```json
{
    "data": {
        "1": "Chicago Gulls 123:89 Prague Wizards",
        "2": "Prague Wizards 76:67 Chicago Gulls",
        "3": "Prague Wizards 0:0 Chicago Gulls"
    },
    "success": true
}
```
Example 13
```
curl --location 'http://10.2.0.2:5000/api/v2/games/3' \
--header 'Content-Type: application/json' \
--data '{"quarters": "12:15"}'
```
```json
{
    "data": "Score updated",
    "success": true
}
```
Example 14
```
curl --location 'http://10.2.0.2:5000/api/v2/games/3' \
--header 'Content-Type: application/json' \
--data '{"quarters": "21:18"}'
```
```json
{
    "data": "Score updated",
    "success": true
}
```
Example 15
```
curl --location 'http://10.2.0.2:5000/api/v2/games'
```
```json
{
    "data": {
        "1": "Chicago Gulls 123:89 Prague Wizards",
        "2": "Prague Wizards 76:67 Chicago Gulls",
        "3": "Prague Wizards 33:33 Chicago Gulls (12:15,21:18)"
    },
    "success": true
}
```
Example 16
```
curl --location 'http://10.2.0.2:5000/api/v1/games'
```
```json
{
    "data": {
        "1": "Chicago Gulls 123:89 Prague Wizards",
        "2": "Prague Wizards 76:67 Chicago Gulls",
        "3": "Prague Wizards 33:33 Chicago Gulls"
    },
    "success": true
}
```
Example 17
```
curl --location 'http://10.2.0.2:5000/api/v2/games/6' \
--header 'Content-Type: application/json' \
--data '{"id": 6, "quarters": "12:20"}'
```
```json
{
    "data": "There is no game with id 6",
    "success": false
}
```
Example 18
```
curl --location 'http://10.2.0.2:5000/api/v2/games/3' \
--header 'Content-Type: application/json' \
--data '{"quarters": "12:21"}'
```
```json
{
    "data": "Score updated",
    "success": true
}
```
Example 19
```
curl --location 'http://10.2.0.2:5000/api/v2/games/3' \
--header 'Content-Type: application/json' \
--data '{"quarters": "20:12"}'
```
```json
{
    "data": "Score updated",
    "success": true
}
```
Example 20
```
curl --location 'http://10.2.0.2:5000/api/v2/games/3' \
--header 'Content-Type: application/json' \
--data '{"quarters": "3:9"}'
```
```json
{
    "data": "Score updated",
    "success": true
}
```
Example 21
```
curl --location 'http://10.2.0.2:5000/api/v2/games'
```
```json
{
    "data": {
        "1": "Chicago Gulls 123:89 Prague Wizards",
        "2": "Prague Wizards 76:67 Chicago Gulls",
        "3": "Prague Wizards 68:75 Chicago Gulls (12:15,21:18,12:21,20:12,3:9)"
    },
    "success": true
}
```
Example 22
```
curl --location 'http://10.2.0.2:5000/api/v1/games'
```
```json
{
    "data": {
        "1": "Chicago Gulls 123:89 Prague Wizards",
        "2": "Prague Wizards 76:67 Chicago Gulls",
        "3": "Prague Wizards 68:75 Chicago Gulls"
    },
    "success": true
}
```

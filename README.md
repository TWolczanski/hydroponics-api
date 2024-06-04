# API documentation
## Authentication
### `POST /auth/registration`
Registers a new user.

Request example:
```json
{
  "username": "user1",
  "email": "user1@example.com",
  "password1": "user1password",
  "password2": "user1password"
}
```

### `POST /auth/login`
Returns a token that can be used to authenticate requests via the `Authorization` HTTP header (e.g. `Authorization: Token 23832c3b8fbc540dde320e157240ade154353dac`) and sets the `sessionid` cookie for session authentication.

Request example:
```json
{
  "username": "user1",
  "password": "user1password"
}
```

Response example:
```json
{
  "key": "23832c3b8fbc540dde320e157240ade154353dac"
}
```

## Hydroponic systems
### `GET /hydroponic_systems`
Query parameters:
* `name`, e.g. `name=some_name`
* `plant_count`, e.g. `plant_count=3`
* `plant_count__gte`, e.g. `plant_count__gte=3` (`plant_count >= 3`)
* `plant_count__lte`, e.g. `plant_count__lte=3` (`plant_count <= 3`)
* `created_at`, e.g. `created_at=2016-01-01T8:00:00+01:00`
* `created_at__gte`, e.g. `created_at__gte=2016-01-01T8:00:00+01:00` (`created_at >= 2016-01-01T8:00:00+01:00`)
* `created_at__lte`, e.g. `created_at__lte=2016-01-01T8:00:00+01:00` (`created_at <= 2016-01-01T8:00:00+01:00`)
* `ordering`, e.g. `ordering=plant_count` (supports ordering by `name`, `plant_count` and `created_at`)
* `page`, e.g. `page=2`

Returns a paginated list of user's hydroponic systems.

Response example:
```json
{
  "count": 20,
  "next": "http://127.0.0.1:8000/hydroponic_systems?page=3",
  "previous": "http://127.0.0.1:8000/hydroponic_systems?page=1",
  "results": [
    {
      "id": 1,
      "name": "Lorem ipsum",
      "description": "Dolor sit amet",
      "plant_count": 3,
      "created_at": "2022-09-18T15:12:09+0000"
    },
    ...
  ]
}
```

### `GET /hydroponic_systems/{id}`
Returns a hydroponic system with the given id.

Response example:
```json
{
  "id": 1,
  "name": "Lorem ipsum",
  "description": "Dolor sit amet",
  "plant_count": 3,
  "created_at": "2022-09-18T15:12:09+0000",
  "recent_sensor_readings": [
    {
      "id": 1,
      "ph": "3.7",
      "water_temp": "20.1",
      "tds": "400.5",
      "hydroponic_system": 1,
      "created_at": "2022-09-18T15:12:09+0000"
    },
    ...
  ]
}
```

### `POST /hydroponic_systems`
Creates a hydroponic system.

Request example:
```json
{
  "name": "Lorem ipsum",
  "description": "Dolor sit amet",
  "plant_count": 3
}
```

### `PUT /hydroponic_systems/{id}`
Updates a hydroponic system.

Request example:
```json
{
  "name": "Lorem ipsum",
  "description": "Dolor sit amet",
  "plant_count": 5
}
```

### `PATCH /hydroponic_systems/{id}`
Partially updates a hydroponic system.

Request example:
```json
{
  "plant_count": 5
}
```

### `DELETE /hydroponic_systems/{id}`
Deletes a hydroponic system with the given id.

## Sensor readings
### `GET /sensor_readings`
Query parameters:
* `ph`, e.g. `ph=3.5`
* `ph__gte`, e.g. `ph__gte=3.5` (`ph >= 3.5`)
* `ph__lte`, e.g. `ph__lte=3.5` (`ph <= 3.5`)
* `water_temp`, e.g. `water_temp=20.1`
* `water_temp__gte`, e.g. `water_temp__gte=20.1` (`water_temp >= 20.1`)
* `water_temp__lte`, e.g. `water_temp__lte=20.1` (`water_temp <= 20.1`)
* `tds`, e.g. `tds=400.6`
* `tds__gte`, e.g. `tds__gte=400.6` (`tds >= 400.6`)
* `tds__lte`, e.g. `tds__lte=400.6` (`tds <= 400.6`)
* `hydroponic_system`, e.g. `hydroponic_system=1`
* `created_at`, e.g. `created_at=2016-01-01T8:00:00+01:00`
* `created_at__gte`, e.g. `created_at__gte=2016-01-01T8:00:00+01:00` (`created_at >= 2016-01-01T8:00:00+01:00`)
* `created_at__lte`, e.g. `created_at__lte=2016-01-01T8:00:00+01:00` (`created_at <= 2016-01-01T8:00:00+01:00`)
* `ordering`, e.g. `ordering=water_temp` (supports ordering by `ph`, `water_temp`, `tds` and `created_at`)
* `page`, e.g. `page=2`

Returns a paginated list of sensor readings related to user's hydroponic systems.

Response example:
```json
{
  "count": 20,
  "next": "http://127.0.0.1:8000/sensor_readings?page=3",
  "previous": "http://127.0.0.1:8000/sensor_readings?page=1",
  "results": [
    {
      "id": 1,
      "ph": "3.7",
      "water_temp": "20.1",
      "tds": "400.5",
      "hydroponic_system": 1,
      "created_at": "2022-09-18T15:12:09+0000"
    },
    ...
  ]
}
```

### `POST /sensor_readings`
Creates a sensor reading for the given hydroponic system.

Request example:
```json
{
  "ph": "3.7",
  "water_temp": "20.1",
  "tds": "400.5",
  "hydroponic_system": 1,
}
```
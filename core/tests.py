import urllib.parse
from rest_framework import test
from rest_framework import status
from django.urls import reverse
from core.factories import HydroponicSystemFactory, SensorReadingFactory, UserFactory


class APITestCase(test.APITestCase):
    def request(
        self,
        method,
        view_name,
        view_kwargs=None,
        query_params=None,
        data=None,
        user=None,
    ):
        url = reverse(view_name, kwargs=view_kwargs)
        if query_params:
            query_string = urllib.parse.urlencode(query_params)
            url = f"{url}?{query_string}"

        self.client.force_authenticate(user=user)

        return getattr(self.client, method)(url, data=data)


class TestHydroponicSystems(APITestCase):
    def setUp(self):
        self.users = UserFactory.create_batch(2)
        self.systems = [
            HydroponicSystemFactory(
                name="system1",
                plant_count=3,
                owner=self.users[0],
                created_at="2024-06-04T13:00:00Z",
            ),
            HydroponicSystemFactory(
                name="system2",
                plant_count=3,
                owner=self.users[0],
                created_at="2024-06-04T13:05:00Z",
            ),
            HydroponicSystemFactory(
                name="system3",
                plant_count=9,
                owner=self.users[0],
                created_at="2024-06-04T13:07:00Z",
            ),
            HydroponicSystemFactory(
                name="system4",
                plant_count=3,
                owner=self.users[1],
                created_at="2024-06-04T13:01:00Z",
            ),
            HydroponicSystemFactory(
                name="system5",
                plant_count=5,
                owner=self.users[1],
                created_at="2024-06-04T13:03:00Z",
            ),
        ]

        SensorReadingFactory.create_batch(15, hydroponic_system=self.systems[0])

    def test_hydroponic_system_retrieve(self):
        def request_and_check_status(system, user=None, status_code=status.HTTP_200_OK):
            response = self.request(
                "get", "hydroponic-system-detail", {"pk": system.pk}, user=user
            )
            self.assertEqual(response.status_code, status_code)
            if status_code == status.HTTP_200_OK:
                return response.json()
            return response

        request_and_check_status(
            self.systems[0], status_code=status.HTTP_401_UNAUTHORIZED
        )

        request_and_check_status(
            self.systems[0], self.users[1], status.HTTP_404_NOT_FOUND
        )

        data = request_and_check_status(self.systems[0], self.users[0])
        self.assertEqual(data["id"], self.systems[0].id)
        self.assertIn("recent_sensor_readings", data)
        self.assertEqual(len(data["recent_sensor_readings"]), 10)

        data = request_and_check_status(self.systems[1], self.users[0])
        self.assertEqual(data["id"], self.systems[1].id)
        self.assertIn("recent_sensor_readings", data)
        self.assertEqual(len(data["recent_sensor_readings"]), 0)

    def test_hydroponic_system_list(self):
        def request_and_check_status(
            query_params=None, user=None, status_code=status.HTTP_200_OK
        ):
            response = self.request(
                "get", "hydroponic-system-list", query_params=query_params, user=user
            )
            self.assertEqual(response.status_code, status_code)
            if status_code == status.HTTP_200_OK:
                return response.json()["results"]
            return response

        request_and_check_status(status_code=status.HTTP_401_UNAUTHORIZED)

        results = request_and_check_status(user=self.users[0])
        self.assertCountEqual(
            [system["id"] for system in results],
            [system.id for system in self.systems[:3]],
        )

        results = request_and_check_status(user=self.users[1])
        self.assertCountEqual(
            [system["id"] for system in results],
            [system.id for system in self.systems[3:]],
        )

        results = request_and_check_status({"name": "system2"}, self.users[0])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.systems[1].id)

        results = request_and_check_status({"name": "system2"}, self.users[1])
        self.assertEqual(len(results), 0)

        results = request_and_check_status({"plant_count": 3}, self.users[0])
        self.assertEqual(len(results), 2)

        results = request_and_check_status({"plant_count": 3}, self.users[1])
        self.assertEqual(len(results), 1)

        results = request_and_check_status({"plant_count__gte": 3}, self.users[0])
        self.assertEqual(len(results), 3)

        results = request_and_check_status({"plant_count__gte": 4}, self.users[0])
        self.assertEqual(len(results), 1)

        results = request_and_check_status({"plant_count__lte": 3}, self.users[0])
        self.assertEqual(len(results), 2)

        results = request_and_check_status({"plant_count__lte": 2}, self.users[0])
        self.assertEqual(len(results), 0)

        query_params = {"plant_count__gte": 2, "plant_count__lte": 9}
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 3)

        request_and_check_status(
            {"plant_count": "invalid"}, self.users[0], status.HTTP_400_BAD_REQUEST
        )

        query_params = {"created_at": "2024-06-04T13:00:00Z"}
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 1)

        query_params = {"created_at__gte": "2024-06-04T13:00:00Z"}
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 3)

        query_params = {"created_at__lte": "2024-06-04T13:06:00Z"}
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 2)

        query_params = {
            "created_at__gte": "2024-06-04T13:05:00Z",
            "created_at__lte": "2024-06-04T13:08:00Z",
        }
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 2)

        request_and_check_status(
            {"created_at": "invalid"}, self.users[0], status.HTTP_400_BAD_REQUEST
        )

        results = request_and_check_status({"ordering": "name"}, self.users[0])
        self.assertListEqual(
            [system["id"] for system in results],
            [system.id for system in self.systems[:3]],
        )

        results = request_and_check_status({"ordering": "plant_count"}, self.users[0])
        self.assertListEqual([system["plant_count"] for system in results], [3, 3, 9])

        results = request_and_check_status({"ordering": "-plant_count"}, self.users[0])
        self.assertListEqual([system["plant_count"] for system in results], [9, 3, 3])

        results = request_and_check_status({"ordering": "created_at"}, self.users[0])
        self.assertListEqual(
            [system["id"] for system in results],
            [system.id for system in self.systems[:3]],
        )

    def test_hydroponic_system_create(self):
        def request_and_check_status(
            data=None, user=None, status_code=status.HTTP_201_CREATED
        ):
            response = self.request(
                "post", "hydroponic-system-list", data=data, user=user
            )
            self.assertEqual(response.status_code, status_code)
            return response

        request_and_check_status(status_code=status.HTTP_401_UNAUTHORIZED)

        data = {
            "name": "some name",
            "description": "some description",
            "plant_count": 5,
        }
        self.assertEqual(self.users[0].hydroponic_systems.count(), 3)
        request_and_check_status(data, self.users[0])
        self.assertEqual(self.users[0].hydroponic_systems.count(), 4)

        data["plant_count"] = -1
        request_and_check_status(data, self.users[0], status.HTTP_400_BAD_REQUEST)

    def test_hydroponic_system_update(self):
        def request_and_check_status(
            system, method, data=None, user=None, status_code=status.HTTP_200_OK
        ):
            response = self.request(
                method,
                "hydroponic-system-detail",
                {"pk": system.pk},
                data=data,
                user=user,
            )
            self.assertEqual(response.status_code, status_code)
            return response

        system = self.systems[0]

        request_and_check_status(
            system, "put", status_code=status.HTTP_401_UNAUTHORIZED
        )
        request_and_check_status(
            system,
            "put",
            user=self.users[1],
            status_code=status.HTTP_404_NOT_FOUND,
        )

        request_and_check_status(
            system, "patch", status_code=status.HTTP_401_UNAUTHORIZED
        )
        request_and_check_status(
            system,
            "patch",
            user=self.users[1],
            status_code=status.HTTP_404_NOT_FOUND,
        )

        data = {
            "name": system.name,
            "description": system.description,
            "plant_count": 5,
        }
        request_and_check_status(system, "put", data, self.users[0])
        system.refresh_from_db()
        self.assertEqual(system.plant_count, 5)

        data = {"plant_count": 7}
        request_and_check_status(system, "patch", data, self.users[0])
        system.refresh_from_db()
        self.assertEqual(system.plant_count, 7)

    def test_hydroponic_system_delete(self):
        def request_and_check_status(
            system, user=None, status_code=status.HTTP_204_NO_CONTENT
        ):
            response = self.request(
                "delete", "hydroponic-system-detail", {"pk": system.pk}, user=user
            )
            self.assertEqual(response.status_code, status_code)
            return response

        system = self.systems[0]

        request_and_check_status(system, status_code=status.HTTP_401_UNAUTHORIZED)
        request_and_check_status(
            system,
            self.users[1],
            status_code=status.HTTP_404_NOT_FOUND,
        )

        self.assertEqual(self.users[0].hydroponic_systems.count(), 3)
        request_and_check_status(system, self.users[0])
        self.assertEqual(self.users[0].hydroponic_systems.count(), 2)


class TestSensorReadings(APITestCase):
    def setUp(self):
        self.users = UserFactory.create_batch(2)
        self.systems = [
            HydroponicSystemFactory(owner=self.users[0]),
            HydroponicSystemFactory(owner=self.users[0]),
            HydroponicSystemFactory(owner=self.users[1]),
        ]
        self.readings = [
            SensorReadingFactory(
                ph=2,
                water_temp=20,
                tds=300,
                hydroponic_system=self.systems[0],
                created_at="2024-06-04T13:00:00Z",
            ),
            SensorReadingFactory(
                ph=8,
                water_temp=25,
                tds=400,
                hydroponic_system=self.systems[0],
                created_at="2024-06-04T13:05:00Z",
            ),
            SensorReadingFactory(
                ph=10,
                water_temp=18,
                tds=100,
                hydroponic_system=self.systems[1],
                created_at="2024-06-04T13:07:00Z",
            ),
            SensorReadingFactory(
                ph=4,
                water_temp=20,
                tds=300,
                hydroponic_system=self.systems[2],
                created_at="2024-06-04T13:01:00Z",
            ),
            SensorReadingFactory(
                ph=5,
                water_temp=20,
                tds=300,
                hydroponic_system=self.systems[2],
                created_at="2024-06-04T13:03:00Z",
            ),
        ]

    def test_sensor_reading_list(self):
        def request_and_check_status(
            query_params=None, user=None, status_code=status.HTTP_200_OK
        ):
            response = self.request(
                "get", "sensor-reading-list", query_params=query_params, user=user
            )
            self.assertEqual(response.status_code, status_code)
            if status_code == status.HTTP_200_OK:
                return response.json()["results"]
            return response

        request_and_check_status(status_code=status.HTTP_401_UNAUTHORIZED)

        results = request_and_check_status(user=self.users[0])
        self.assertCountEqual(
            [reading["id"] for reading in results],
            [reading.id for reading in self.readings[:3]],
        )

        results = request_and_check_status(user=self.users[1])
        self.assertCountEqual(
            [reading["id"] for reading in results],
            [reading.id for reading in self.readings[3:]],
        )

        query_params = {"hydroponic_system": self.systems[0].id}
        results = request_and_check_status(query_params, self.users[0])
        self.assertCountEqual(
            [reading["id"] for reading in results],
            [reading.id for reading in self.readings[:2]],
        )

        query_params = {"hydroponic_system": self.systems[2].id}
        results = request_and_check_status(query_params, self.users[1])
        self.assertCountEqual(
            [reading["id"] for reading in results],
            [reading.id for reading in self.readings[3:]],
        )

        query_params = {"hydroponic_system": self.systems[0].id}
        results = request_and_check_status(query_params, self.users[1])
        self.assertEqual(len(results), 0)

        query_params = {"hydroponic_system": self.systems[2].id}
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 0)

        results = request_and_check_status({"ph": 2}, self.users[0])
        self.assertEqual(len(results), 1)

        results = request_and_check_status({"ph__gte": 3}, self.users[0])
        self.assertEqual(len(results), 2)

        results = request_and_check_status({"ph__lte": 3}, self.users[0])
        self.assertEqual(len(results), 1)

        results = request_and_check_status({"ph__lte": 1}, self.users[0])
        self.assertEqual(len(results), 0)

        query_params = {"ph__gte": 2, "ph__lte": 10}
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 3)

        request_and_check_status(
            {"ph": "invalid"}, self.users[0], status.HTTP_400_BAD_REQUEST
        )

        results = request_and_check_status({"water_temp": 25}, self.users[0])
        self.assertEqual(len(results), 1)

        results = request_and_check_status({"water_temp": 20}, self.users[1])
        self.assertEqual(len(results), 2)

        results = request_and_check_status({"water_temp__gte": 19}, self.users[0])
        self.assertEqual(len(results), 2)

        results = request_and_check_status({"water_temp__lte": 19}, self.users[0])
        self.assertEqual(len(results), 1)

        results = request_and_check_status({"water_temp__lte": 0}, self.users[0])
        self.assertEqual(len(results), 0)

        query_params = {"water_temp__gte": 18, "water_temp__lte": 25}
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 3)

        request_and_check_status(
            {"water_temp": "invalid"}, self.users[0], status.HTTP_400_BAD_REQUEST
        )

        results = request_and_check_status({"tds": 400}, self.users[0])
        self.assertEqual(len(results), 1)

        results = request_and_check_status({"tds": 300}, self.users[1])
        self.assertEqual(len(results), 2)

        results = request_and_check_status({"tds__gte": 200}, self.users[0])
        self.assertEqual(len(results), 2)

        results = request_and_check_status({"tds__lte": 200}, self.users[0])
        self.assertEqual(len(results), 1)

        results = request_and_check_status({"tds__lte": 200}, self.users[1])
        self.assertEqual(len(results), 0)

        query_params = {"tds__gte": 100, "tds__lte": 400}
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 3)

        request_and_check_status(
            {"tds": "invalid"}, self.users[0], status.HTTP_400_BAD_REQUEST
        )

        query_params = {"created_at": "2024-06-04T13:00:00Z"}
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 1)

        query_params = {"created_at__gte": "2024-06-04T13:00:00Z"}
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 3)

        query_params = {"created_at__lte": "2024-06-04T13:06:00Z"}
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 2)

        query_params = {
            "created_at__gte": "2024-06-04T13:05:00Z",
            "created_at__lte": "2024-06-04T13:08:00Z",
        }
        results = request_and_check_status(query_params, self.users[0])
        self.assertEqual(len(results), 2)

        request_and_check_status(
            {"created_at": "invalid"}, self.users[0], status.HTTP_400_BAD_REQUEST
        )

        results = request_and_check_status({"ordering": "name"}, self.users[0])
        self.assertListEqual(
            [reading["id"] for reading in results],
            [reading.id for reading in self.readings[:3]],
        )

        results = request_and_check_status({"ordering": "ph"}, self.users[0])
        self.assertListEqual(
            [reading["ph"] for reading in results], ["2.00", "8.00", "10.00"]
        )

        results = request_and_check_status({"ordering": "-ph"}, self.users[0])
        self.assertListEqual(
            [reading["ph"] for reading in results], ["10.00", "8.00", "2.00"]
        )

        results = request_and_check_status({"ordering": "water_temp"}, self.users[0])
        self.assertListEqual(
            [reading["water_temp"] for reading in results], ["18.00", "20.00", "25.00"]
        )

        results = request_and_check_status({"ordering": "water_temp"}, self.users[1])
        self.assertListEqual(
            [reading["water_temp"] for reading in results], ["20.00", "20.00"]
        )

        results = request_and_check_status({"ordering": "tds"}, self.users[0])
        self.assertListEqual(
            [reading["tds"] for reading in results], ["100.00", "300.00", "400.00"]
        )

        results = request_and_check_status({"ordering": "tds"}, self.users[1])
        self.assertListEqual(
            [reading["tds"] for reading in results], ["300.00", "300.00"]
        )

        results = request_and_check_status({"ordering": "created_at"}, self.users[0])
        self.assertListEqual(
            [reading["id"] for reading in results],
            [reading.id for reading in self.readings[:3]],
        )

    def test_sensor_reading_create(self):
        def request_and_check_status(
            data=None, user=None, status_code=status.HTTP_201_CREATED, text=""
        ):
            response = self.request("post", "sensor-reading-list", data=data, user=user)
            self.assertContains(response, text, status_code=status_code)
            return response

        request_and_check_status(status_code=status.HTTP_401_UNAUTHORIZED)

        system = self.systems[0]
        data = {
            "ph": "3.7",
            "water_temp": "20.1",
            "tds": "400.5",
            "hydroponic_system": system.id,
        }

        request_and_check_status(
            data,
            self.users[1],
            status_code=status.HTTP_403_FORBIDDEN,
            text="You are not the owner of the hydroponic system.",
        )

        self.assertEqual(system.sensor_readings.count(), 2)
        request_and_check_status(data, self.users[0])
        self.assertEqual(system.sensor_readings.count(), 3)

        data["ph"] = "invalid"
        request_and_check_status(data, self.users[0], status.HTTP_400_BAD_REQUEST)

        data["hydroponic_system"] = 999
        request_and_check_status(data, self.users[0], status.HTTP_400_BAD_REQUEST)

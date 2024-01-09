from conftest import BaseTest
from http import HTTPStatus

correct_get_categories_response = {
    "categories": [
        {
            "alternateName": None,
            "baseRegistrationFee": 7,
            "categoryId": "A",
            "color": "blue",
            "currentFee": 7,
            "entryCount": 130,
            "lateRegistrationFee": 1,
            "maxPlayers": 72,
            "maxPoints": 900,
            "minPoints": 0,
            "overbookingPercentage": 20,
            "rewardFirst": 70,
            "rewardQuarter": None,
            "rewardSecond": 35,
            "rewardSemi": 20,
            "startTime": "2024-01-06T09:00:00",
            "womenOnly": False,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 7,
            "categoryId": "B",
            "color": "blue",
            "currentFee": 7,
            "entryCount": 46,
            "lateRegistrationFee": 1,
            "maxPlayers": 72,
            "maxPoints": 1500,
            "minPoints": 0,
            "overbookingPercentage": 15,
            "rewardFirst": 140,
            "rewardQuarter": None,
            "rewardSecond": 70,
            "rewardSemi": 35,
            "startTime": "2024-01-06T10:15:00",
            "womenOnly": False,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 10,
            "categoryId": "C",
            "color": "#00FF00",
            "currentFee": 10,
            "entryCount": 18,
            "lateRegistrationFee": 2,
            "maxPlayers": 36,
            "maxPoints": 4000,
            "minPoints": 1300,
            "overbookingPercentage": 10,
            "rewardFirst": 300,
            "rewardQuarter": None,
            "rewardSecond": 150,
            "rewardSemi": 75,
            "startTime": "2024-01-06T11:30:00",
            "womenOnly": True,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 7,
            "categoryId": "D",
            "color": "#00FF00",
            "currentFee": 7,
            "entryCount": 41,
            "lateRegistrationFee": 1,
            "maxPlayers": 72,
            "maxPoints": 1100,
            "minPoints": 0,
            "overbookingPercentage": 20,
            "rewardFirst": 100,
            "rewardQuarter": None,
            "rewardSecond": 50,
            "rewardSemi": 25,
            "startTime": "2024-01-06T12:45:00",
            "womenOnly": False,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 10,
            "categoryId": "E",
            "color": "#FF0000",
            "currentFee": 10,
            "entryCount": 49,
            "lateRegistrationFee": 2,
            "maxPlayers": 72,
            "maxPoints": 4000,
            "minPoints": 1500,
            "overbookingPercentage": 0,
            "rewardFirst": 300,
            "rewardQuarter": None,
            "rewardSecond": 150,
            "rewardSemi": 75,
            "startTime": "2024-01-06T14:00:00",
            "womenOnly": False,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 7,
            "categoryId": "F",
            "color": "#FF0000",
            "currentFee": 7,
            "entryCount": 36,
            "lateRegistrationFee": 1,
            "maxPlayers": 72,
            "maxPoints": 1300,
            "minPoints": 0,
            "overbookingPercentage": 10,
            "rewardFirst": 120,
            "rewardQuarter": None,
            "rewardSecond": 60,
            "rewardSemi": 30,
            "startTime": "2024-01-06T15:00:00",
            "womenOnly": False,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 7,
            "categoryId": "G",
            "color": None,
            "currentFee": 7,
            "entryCount": 48,
            "lateRegistrationFee": 1,
            "maxPlayers": 72,
            "maxPoints": 1900,
            "minPoints": 0,
            "overbookingPercentage": 15,
            "rewardFirst": 180,
            "rewardQuarter": None,
            "rewardSecond": 90,
            "rewardSemi": 45,
            "startTime": "2024-01-06T16:00:00",
            "womenOnly": False,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 7,
            "categoryId": "1",
            "color": "#0000FF",
            "currentFee": 7,
            "entryCount": 148,
            "lateRegistrationFee": 1,
            "maxPlayers": 72,
            "maxPoints": 1700,
            "minPoints": 0,
            "overbookingPercentage": 20,
            "rewardFirst": 170,
            "rewardQuarter": None,
            "rewardSecond": 85,
            "rewardSemi": 45,
            "startTime": "2024-01-07T09:00:00",
            "womenOnly": False,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 7,
            "categoryId": "2",
            "color": "#0000FF",
            "currentFee": 7,
            "entryCount": 30,
            "lateRegistrationFee": 1,
            "maxPlayers": 72,
            "maxPoints": 1400,
            "minPoints": 0,
            "overbookingPercentage": 0,
            "rewardFirst": 130,
            "rewardQuarter": None,
            "rewardSecond": 65,
            "rewardSemi": 35,
            "startTime": "2024-01-07T10:15:00",
            "womenOnly": False,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 7,
            "categoryId": "3",
            "color": "#FFFF00",
            "currentFee": 7,
            "entryCount": 33,
            "lateRegistrationFee": 1,
            "maxPlayers": 72,
            "maxPoints": 2100,
            "minPoints": 0,
            "overbookingPercentage": 30,
            "rewardFirst": 200,
            "rewardQuarter": None,
            "rewardSecond": 100,
            "rewardSemi": 50,
            "startTime": "2024-01-07T11:30:00",
            "womenOnly": False,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 7,
            "categoryId": "4",
            "color": "#FFFF00",
            "currentFee": 7,
            "entryCount": 13,
            "lateRegistrationFee": 1,
            "maxPlayers": 72,
            "maxPoints": 1000,
            "minPoints": 0,
            "overbookingPercentage": 20,
            "rewardFirst": 90,
            "rewardQuarter": None,
            "rewardSecond": 45,
            "rewardSemi": 25,
            "startTime": "2024-01-07T12:45:00",
            "womenOnly": False,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 7,
            "categoryId": "5",
            "color": None,
            "currentFee": 7,
            "entryCount": 5,
            "lateRegistrationFee": 1,
            "maxPlayers": 36,
            "maxPoints": 1600,
            "minPoints": 0,
            "overbookingPercentage": 20,
            "rewardFirst": 150,
            "rewardQuarter": None,
            "rewardSecond": 75,
            "rewardSemi": 40,
            "startTime": "2024-01-07T14:00:00",
            "womenOnly": True,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 7,
            "categoryId": "6",
            "color": "#00FFFF",
            "currentFee": 7,
            "entryCount": 15,
            "lateRegistrationFee": 1,
            "maxPlayers": 72,
            "maxPoints": 1200,
            "minPoints": 0,
            "overbookingPercentage": 15,
            "rewardFirst": 110,
            "rewardQuarter": None,
            "rewardSecond": 55,
            "rewardSemi": 30,
            "startTime": "2024-01-07T15:00:00",
            "womenOnly": False,
        },
        {
            "alternateName": None,
            "baseRegistrationFee": 7,
            "categoryId": "7",
            "color": "#00FFFF",
            "currentFee": 7,
            "entryCount": 10,
            "lateRegistrationFee": 1,
            "maxPlayers": 72,
            "maxPoints": 800,
            "minPoints": 0,
            "overbookingPercentage": 10,
            "rewardFirst": 60,
            "rewardQuarter": None,
            "rewardSecond": 30,
            "rewardSemi": 15,
            "startTime": "2024-01-07T16:00:00",
            "womenOnly": False,
        },
    ],
}


class TestAPIGetCategories(BaseTest):
    def test_get(self, client, reset_db, populate):
        r = client.get("/api/public/categories")
        assert r.status_code == HTTPStatus.OK, r.json
        assert r.json == correct_get_categories_response, r.json

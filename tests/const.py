MOCK_CLIENT_ID = "mock-client-id"
MOCK_CLIENT_SECRET = "mock-client-secret"
MOCK_AUTH_CODE = "mock-auth-code"
MOCK_REDIRECT_URI = "http://mock-redirect-uri"
MOCK_ACCESS_TOKEN = "mock-access-token"

MOCK_AUTH_RESPONSE = {
    "access_token": MOCK_ACCESS_TOKEN,
    "token_type": "Bearer",
    "expires_in": 3600,
}
MOCK_USER_RESPONSE = {
    "email": "user@email.com",
    "name": "John Doe",
    "id": "5ed95be16e8444001bc97a1f",
}

MOCK_TRIPS_RESPONSE_IMEI = [
    {
        "transactionId": "353762078072777-123-1590670937000",
        "hardBrakingCount": 0,
        "hardAccelerationCount": 2,
        "distance": 3.4,
        "gps": "qiwaHzkmhVCuBk@pBkAfC~CuB??IXCHUq@???_AkFlA?W????lFuAEU??c@CMp@DbA??CjAQ`@u@X??_A_@c@i@Kk@??",
        "startTime": "2020-05-28 13:07:07.000Z",
        "endTime": "2020-05-28 13:17:07.000Z",
        "startOdometer": 12011,
        "endOdometer": 12014,
        "averageSpeed": 12,
        "maxSpeed": 21,
        "fuelConsumed": 0.2,
        "timeZone": "-0500",
    }
]
MOCK_VEHICLES_RESPONSE = [
    {
        "model": {"make": "TOYOTA", "name": "PRIUS", "year": 2007},
        "standardEngine": "1.5L I4",
        "vin": "toyota-prius-2007-vin",
        "imei": "toyota-prius-2007-imei",
        "stats": {
            "localTimeZone": "-0500",
            "lastUpdated": "2022-11-23T01:53:57.000Z",
            "odometer": 123456,
            "location": {
                "lat": 40.748440,
                "lon": -73.985664,
                "heading": 120,
                "address": "20 W 34th St., New York, NY 10001, USA",
            },
            "isRunning": False,
            "speed": 0,
            "mil": {"lastUpdated": "2022-11-23T01:38:55.000Z"},
            "battery": {"status": "normal", "lastUpdated": "2022-11-23T01:37:41.000Z"},
        },
    }
]
MOCK_VEHICLES_IMEI_RESPONSE = [
    {
        "model": {"make": "TOYOTA", "name": "PRIUS", "year": 2007},
        "standardEngine": "1.5L I4",
        "vin": "toyota-prius-2007-vin",
        "imei": "toyota-prius-2007-imei",
        "nickName": "My Gmc",
        "stats": {
            "localTimezone": "-0600",
            "lastUpdated": "2020-04-28 22:13:17.000Z",
            "location": "123 Main St, Dallas, Texas 75251, United States",
            "fuelLevel": 27.3,
            "isRunning": False,
            "speed": 0,
            "mil": {"milOn": False, "lastUpdated": "2020-01-01 12:00:00:000Z"},
            "battery": {"status": "normal", "lastUpdated": "2020-04-25 12:00:00:000Z"},
        },
    }
]

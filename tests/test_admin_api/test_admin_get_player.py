from tests.conftest import BaseTest, before_cutoff, after_cutoff
import flaskr.api.api_errors as ae

from http import HTTPStatus

import pytest
from freezegun import freeze_time


origin = "admin_get_player"

correct_db_before = (
    9943272,
    before_cutoff,
    {
        "bibNo": None,
        "club": "NANTES ST MEDARD DOULON",
        "email": "player24@emailhost.com",
        "firstName": "Player24",
        "gender": "M",
        "lastName": "AERGTHVI",
        "licenceNo": 9943272,
        "nbPoints": 1583,
        "phone": "+33806956124",
        "registeredEntries": {
            "E": {
                "alternateName": None,
                "entryFee": 10,
                "licenceNo": 9943272,
                "markedAsPaid": False,
                "markedAsPresent": None,
                "rank": 44,
                "registrationTime": "2023-12-23T16:27:46.012875",
                "startTime": "2024-01-06T14:00:00",
            },
        },
    },
)

correct_db_after = (
    9943272,
    after_cutoff,
    {
        "bibNo": None,
        "club": "NANTES ST MEDARD DOULON",
        "email": "player24@emailhost.com",
        "firstName": "Player24",
        "gender": "M",
        "lastName": "AERGTHVI",
        "leftToPay": 0,
        "licenceNo": 9943272,
        "nbPoints": 1583,
        "paymentStatus": {
            "totalActualPaid": 0,
            "totalPaid": 0,
            "totalPresent": 0,
            "totalRegistered": 10,
        },
        "phone": "+33806956124",
        "registeredEntries": {
            "E": {
                "alternateName": None,
                "entryFee": 10,
                "licenceNo": 9943272,
                "markedAsPaid": False,
                "markedAsPresent": None,
                "rank": 44,
                "registrationTime": "2023-12-23T16:27:46.012875",
                "startTime": "2024-01-06T14:00:00",
            },
        },
    },
)

correct_fftt_before = (
    7513006,
    before_cutoff,
    {
        "bibNo": None,
        "club": "KREMLIN BICETRE US",
        "email": None,
        "firstName": "Celine",
        "gender": "F",
        "lastName": "LAY",
        "licenceNo": 7513006,
        "nbPoints": 1232,
        "paymentStatus": {
            "totalActualPaid": 0,
            "totalPaid": 0,
            "totalPresent": 0,
            "totalRegistered": 0,
        },
        "phone": None,
        "registeredEntries": {},
    },
)

correct_licences = [
    correct_db_before,
    correct_db_after,
    correct_fftt_before,
]

incorrect_licence = (
    1234567,
    False,
    ae.PlayerNotFoundError(
        origin=origin,
        licence_no=1234567,
    ),
)

incorrect_licence_db_only = (
    7513006,
    True,
    ae.PlayerNotFoundError(
        origin="admin_get_player_db_only",
        licence_no=7513006,
    ),
)

incorrect_licences = [incorrect_licence, incorrect_licence_db_only]


class TestAPIAdminGetPlayer(BaseTest):
    @pytest.mark.parametrize("licence_no,now,response", correct_licences)
    def test_get_player_correct(
        self,
        client,
        reset_db,
        populate,
        licence_no,
        now: str,
        response,
    ):
        with freeze_time(now):
            r = client.get(f"/api/admin/players/{licence_no}")
            assert r.status_code == HTTPStatus.OK, r.json
            assert r.json == response, r.json

    @pytest.mark.parametrize("licence_no,db_only,error", incorrect_licences)
    def test_get_player_incorrect(
        self,
        client,
        reset_db,
        populate,
        licence_no,
        db_only,
        error,
    ):
        r = client.get(
            f"/api/admin/players/{licence_no}?db_only={'true' if db_only else 'false'}",
        )
        assert r.status_code == error.status_code
        assert r.json == error.to_dict(), r.json
from tests.conftest import BaseTest, before_cutoff, after_cutoff
from http import HTTPStatus
import pytest

import flaskr.api.api_errors as ae
from freezegun import freeze_time


overall_correct_licence = 722370
overall_incorrect_licence = 555555

origin = "api_public_register_entries"

correct_registration = (
    4526124,
    before_cutoff,
    {"categoryIds": ["1"]},
    {
        "1": {
            "alternateName": None,
            "entryFee": 7,
            "licenceNo": 4526124,
            "markedAsPaid": False,
            "markedAsPresent": None,
            "rank": 0,
            "registrationTime": "2023-01-01T00:00:00",
            "startTime": "2024-01-07T09:00:00",
        },
        "B": {
            "alternateName": "< 1500",
            "entryFee": 7,
            "licenceNo": 4526124,
            "markedAsPaid": True,
            "markedAsPresent": True,
            "rank": 43,
            "registrationTime": "2023-11-17T18:01:20",
            "startTime": "2024-01-06T10:15:00",
        },
        "F": {
            "alternateName": "Pas open féminin",
            "entryFee": 7,
            "licenceNo": 4526124,
            "markedAsPaid": True,
            "markedAsPresent": True,
            "rank": 30,
            "registrationTime": "2023-11-25T21:56:50",
            "startTime": "2024-01-06T15:00:00",
        },
    },
)

correct_registration_with_duplicates = (
    4526124,
    before_cutoff,
    {
        "categoryIds": ["1", "B", "F"],
    },
    {
        "1": {
            "alternateName": None,
            "entryFee": 7,
            "licenceNo": 4526124,
            "markedAsPaid": False,
            "markedAsPresent": None,
            "rank": 0,
            "registrationTime": "2023-01-01T00:00:00",
            "startTime": "2024-01-07T09:00:00",
        },
        "B": {
            "alternateName": "< 1500",
            "entryFee": 7,
            "licenceNo": 4526124,
            "markedAsPaid": True,
            "markedAsPresent": True,
            "rank": 43,
            "registrationTime": "2023-11-17T18:01:20",
            "startTime": "2024-01-06T10:15:00",
        },
        "F": {
            "alternateName": "Pas open féminin",
            "entryFee": 7,
            "licenceNo": 4526124,
            "markedAsPaid": True,
            "markedAsPresent": True,
            "rank": 30,
            "registrationTime": "2023-11-25T21:56:50",
            "startTime": "2024-01-06T15:00:00",
        },
    },
)

correct_register_entries = [
    correct_registration,
    correct_registration_with_duplicates,
]

incorrect_registration_color_violation = (
    7886249,
    before_cutoff,
    {"categoryIds": ["1"]},
    ae.InvalidDataError(
        origin=origin,
        error_message=ae.COLOR_VIOLATION_MESSAGE,
    ),
)

incorrect_registration_gender_points_violation = (
    4526124,
    before_cutoff,
    {
        "categoryIds": ["A"],
    },
    ae.InvalidDataError(
        origin=origin,
        error_message=ae.GENDER_POINTS_VIOLATION_MESSAGE,
        payload={"categoryIds": ["A"]},
    ),
)

incorrect_registration_nonexisting_player = (
    overall_incorrect_licence,
    before_cutoff,
    {"categoryIds": ["A"]},
    ae.PlayerNotFoundError(
        origin=origin,
        licence_no=overall_incorrect_licence,
    ),
)

incorrect_registrations_missing_categoryids_json_fields = (
    4526124,
    before_cutoff,
    {},
    ae.InvalidDataError(
        origin=origin,
        error_message=ae.REGISTRATION_FORMAT_MESSAGE,
        payload={"categoryIds": ["Missing data for required field."]},
    ),
)

incorrect_registration_empty_categories = (
    4526124,
    before_cutoff,
    {"categoryIds": []},
    ae.InvalidDataError(
        origin=origin,
        error_message=ae.REGISTRATION_MISSING_IDS_MESSAGE,
    ),
)

incorrect_registration_nonexisting_categories = (
    4526124,
    before_cutoff,
    {
        "categoryIds": ["A", "a"],
    },
    ae.InvalidDataError(
        origin=origin,
        error_message=ae.INVALID_CATEGORY_ID_MESSAGES["registration"],
        payload={"categoryIds": ["a"]},
    ),
)

incorrect_registration_after_cutoff = (
    4526124,
    after_cutoff,
    {"categoryIds": ["1"]},
    ae.RegistrationCutoffError(
        origin=origin,
        error_message=ae.REGISTRATION_MESSAGES["ended"],
    ),
)

incorrect_register_entries = [
    incorrect_registration_color_violation,
    incorrect_registration_gender_points_violation,
    incorrect_registration_nonexisting_player,
    incorrect_registrations_missing_categoryids_json_fields,
    incorrect_registration_empty_categories,
    incorrect_registration_nonexisting_categories,
    incorrect_registration_after_cutoff,
]


class TestRegisterEntries(BaseTest):
    @pytest.mark.parametrize(
        "licence_no,now,payload,response",
        correct_register_entries,
    )
    def test_correct_register_entries(
        self,
        client,
        reset_db,
        populate,
        licence_no,
        now: str,
        payload,
        response,
    ):
        with freeze_time(now):
            r = client.post(f"/api/public/entries/{licence_no}", json=payload)
            assert r.status_code == HTTPStatus.CREATED, r.json
            assert "registeredEntries" in r.json, r.json
            assert r.json["registeredEntries"] == response, r.json

    @pytest.mark.parametrize("licence_no,now,payload,error", incorrect_register_entries)
    def test_incorrect_register_entries(
        self,
        client,
        reset_db,
        populate,
        licence_no,
        now: str,
        payload,
        error,
    ):
        with freeze_time(now):
            r = client.post(f"/api/public/entries/{licence_no}", json=payload)
            assert r.status_code == error.status_code, r.json
            assert r.json == error.to_dict(), r.json

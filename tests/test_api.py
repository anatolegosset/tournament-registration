from conftest import BaseTest
from http import HTTPStatus

from tests.testing_data import (
    correct_categories,
    correct_categories_response,
    correct_delete_entries_all,
    correct_delete_entries_all_response,
    correct_delete_entries_partial,
    correct_delete_entries_partial_response,
    correct_delete_player_by_licence,
    correct_delete_player_by_name,
    correct_get_categories_response,
    correct_get_player_existing,
    correct_get_player_existing_response,
    correct_get_player_nonexisting,
    correct_get_player_nonexisting_response,
    correct_payment_all_recap_positive,
    correct_payment_all_recap_positive_response,
    correct_payment_pay_all,
    correct_payment_pay_all_by_name,
    correct_payment_pay_all_by_name_response,
    correct_payment_pay_all_response,
    correct_payment_pay_partial,
    correct_payment_pay_partial_response,
    correct_payment_previously_paid,
    correct_payment_previously_paid_response,
    correct_player,
    correct_player_response,
    correct_registration,
    correct_registration_response,
    correct_registration_with_duplicates,
    correct_registration_with_duplicates_response,
    incorrect_categories_duplicate,
    incorrect_categories_missing_badly_formatted_data,
    incorrect_categories_missing_categories_field,
    incorrect_delete_entries_missing_categories_json_field,
    incorrect_delete_entries_missing_player_identifier_json_field,
    incorrect_delete_entries_nonexisting_categories,
    incorrect_delete_entries_nonexisting_entries,
    incorrect_delete_entries_nonexisting_player,
    incorrect_delete_player_missing_json_field,
    incorrect_delete_player_nonexisting_player_by_licence,
    incorrect_delete_player_nonexisting_player_by_name,
    incorrect_get_player_missing_licence_no_json_field,
    incorrect_payment_duplicate_payment,
    incorrect_payment_missing_categories_json_field,
    incorrect_payment_missing_player_identifier_json_field,
    incorrect_payment_without_registration,
    incorrect_player_duplicate,
    incorrect_player_missing_badly_formatted_data,
    incorrect_player_missing_player_json_field,
    incorrect_registration_color_violation,
    incorrect_registration_empty_categories,
    incorrect_registration_gender_points_violation,
    incorrect_registration_missing_player,
    incorrect_registration_nonexisting_categories,
    incorrect_registrations_missing_json_fields,
    correct_payment_default_actual,
    correct_payment_default_actual_response,
    correct_payment_nondefault_actual,
    correct_payment_nondefault_actual_response,
    correct_payment_nonzero_diff,
    correct_payment_nonzero_diff_response,
    correct_payment_nonzero_diff_nondefault_actual,
    correct_payment_nonzero_diff_nondefault_actual_response,
)


class TestAPISetCategories(BaseTest):
    def test_correct(self, client, reset_db):
        r = client.post("/api/categories", json=correct_categories)
        assert r.status_code == HTTPStatus.CREATED, r.json
        assert "categories" in r.json
        assert r.json["categories"] == correct_categories_response

    def test_incorrect_missing_categories_json_field(self, client, reset_db):
        r = client.post(
            "/api/categories",
            json=incorrect_categories_missing_categories_field,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "json was missing 'categories' field. Categories were not set"
            in r.json["error"]
        ), r.json

    def test_incorrect_missing_badly_formatted_data(self, client, reset_db):
        r = client.post(
            "/api/categories",
            json=incorrect_categories_missing_badly_formatted_data,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "Some category data was missing or wrongly formatted. Categories "
            "were not set." in r.json["error"]
        ), r.json

    def test_incorrect_duplicate(self, client, reset_db):
        r = client.post("/api/categories", json=incorrect_categories_duplicate)
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "At least two categories have the same name. Categories were not set."
            in r.json["error"]
        ), r.json


class TestAPIMakePayment(BaseTest):
    def test_correct_pay_all(self, client, reset_db, populate):
        r = client.put("/api/pay", json=correct_payment_pay_all)
        assert r.status_code == HTTPStatus.OK, r.json
        assert r.json == correct_payment_pay_all_response, r.json

    def test_correct_pay_all_by_name(self, client, reset_db, populate):
        r = client.put("/api/pay", json=correct_payment_pay_all_by_name)
        assert r.status_code == HTTPStatus.OK, r.json
        assert r.json == correct_payment_pay_all_by_name_response, r.json

    def test_correct_pay_partial(self, client, reset_db, populate):
        r = client.put("/api/pay", json=correct_payment_pay_partial)
        assert r.status_code == HTTPStatus.OK, r.json
        assert r.json == correct_payment_pay_partial_response, r.json

    def test_correct_previously_paid(self, client, reset_db, populate):
        r = client.put("/api/pay", json=correct_payment_previously_paid)
        assert r.status_code == HTTPStatus.OK, r.json
        assert r.json == correct_payment_previously_paid_response, r.json

    def test_correct_all_recap_positive(self, client, reset_db, populate):
        r = client.put("/api/pay", json=correct_payment_all_recap_positive)
        assert r.status_code == HTTPStatus.OK, r.json
        assert r.json == correct_payment_all_recap_positive_response, r.json

    def test_correct_with_default_actual(self, client, reset_db, populate):
        r = client.put("/api/pay", json=correct_payment_default_actual)
        assert r.status_code == HTTPStatus.OK, r.json
        assert r.json == correct_payment_default_actual_response, r.json

    def test_correct_with_nondefault_actual(self, client, reset_db, populate):
        r = client.put("/api/pay", json=correct_payment_nondefault_actual)
        assert r.status_code == HTTPStatus.OK, r.json
        assert r.json == correct_payment_nondefault_actual_response, r.json

    def test_correct_nonzero_diff(self, client, reset_db, populate):
        r = client.put("/api/pay", json=correct_payment_nonzero_diff)
        assert r.status_code == HTTPStatus.OK, r.json
        assert r.json == correct_payment_nonzero_diff_response, r.json

    def test_correct_nonzero_diff_nondefault_actual(self, client, reset_db, populate):
        r = client.put("/api/pay", json=correct_payment_nonzero_diff_nondefault_actual)
        assert r.status_code == HTTPStatus.OK, r.json
        assert r.json == correct_payment_nonzero_diff_nondefault_actual_response, r.json

    def test_incorrect_missing_player_identifier_json_field(
        self,
        client,
        reset_db,
        populate,
    ):
        r = client.put(
            "/api/pay",
            json=incorrect_payment_missing_player_identifier_json_field,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "Missing 'licenceNo' and ('firstName' or 'lastName') fields in json."
            in r.json["error"]
        ), r.json

    def test_incorrect_missing_categories_json_field(self, client, reset_db, populate):
        r = client.put("/api/pay", json=incorrect_payment_missing_categories_json_field)
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert "Missing 'categoryIds' field in json." in r.json["error"], r.json

    def test_incorrect_duplicate_payment(self, client, reset_db, populate):
        r = client.put("/api/pay", json=incorrect_payment_duplicate_payment)
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "Tried to make payment for some entries which were already paid for"
            in r.json["error"]
        ), r.json

    def test_incorrect_without_registration(self, client, reset_db, populate):
        r = client.put("/api/pay", json=incorrect_payment_without_registration)
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "Tried to pay the fee for some categories which did not exist,"
            in r.json["error"]
        ), r.json


class TestAPIDeleteEntries(BaseTest):
    def test_correct_delete_all(self, client, reset_db, populate):
        r = client.delete("/api/entries", json=correct_delete_entries_all)
        assert r.status_code == HTTPStatus.OK, r.json
        assert "remainingEntries" in r.json, r.json
        assert r.json["remainingEntries"] == correct_delete_entries_all_response, r.json

    def test_correct_delete_partial(self, client, reset_db, populate):
        r = client.delete("/api/entries", json=correct_delete_entries_partial)
        assert r.status_code == HTTPStatus.OK, r.json
        assert "remainingEntries" in r.json, r.json
        assert (
            r.json["remainingEntries"] == correct_delete_entries_partial_response
        ), r.json

    def test_incorrect_missing_player_identifier_json_field(
        self,
        client,
        reset_db,
        populate,
    ):
        r = client.delete(
            "/api/entries",
            json=incorrect_delete_entries_missing_player_identifier_json_field,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "Missing 'licenceNo' and ('firstName' or 'lastName') fields in json."
            in r.json["error"]
        ), r.json

    def test_incorrect_missing_categories_json_field(self, client, reset_db, populate):
        r = client.delete(
            "/api/entries",
            json=incorrect_delete_entries_missing_categories_json_field,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert "Missing 'categoryIds' field in json." in r.json["error"], r.json

    def test_incorrect_nonexisting_player(self, client, reset_db, populate):
        r = client.delete(
            "/api/entries",
            json=incorrect_delete_entries_nonexisting_player,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert "No player with licence number" in r.json["error"], r.json

    def test_incorrect_nonexisting_categories(self, client, reset_db, populate):
        r = client.delete(
            "/api/entries",
            json=incorrect_delete_entries_nonexisting_categories,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "Tried to delete some entries which were not registered" in r.json["error"]
        ), r.json

    def test_incorrect_nonexisting_entries(self, client, reset_db, populate):
        r = client.delete(
            "/api/entries",
            json=incorrect_delete_entries_nonexisting_entries,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "Tried to delete some entries which were not registered" in r.json["error"]
        ), r.json


class TestAPIDeletePlayer(BaseTest):
    def test_correct_by_licence(self, client, reset_db, populate):
        r = client.delete("/api/players", json=correct_delete_player_by_licence)
        assert r.status_code == HTTPStatus.NO_CONTENT, r.json

    def test_correct_by_name(self, client, reset_db, populate):
        r = client.delete("/api/players", json=correct_delete_player_by_name)
        assert r.status_code == HTTPStatus.NO_CONTENT, r.json

    def test_incorrect_missing_json_field(self, client, reset_db, populate):
        r = client.delete(
            "/api/players",
            json=incorrect_delete_player_missing_json_field,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "Missing 'licenceNo' and ('firstName' or 'lastName') fields in json."
            in r.json["error"]
        ), r.json

    def test_incorrect_nonexisting_player_by_name(self, client, reset_db, populate):
        r = client.delete(
            "/api/players",
            json=incorrect_delete_player_nonexisting_player_by_name,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert "No player named " in r.json["error"], r.json

    def test_incorrect_nonexisting_player_by_licence(self, client, reset_db, populate):
        r = client.delete(
            "/api/players",
            json=incorrect_delete_player_nonexisting_player_by_licence,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert "No player with licence number " in r.json["error"], r.json


class TestAPIGetCategories(BaseTest):
    def test_get(self, client, reset_db, populate):
        r = client.get("/api/categories")
        assert r.status_code == HTTPStatus.OK, r.json
        assert "categories" in r.json, r.json
        assert r.json["categories"] == correct_get_categories_response


class TestAPIAddPlayer(BaseTest):
    def test_add_correct_player(self, client, reset_db, populate):
        r = client.post("/api/players", json=correct_player)
        assert r.status_code == HTTPStatus.CREATED, r.json
        assert r.json == correct_player_response, r.json

    def test_add_incorrect_missing_player_json_field(self, client, reset_db, populate):
        r = client.post("/api/players", json=incorrect_player_missing_player_json_field)
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "json was missing 'player' field. Player was not added." in r.json["error"]
        ), r.json

    def test_add_incorrect_player_missing_badly_formatted_data(
        self,
        client,
        reset_db,
        populate,
    ):
        r = client.post(
            "/api/players",
            json=incorrect_player_missing_badly_formatted_data,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "Some player data was missing or wrongly formatted. Player was not added."
            in r.json["error"]
        ), r.json

    def test_add_duplicate_player(self, client, reset_db, populate):
        r = client.post("/api/players", json=incorrect_player_duplicate)
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "A player with this licence already exists in the database. Player "
            "was not added." in r.json["error"]
        ), r.json


class TestGetPlayerInfo(BaseTest):
    def test_correct_existing_player(self, client, reset_db, populate):
        r = client.get("/api/players", json=correct_get_player_existing)
        assert r.status_code == HTTPStatus.OK, r.json
        assert "player" in r.json, r.json
        assert (
            r.json["player"] == correct_get_player_existing_response["player"]
        ), r.json
        assert "registeredEntries" in r.json, r.json
        assert (
            r.json["registeredEntries"]
            == correct_get_player_existing_response["registeredEntries"]
        ), r.json

    def test_correct_nonexisting_player(self, client, reset_db, populate):
        r = client.get("/api/players", json=correct_get_player_nonexisting)
        assert r.status_code == HTTPStatus.OK, r.json
        assert "player" in r.json, r.json
        assert (
            r.json["player"] == correct_get_player_nonexisting_response["player"]
        ), r.json
        assert "registeredEntries" in r.json, r.json
        assert (
            r.json["registeredEntries"]
            == correct_get_player_nonexisting_response["registeredEntries"]
        ), r.json

    def test_incorrect_missing_field(self, client, reset_db, populate):
        r = client.get(
            "/api/players",
            json=incorrect_get_player_missing_licence_no_json_field,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "json was missing 'licenceNo' field. Could not retrieve player info."
            in r.json["error"]
        ), r.json


class TestRegisterEntry(BaseTest):
    def test_correct(self, client, reset_db, populate):
        r = client.post("/api/entries", json=correct_registration)
        assert r.status_code == HTTPStatus.CREATED, r.json
        assert "entries" in r.json, r.json
        for entry1, entry2 in zip(r.json["entries"], correct_registration_response):
            for key in entry1:
                assert entry1[key] == entry2[key] or (
                    key == "registrationTime" and entry1["categoryId"] == "1"
                ), r.json

    def test_correct_with_duplicates(self, client, reset_db, populate):
        r = client.post("/api/entries", json=correct_registration_with_duplicates)
        assert r.status_code == HTTPStatus.CREATED, r.json
        assert "entries" in r.json, r.json
        for entry1, entry2 in zip(
            r.json["entries"],
            correct_registration_with_duplicates_response,
        ):
            for key in entry1:
                assert entry1[key] == entry2[key] or (
                    key == "registrationTime" and entry1["categoryId"] == "1"
                ), r.json

    def test_missing_player(self, client, reset_db, populate):
        r = client.post("/api/entries", json=incorrect_registration_missing_player)
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert "No player with licence number" in r.json["error"], r.json

    def test_color_violation(self, client, reset_db, populate):
        r = client.post("/api/entries", json=incorrect_registration_color_violation)
        assert r.status_code == HTTPStatus.BAD_REQUEST
        assert "error" in r.json, r.json
        assert (
            "One or several potential entries violate color constraint."
            in r.json["error"]
        ), r.json

    def test_gender_points_violation(self, client, reset_db, populate):
        r = client.post(
            "/api/entries",
            json=incorrect_registration_gender_points_violation,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST
        assert "error" in r.json, r.json
        assert (
            "Tried to register some entries violating either gender or "
            "points conditions:" in r.json["error"]
        ), r.json

    def test_missing_fields(self, client, reset_db, populate):
        for incorrect_json in incorrect_registrations_missing_json_fields:
            r = client.post("/api/entries", json=incorrect_json)
            assert r.status_code == HTTPStatus.BAD_REQUEST
            assert "error" in r.json, r.json
            assert (
                "Missing either 'licenceNo' or 'categoryIds' field in json."
                in r.json["error"]
            ), r.json

    def test_empty_categories(self, client, reset_db, populate):
        r = client.post("/api/entries", json=incorrect_registration_empty_categories)
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert (
            "No categories to register entries in were sent." in r.json["error"]
        ), r.json

    def test_nonexisting_categories(self, client, reset_db, populate):
        r = client.post(
            "/api/entries",
            json=incorrect_registration_nonexisting_categories,
        )
        assert r.status_code == HTTPStatus.BAD_REQUEST, r.json
        assert "error" in r.json, r.json
        assert "No categories with the following categoryIds" in r.json["error"], r.json

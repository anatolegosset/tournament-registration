import requests
from http import HTTPStatus

import hashlib
import hmac

from datetime import datetime

from xml.etree import ElementTree

from flask import current_app
from shared.api.api_errors import FFTTAPIError


def get_current_formatted_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]


def get_encrypted_timestamp(pwd: str, timestamp: str) -> str:
    # hash password to md5
    encoded_password = hashlib.md5(pwd.encode()).hexdigest()
    # encrypt timestamp with password to sha256
    return hmac.new(
        encoded_password.encode(),
        timestamp.encode(),
        hashlib.sha1,
    ).hexdigest()


def get_player_fftt(licence_no):
    url = current_app.config.get("FFTT_API_URL") + "/xml_licence.php"

    tm = get_current_formatted_timestamp()

    serial_no = current_app.config["FFTT_SERIAL_NO"]
    app_id = current_app.config["FFTT_APP_ID"]
    password = current_app.config["FFTT_PASSWORD"]

    tmc = get_encrypted_timestamp(password, tm)
    params = {
        "serie": serial_no,
        "id": app_id,
        "licence": licence_no,
        "tm": tm,
        "tmc": tmc,
    }
    response = requests.get(url, params=params)

    if response.status_code != HTTPStatus.OK:
        raise FFTTAPIError()

    xml = response.content.decode("utf-8")
    root = ElementTree.fromstring(xml).find("licence")

    if root is None:
        return None

    return {
        "licenceNo": root.find("licence").text,
        "firstName": root.find("prenom").text,
        "lastName": root.find("nom").text,
        "club": root.find("nomclub").text,
        "gender": root.find("sexe").text,
        "nbPoints": int(root.find("point").text),
        "bibNo": None,
        "email": None,
        "phone": None,
        "paymentStatus": {
            "totalActualPaid": 0,
            "totalPaid": 0,
            "totalRegistered": 0,
            "totalPresent": 0,
        },
        "registeredEntries": {},
    }

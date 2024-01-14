from json import loads

from flask import Blueprint, render_template, redirect, url_for, request, current_app
from datetime import datetime

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="../templates",
)


@admin_bp.route("/", methods=["GET"])
def index():
    return redirect(url_for("admin.show_all_players"))


@admin_bp.route("/inscrits", methods=["GET"])
def show_all_players():
    return render_template(
        "/admin_show_all_players.html",
        has_registration_ended=(
            datetime.now() > current_app.config["TOURNAMENT_REGISTRATION_CUTOFF"]
        ),
    )


@admin_bp.route("/categories", methods=["GET"])
def set_categories():
    return render_template("admin_set_categories.html")


@admin_bp.route("/inscrits/<int:licence_no>", methods=["GET"])
def player_page(licence_no):
    if datetime.now() > current_app.config["TOURNAMENT_REGISTRATION_CUTOFF"]:
        show_bib = request.args.get("bib", True, loads)
        return render_template(
            "/admin_player_management_during_tournament.html",
            licence_no=licence_no,
            show_bib=show_bib,
        )
    return render_template(
        "/admin_player_management_pre_tournament.html",
        licence_no=licence_no,
    )


@admin_bp.route("/inscrits_par_tableaux", methods=["GET"])
def players_by_category_page():
    return render_template(
        "/admin_players_by_category.html",
        has_registration_ended=(
            datetime.now() > current_app.config["TOURNAMENT_REGISTRATION_CUTOFF"]
        ),
    )
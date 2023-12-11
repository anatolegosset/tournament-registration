import os
import subprocess
from datetime import datetime

from sqlalchemy import create_engine, Table, func, select
from sqlalchemy.orm import DeclarativeBase, Session, Mapped
from marshmallow import Schema, fields, post_load, post_dump

db_url = os.environ.get("DATABASE_URL")
migration_directory = os.environ.get("MIGRATION_DIR")


def execute_dbmate(command):
    subprocess.run(
        [
            "dbmate",
            "-d",
            migration_directory,
            "--no-dump-schema",
            "--url",
            db_url,
            command,
        ],
        env=os.environ.copy(),
    )


execute_dbmate("up")
engine = create_engine(db_url)

session = Session(engine)


class Base(DeclarativeBase):
    pass


class Category(Base):
    start_time: Mapped[datetime]
    entry_fee: Mapped[int]
    category_id: Mapped[str]

    __table__ = Table("categories", Base.metadata, autoload_with=engine)

    def __repr__(self):
        schema = CategorySchema()
        return str(schema.dump(self))


class Player(Base):
    licence_no: Mapped[int]
    bib_no: Mapped[int]

    __table__ = Table("players", Base.metadata, autoload_with=engine)

    def __repr__(self):
        schema = PlayerSchema()
        return str(schema.dump(self))


def player_from_licence(licence_no):
    return session.scalar(select(Player).filter_by(licence_no=licence_no))


def player_not_found_message(licence_no):
    return f"No player with licence number {licence_no} exists in the database."


class Entry(Base):
    entry_id: Mapped[int]
    marked_as_present: Mapped[bool]
    category_id: Mapped[str]
    licence_no: Mapped[int]
    marked_as_paid: Mapped[bool]

    __table__ = Table("entries", Base.metadata, autoload_with=engine)

    def __repr__(self):
        schema = EntrySchema()
        return str(schema.dump(self))


class CategorySchema(Schema):
    category_id = fields.Str(data_key="categoryId")
    color = fields.Str()
    min_points = fields.Int(data_key="minPoints")
    max_points = fields.Int(data_key="maxPoints")
    start_time = fields.DateTime(data_key="startTime", allow_none=False, required=True)
    women_only = fields.Bool(data_key="womenOnly")
    entry_fee = fields.Int(data_key="entryFee")
    reward_first = fields.Int(data_key="rewardFirst")
    reward_second = fields.Int(data_key="rewardSecond")
    reward_semi = fields.Int(data_key="rewardSemi")
    reward_quarter = fields.Int(data_key="rewardQuarter")
    max_players = fields.Int(data_key="maxPlayers")
    overbooking_percentage = fields.Int(data_key="overbookingPercentage")

    @post_load
    def make_field(self, data, **kwargs):
        return Category(**data)

    @post_dump
    def add_entry_count(self, data, **kwargs):
        data["entryCount"] = session.scalar(
            select(func.count(Entry.entry_id)).where(
                Entry.category_id == data["categoryId"],
            ),
        )
        return data


class PlayerSchema(Schema):
    # TODO: use nested fields for licence_no & bib_no, maybe change to player & category
    licence_no = fields.Int(data_key="licenceNo")
    bib_no = fields.Int(data_key="bibNo")
    first_name = fields.Str(data_key="firstName", required=True)
    last_name = fields.Str(data_key="lastName", required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    gender = fields.Str(required=True)
    nb_points = fields.Int(data_key="nbPoints", required=True)
    club = fields.Str(required=True)
    payment_diff = fields.Int(data_key="paymentDiff")

    @post_load
    def make_field(self, data, **kwargs):
        return Player(**data)

    @post_dump
    def add_entries_info(self, data, **kwargs):
        if self.context.get("with_entries_info", False):
            data["registeredEntries"] = EntrySchema(many=True).dump(
                session.scalars(
                    select(Entry).where(Entry.licence_no == data["licenceNo"]),
                ).all(),
            )
        return data


class EntrySchema(Schema):
    entry_id = fields.Int(data_key="entryId")
    category_id = fields.Str(data_key="categoryId")
    licence_no = fields.Int(data_key="licenceNo")
    color = fields.Str()
    registration_time = fields.DateTime(data_key="registrationTime")
    marked_as_paid = fields.Bool(data_key="markedAsPaid")
    marked_as_present = fields.Bool(data_key="markedAsPresent")

    @post_load
    def make_field(self, data, **kwargs):
        return Entry(**data)

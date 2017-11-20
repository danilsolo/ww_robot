from peewee import *


db = SqliteDatabase('db.db')


class profiles(Model):
    username = TextField(null=True, default=None)
    heroflag = TextField(null=True, default=None)
    heroname = TextField(null=True, default=None)
    prof = TextField(null=True, default=None)
    attack = IntegerField(default=0)
    defense = IntegerField(default=0)
    exp = IntegerField(default=0)
    stamina = IntegerField(default=0)
    mana = IntegerField(default=0)
    gold = IntegerField(default=0)
    gems = IntegerField(default=0)
    wins = IntegerField(default=0)
    sword = TextField(null=True, default=None)
    dagger = TextField(null=True, default=None)
    head = TextField(null=True, default=None)
    arms = TextField(null=True, default=None)
    body = TextField(null=True, default=None)
    legs = TextField(null=True, default=None)
    specials = TextField(null=True, default=None)
    stock = IntegerField(default=0)
    pet = TextField(null=True, default=None)
    proftime = TextField(null=True, default=None)
    rights = IntegerField(default=0)
    mobs = BooleanField(default=False)

    class Meta:
        database = db

# profiles.create_table()
# a = profiles()
# a.save()
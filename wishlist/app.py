
from flask import Flask, render_template, request, redirect, url_for
from uuid import uuid4
from datetime import datetime
from dotenv import dotenv_values


from .db import db
from .models import Room, CheckList

my_config = dotenv_values(".env")


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = my_config["SQL_DB"]

db.init_app(app)

with app.app_context():
    db.create_all()




@app.route("/", methods=["GET", "POST"])
def home():
    rooms = db.session.execute(db.select(Room)).scalars().all()
    context = {
        "rooms": rooms
    }
    return render_template("rooms.html", context=context)

@app.route("/rooms", methods=["GET", "POST"])
def get_rooms():
    rooms = db.session.execute(db.select(Room)).scalars().all()
    context = {
        "rooms": rooms
    }
    return render_template("rooms.html", context=context)


@app.route("/create", methods=["GET", "POST"])
def create_room():
    uuid = uuid4()

    if request.method == "POST":
        name = request.form["room_name"]
        try:
            room = Room(uuid=str(uuid), name=name, date_created=datetime.now())
            print(f"Create room {room.uuid}")
            db.session.add(room)
            db.session.commit()

            return redirect(url_for("get_rooms"))
        except:
            message="There was an error creating the room"
            context = {
                "message": message
            }
            return render_template("error.html", context=context)


@app.route("/rooms/delete/<string:uuid>", methods=["GET", "POST"])
def delete_room(uuid):
    room = db.session.execute(db.select(Room).filter_by(uuid=uuid)).scalar_one()
    try:
        db.session.delete(room)
        db.session.commit()
    except:
        return render_template("error.html", context="There was an error deleting the room")
    return redirect(url_for("get_rooms"))



@app.route("/rooms/<string:uuid>", methods=["GET", "POST"])
def get_checklist(uuid):
    room = db.session.execute(db.select(Room).filter_by(uuid=uuid)).scalar_one()
    contents = db.session.execute(db.select(CheckList).filter_by(room_id=uuid)).scalars().all()
    context = {
        "contents" : contents,
        "room": room
    }
    return render_template("checklist.html", context=context)



@app.route("/rooms/<string:uuid>/create", methods=["GET", "POST"])
def create_checklist(uuid):
    if request.method == "POST":
        try:
            item = CheckList(room_id=str(uuid), content=str(request.form["message"]))
            db.session.add(item)
            db.session.commit()
            return redirect(url_for("get_checklist", uuid=uuid))
        except:
            message="There was an error creating the checklist"
            context = {
                "message": message
            }
            return render_template("error.html", context=context)



@app.route("/rooms/<string:uuid>/update/<int:id>/", methods=["GET", "POST"])
def update_checklist(uuid, id):
    if request.method == "POST":
        try:
            item = db.session.execute(db.select(CheckList).filter_by(id=id)).scalar_one()
            item.content = request.form["amend"]
            db.session.commit()
            return redirect(url_for("get_checklist", uuid=uuid))
        except:
            message="There was an error Updating the checklist!"
            context = {
                "message": message
            }
            return render_template("error.html", context=context)




@app.route("/rooms/<string:uuid>/delete/<int:id>/", methods=["GET", "POST"])
def delete_checklist(uuid, id):
    item = db.session.execute(db.select(CheckList).filter_by(id=id)).scalar_one()
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for("get_checklist", uuid=uuid))
    except:
        message="There was an error deleting the checklist!"
        context = {
            "message": message
        }
        return render_template("error.html", context=context)




@app.route("/rooms/join", methods=["GET", "POST"])
def join_room():

    if request.method == "POST":
        print("Inside join room")
        room_id = request.form["room_id"]
        print(f"got room id: {room_id}")

        try:
            _ = db.session.execute(db.select(Room).filter_by(uuid=room_id)).scalar_one()
            return redirect(url_for("get_checklist", uuid=room_id))
        except:
            message="No such room found 💀. Please check your Room ID 🥸"
            context = {
                "message": message
            }
            return render_template("error.html", context=context)
    
    else:
        return redirect(url_for("get_rooms"))
    

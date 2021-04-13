from . import db
from psycopg2 import connect
import random


class UserModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    senha = db.Column(db.String, nullable=False)

    lista_perguntas = db.relationship(
        "PerguntaModel",
        lazy="joined",
        backref=db.backref("question", lazy="joined"),
    )


def db_connection():
    return connect(
        dbname="qzen", user="admin", password="admin", port="5432", host="localhost"
    )


def bd_query_post_users_register(name, email, password):
    connection = db_connection()

    ids = random.randint(0, 1000)
    questions_list = "TESTE {}".format(str(ids))
    cur = connection.cursor()

    cur.execute(
        """INSERT INTO "user"
    (id, "name", "email", "password", "questions_list")
    values
     ({},'{}','{}','{}','{}')
    ;""".format(
            int(ids), name, email, password, questions_list
        )
    )

    try:
        cur.fetchall()
        response = {"name": name, "email": email}

    except:
        response = "Bad request"

    connection.commit()
    cur.close()
    connection.close()
    return response


def bd_query_post_users_login(email, password):
    connection = db_connection()

    cur = connection.cursor()

    cur.execute(
        """SELECT * FROM user WHERE "email" = '{}' AND "password" = '{}';""".format(
            email, password
        )
    )

    try:
        fetch = cur.fetchall()
        response = {"id": fetch[0], "nome": fetch[1]}

    except:
        response = False

    connection.commit()
    connection.close()
    return response


def bd_query_delete_id_user(ids):
    connection = db_connection()

    cur = connection.cursor()

    cur.execute("""DELETE FROM "user" WHERE id = {};""".format(int(ids)))

    try:
        cur.fetchall()
        response = "User deleted"
    except:
        response = "User not found"

        connection.commit()
        connection.close()
    return response

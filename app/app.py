import flask

from database import get_db_connection

app = flask.Flask(__name__)


@app.route("/test-db")
def test_database():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        database = cursor.fetchone()
        cursor.close()
        connection.close()
        return {"status": "success", "database": database[0]}
    except Exception as error:
        return {"status": "error", "message": str(error)}, 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
        connection.close()

from flask import Flask, jsonify
# from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import docker

app = Flask(__name__)
# CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://jakub_rozkosz:!Jakub01@localhost:3306/alg_ranking_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SampleData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

    if not SampleData.query.first():
        sample1 = SampleData(value='Przykładowa wartość 1')
        sample2 = SampleData(value='Przykładowa wartość 2')

        db.session.add_all([sample1, sample2])
        db.session.commit()

@app.route('/api/data')
def get_data():
    data_from_db = SampleData.query.all()

    sample_data = [data.value for data in data_from_db]

    return jsonify(sample_data)

@app.route('/run_container')
def run_container():
    try:
        client = docker.from_env()

        image, build_logs = client.images.build(path='.', dockerfile='Dockerfile')

        container = client.containers.run(image.id, detach=True)

        return jsonify({"success": True, "message": "Container started successfully."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)


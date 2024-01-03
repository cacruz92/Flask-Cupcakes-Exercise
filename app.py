"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

with app.app_context():
    db.create_all()

def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary"""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

@app.route('/api/cupcakes')
def list_cupcakes():
    """Return JSON {'cupcakes': [{id, flavor, size, rating, image}]}"""
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes = serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def list_single_cupcake(cupcake_id):
    """Return JSON like: {cupcake:{id, flavor, size, rating, image}}."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake = serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake and return with JSON like: {cupcake: {id, flavor, size, rating, image}}. """
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    return (jsonify(cupcake = serialized), 201)




if __name__ == '__main__':
    app.run()
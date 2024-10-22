from config import *
from crud_operations import require_api_key

@app.route('/get_ratings', methods=['GET'])
@require_api_key
def get_ratings():
    ratings = PortfolioRatings.query.all()
    return jsonify([{"id": rating.id, "ip address": rating.ip_address, "rate": rating.rate, 
                     "Date Created": rating.Date_Created, "Last Updatd": rating.Date_Updated} 
                    for rating in ratings]), 200
    
@app.route('/get_rating/<int:id>', methods=['GET'])
@require_api_key
def get_rating(id):
    user = PortfolioRatings.query.filter(PortfolioRatings.id == id).first()
    if user:
        user = user.__dict__
        # del user["password"]
        del user["_sa_instance_state"]
        return jsonify([user]), 200
    else:
        return jsonify({"msg": "PortfolioRatings does not exist"}), 400
    
@app.route('/del_rating/<int:id>', methods=['DELETE'])
@require_api_key
def delete_rating(id):
    user = PortfolioRatings.query.get_or_404(id)
    if user:
        db.session.delete(user) 
        db.session.commit()
        return jsonify({"msg": "PortfolioRatings deleted"}), 200
    else:
        return jsonify({"msg": "PortfolioRatings does not exist"}), 400
    
@app.route('/update_rating/<int:id>', methods=['PUT'])
@require_api_key
def update_rating(id):
    user = PortfolioRatings.query.get_or_404(id)
    if user:
        data = request.get_json()
        for key, value in data.items():
            user.key = value
        db.session.commit()
        return jsonify({"msg": "PortfolioRatings updated"}), 200
    else:
        return jsonify({"msg": "PortfolioRatings does not exist"}), 400

@app.route('/add_rating', methods=['POST'])
# @require_api_key
def add_rating():
    data = request.get_json()
    print("Payload : ", data)
    if data:
        is_duplicate = PortfolioRatings.query.filter_by(ip_address=data['ip_address']).first()
        if is_duplicate:
            return jsonify({"msg": "Avoid duplicates"}), 400
        db.session.add(PortfolioRatings(ip_address=data["ip_address"], rate=data["rating"])) 
        db.session.commit()
        return jsonify({"msg": "New Portfolio Ratings Added"}), 200
    else:
        return jsonify({"msg": "Check your input"}), 400
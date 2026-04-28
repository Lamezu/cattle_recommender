from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from services.main_controller import MainController
import os

from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'cattle_pro_premium_secret_key' # Clave fija para que no te eche al reiniciar
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

controller = MainController()

@app.route('/')
def index():
    if 'farmer_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        answer = request.form.get('security_answer').strip().lower()
        
        farmers = controller.get_farmers()
        user = next((f for f in farmers if f.name.lower() == name.lower()), None)
        
        if user and user.security_answer and user.security_answer.strip().lower() == answer:
            session.permanent = True
            session['farmer_id'] = user.farmer_id
            return redirect(url_for('index'))
            
        return render_template('login.html', error="Datos incorrectos, inténtalo de nuevo")
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name').strip()
    answer = request.form.get('security_answer').strip().lower()
    
    farmers = controller.get_farmers()
    new_id = f"F{len(farmers) + 1:04d}"
    
    controller.register_farmer(new_id, name, answer)
    session.permanent = True
    session['farmer_id'] = new_id
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/current_user')
def get_current_user():
    if 'farmer_id' not in session:
        return jsonify({"error": "No session"}), 401
    farmers = controller.get_farmers()
    user = next((f for f in farmers if f.farmer_id == session['farmer_id']), None)
    if not user:
        session.clear()
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user.farmer_id, "name": user.name})

@app.route('/api/recommendations/<farmer_id>')
def get_recommendations(farmer_id):
    breed = request.args.get('breed')
    search = request.args.get('search')
    sort = request.args.get('sort')
    recs = controller.get_personalized_recommendations(farmer_id, breed, search, sort)
    return jsonify([vars(c) for c in recs])

@app.route('/api/purchases/<farmer_id>')
def get_purchases(farmer_id):
    breed = request.args.get('breed')
    search = request.args.get('search')
    sort = request.args.get('sort')
    recs = controller.get_purchases(farmer_id, breed, search, sort)
    return jsonify([vars(c) for c in recs])

@app.route('/api/catalog')
def get_catalog():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 15)) # Forzamos a 15 como acordamos
    breed = request.args.get('breed')
    search = request.args.get('search')
    sort = request.args.get('sort')
    
    skip = (page - 1) * limit
    
    cows = controller.get_catalog(skip=skip, limit=limit, breed=breed, search=search, sort=sort)
    total = controller.get_total_cows(breed=breed, search=search)
    
    return jsonify({
        "cows": [vars(c) for c in cows],
        "total": total,
        "page": page,
        "limit": limit
    })

@app.route('/api/similar/<cow_id>')
def get_similar(cow_id):
    recs = controller.get_similar_cows(cow_id)
    return jsonify([vars(c) for c in recs])

@app.route('/api/top-rated')
def get_top_rated():
    breed = request.args.get('breed')
    search = request.args.get('search')
    sort = request.args.get('sort')
    recs = controller.get_top_rated(breed, search, sort)
    return jsonify([vars(c) for c in recs])

@app.route('/api/most-purchased')
def get_most_purchased():
    breed = request.args.get('breed')
    search = request.args.get('search')
    sort = request.args.get('sort')
    recs = controller.get_most_purchased(breed, search, sort)
    return jsonify([vars(c) for c in recs])

@app.route('/api/buy', methods=['POST'])
def buy_cow():
    data = request.json
    success = controller.buy_cow(data['farmer_id'], data['cow_id'])
    return jsonify({"success": success})

@app.route('/api/return', methods=['POST'])
def return_cow():
    data = request.json
    success = controller.delete_purchase(data['farmer_id'], data['cow_id'])
    return jsonify({"success": success})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

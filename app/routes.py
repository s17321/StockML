from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app
from app import db
from app.models import User, Portfolio, Position
from app.utils import get_stock_price

# Tworzenie blueprintu
main = Blueprint('main', __name__)

@main.route('/')
def index():
    user = User.query.first()  # Na potrzeby przykładu, zakładamy pierwszego użytkownika
    if user is None:
        # Jeśli nie ma użytkownika, zwróć stronę błędu lub stwórz nowego użytkownika
        return "Brak użytkowników w bazie danych", 404

    portfolio = Portfolio.query.filter_by(user_id=user.id).first()
    positions = Position.query.filter_by(portfolio_id=portfolio.id, closed=False).all()
    return render_template('index.html', portfolio=portfolio, positions=positions)

@main.route('/buy', methods=['POST'])
def buy():
    user = User.query.first()  # Na potrzeby przykładu, zakładamy pierwszego użytkownika
    ticker = request.form['ticker']
    amount = float(request.form['amount'])
    price = get_stock_price(ticker)
    quantity = int(amount // price)
    cost = quantity * price

    portfolio = Portfolio.query.filter_by(user_id=user.id).first()
    if portfolio.balance >= cost:
        portfolio.balance -= cost
        db.session.commit()
        
        position = Position(portfolio_id=portfolio.id, ticker=ticker, quantity=quantity, buy_price=price)
        db.session.add(position)
        db.session.commit()
    
    return redirect(url_for('main.index'))

@main.route('/sell/<int:position_id>')
def sell(position_id):
    position = Position.query.get(position_id)
    if position and not position.closed:
        price = get_stock_price(position.ticker)
        proceeds = position.quantity * price

        portfolio = position.portfolio
        portfolio.balance += proceeds
        db.session.commit()

        position.closed = True
        position.close_price = price
        position.close_date = datetime.utcnow()
        db.session.commit()
    
    return redirect(url_for('main.index'))

@main.route('/secret-key')
def show_secret_key():
    return f"SECRET_KEY: {current_app.config['SECRET_KEY']}"
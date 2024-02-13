from flask import Flask, render_template, request, redirect, url_for,session,flash
import requests
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def product_details():
    api_url = "https://fakestoreapi.com/products"
    # Make a GET request
    response = requests.get(api_url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response content (assuming it's JSON)
        data = response.json()
        return data
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    data=product_details()
    return render_template('/Products.html',data=data)
    
@app.route('/category/mens_clothing')
def mens_clothing():

    data = product_details()
    return render_template('/mens_category.html',data=data)


@app.route('/category/womens_clothing')
def womens_clothing():
   
        data = product_details()
        return render_template('/womens_category.html',data=data)
    

@app.route('/category/electronics')
def electronics():
   
        data = product_details()
        return render_template('/electronics_category.html',data=data)
   

@app.route('/category/jewelery')
def jewelery():
 
        data =product_details()
        return render_template('/jewelery_category.html',data=data)
    
@app.route('/cart/<string:id>', methods=['GET'])
def add_to_cart(id):

    # Retrieving product information from the fake API
    req = requests.get("https://fakestoreapi.com/products/{}".format(id))
    product = json.loads(req.content)

    # Check if 'cart' key exists in session, if not, initialize an empty list
    if 'cart' not in session:
        session['cart'] = []

    # Append product to cart
    if any(item['id'] == int(id) for item in session['cart']):
        flash('Product is already in your cart!')
        return redirect(url_for('products'))
    else:
        product['quantity'] = 1
        session['cart'].append(product)
        flash('Product added to cart successfully!')
        return redirect(url_for('products'))

@app.route('/cart', methods=['GET'])
def view_cart():
    if 'cart' in session:
        cart_items = session['cart']
        return render_template('cart.html', cart_items=cart_items)
    else:
        flash('Your cart is empty.')
        return render_template('cart.html', cart_items=None)


@app.route('/update_quantity/<string:id>', methods=['GET','POST'])
def update_quantity(id):
    if 'cart' in session:
        cart_items = session['cart']
        for item in cart_items:
            if item['id'] == int(id):
                if request.form['action'] == '+':
                    item['quantity'] += 1
                elif request.form['action'] == '-':
                    if item['quantity'] > 1: 
                        item['quantity'] -= 1
                session['cart'] = cart_items
                flash('Quantity updated successfully!', 'cart_update')
                break
    return redirect(url_for('view_cart'))

@app.route('/remove_from_cart/<string:id>', methods=['GET'])
def remove_from_cart(id):
    if 'cart' in session:
        cart_items = session['cart']
        for item in cart_items:
            if item['id'] == int(id):
                cart_items.remove(item)
                session['cart'] = cart_items
                flash('Product removed from cart successfully!', 'cart_remove')
    return redirect(url_for('view_cart'))
@app.route('/buy_now')
def buy_now():
    session ['cart'] = []
    return render_template('buy_now.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)

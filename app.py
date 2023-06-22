from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flaskMongo'  
mongo = PyMongo(app)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=['POST'])
def create():
    # Obtain product data from form
    product_name = request.form['product_name']
    product_details = request.form['product_details']
    product_price = float(request.form['product_price'])
    product_category = request.form['product_category']
    product_brand = request.form['product_brand']
    product_quantity = int(request.form['product_quantity'])

    # Create data dictionary
    data = {
        'product_name': product_name,
        'product_details': product_details,
        'product_price': product_price,
        'product_category': product_category,
        'product_brand': product_brand,
        'product_quantity': product_quantity
    }

    # Insert data into MongoDB
    mongo.db.products.insert_one(data)

     # Display JavaScript alert after creating the product
    script = """
        <script>
            alert('Product created successfully!');
            window.location.href = '/view';
        </script>
    """
    return script

    # Redirect to the table view
    return render_template('table_view.html', products=mongo.db.products.find())


@app.route('/view')
def view():
    return render_template('table_view.html', products=mongo.db.products.find())


if __name__ == '__main__':
    app.run(debug=True)
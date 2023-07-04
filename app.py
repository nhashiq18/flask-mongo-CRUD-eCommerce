from flask import Flask, render_template, request, jsonify, redirect, make_response, Response
from flask_pymongo import PyMongo
import json as json_module
import csv
from bson import ObjectId

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


@app.route('/view')
def view():
    products = mongo.db.products.find()
    return render_template('table_view.html', products=products)

@app.route('/edit/<string:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    if request.method == 'GET':
        product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
        return render_template('edit.html', product=product)
    elif request.method == 'POST':
        # Obtain updated product data from form
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

        # Update product in MongoDB
        update_product = mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$set': data})

        if update_product:
            # Display JavaScript alert after deleting the product
            script = """
                <script>
                    alert('Product updated successfully!');
                    window.location.href = '/view';
                </script>
            """
            return script

        # Redirect to table view page with success parameter
        return redirect('/view')

@app.route('/delete/<string:product_id>', methods=['POST', 'GET'])
def delete(product_id):
    if request.method == 'POST' or request.method == 'DELETE':
        # Delete product from MongoDB based on product ID
        deleted_product = mongo.db.products.find_one_and_delete({'_id': ObjectId(product_id)})

        if deleted_product:
            # Display JavaScript alert after deleting the product
            script = """
                <script>
                    alert('Product deleted successfully!');
                    window.location.href = '/view';
                </script>
            """
            return script

        return "Product deletion failed."

    return 'Invalid request method.'


# Route for downloading product data as CSV or JSON based on format selection
@app.route('/download_data_csv')
def download_data_csv():
        products = mongo.db.products.find()
        csv_data = "Name,Details,Price,Category,Brand,Quantity\n"  # CSV header

        for product in products:
            csv_data += f"{product['product_name']},{product['product_details']},{product['product_price']},{product['product_category']},{product['product_brand']},{product['product_quantity']}\n"

        # Create a response with CSV content
        response = Response(csv_data, mimetype='text/csv')
        response.headers.set('Content-Disposition', 'attachment', filename='product_data.csv')

        return response

# Route for downloading product data as formatted JSON
@app.route('/json')
def json():
    products = mongo.db.products.find()
    product_list = []

    for product in products:
        product_list.append({
            'Name': product['product_name'],
            'Details': product['product_details'],
            'Price': product['product_price'],
            'Category': product['product_category'],
            'Brand': product['product_brand'],
            'Quantity': product['product_quantity']
        })

    # Convert product_list to formatted JSON using json_module.dumps()
    json_data = json_module.dumps(product_list, indent=2)

    # Create a response with JSON content
    response = Response(json_data, mimetype='application/json')
    response.headers.set('Content-Disposition', 'attachment', filename='product_data.json')

    return response

if __name__ == '__main__':
    app.run(debug=True)

   

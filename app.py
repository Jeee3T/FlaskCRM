from flask import Flask
from config.firebase_config import db
from routes.customer_routes import(
    get_customers,
    create_customer,
    get_customer_by_id,
    update_customer, 
    delete_customer, 
)

app = Flask(__name__)

# @app.route('/')
# def home(): 
#     return {"message " : "Flask is running"}

# @app.route('/test')
# def test():
#     db.collection('customers').document('test1').set({"name": "Test User"})
#     return {"status": "written to firestore"}

app.add_url_rule('/customers',view_func = create_customer,methods=['POST'])
app.add_url_rule('/customers', view_func = get_customers, methods = ['GET'])
app.add_url_rule('/customers/<id>', view_func = get_customer_by_id, methods = ['GET'])
app.add_url_rule('/customers/<id>', view_func = update_customer , methods = ['PUT'])
app.add_url_rule('/customers/<id>', view_func = delete_customer, methods = ['DELETE'])



if __name__ == '__main__':
    app.run(debug= True, port =5000)
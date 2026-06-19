from flask import request, jsonify
from models.customer_model import validate_customer
from config.firebase_config import db
from datetime import datetime , UTC

#not going with the blueprint here ,instead using direct route registration
#creating a customer route

#POST route
def create_customer():
    data = request.get_json()
    error = validate_customer(data)

    if error:
        return jsonify({"error" : error}), 400
    
    data["created_at"] = datetime.now(UTC).isoformat()
    doc_ref = db.collection('customers').document()
    doc_ref.set(data)
    return jsonify({"id" : doc_ref.id , **data}),201


#GET route
#fetch customer details with pagination support
def get_customers():
    name = request.args.get('name')
    email = request.args.get('email')
    page_size = int(request.args.get('page_size',10))
    start_after_id = request.args.get('start_after')

    query = db.collection('customers')

    if email: 
        query = query.where("email" , "==" , email)
    elif name: 
        query = query.where("name" , "==", name)

    query = query.order_by('__name__').limit(page_size)

    if start_after_id:
        last_doc = db.collection('customers').document(start_after_id).get()
        if last_doc.exists:
            query = query.start_after(last_doc)

    docs = list(query.stream())
    customers = [{"id" : d.id , **d.to_dict()} for d in docs]

    next_cursor = customers[-1]["id"] if len(customers) == page_size else None
    return jsonify({"customers" : customers, "next_start_page" : next_cursor}), 200
    


#fetch customer details by id 
def get_customer_by_id(id):
    doc = db.collection('customers').document(id).get()


    if not doc.exists:
        return jsonify({"error": "Customer Not Found "}),404
    
    return jsonify({"id" : doc.id, **doc.to_dict()}),200


#update existing record with id
def update_customer(id):
    data = request.get_json()
    doc_ref = db.collection('customers').document(id)

    if not  doc_ref.get().exists:
        return jsonify({"error" :  "Customer not found "}), 404
    
    data["updated_at"] = datetime.now(UTC).isoformat()
    doc_ref.update(data)
    return jsonify({"id" :id  , **doc_ref.get().to_dict()}),200


    
#removes a customer record by id
def delete_customer(id):
    doc_ref = db.collection('customers').document(id)

    if not doc_ref.get().exists:
        return jsonify({"error" : "Customer not found"}),404
    
    doc_ref.delete()
    return jsonify({"message" : "Customer deleted"}),200
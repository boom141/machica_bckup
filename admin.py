from flask import make_response, jsonify
from flask_restful import Resource
from mongo_init import*
from settings import app, api

class Get_User_list(Resource):
	def get(self):
		with app.app_context():
			try:
				user_list = machica_users.find({},{'_id':0})
				return list(user_list)
			except:
				return make_response(jsonify({'message':'database_access_denied', 'error':200}))

api.add_resource(Get_User_list,'/admin/getUserList')

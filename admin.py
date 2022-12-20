from flask import make_response, jsonify, request
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


	def post(self):
		with app.app_context():
			try:
				user_email = request.form['user_email']
				user = machica_users.find_one({'email':user_email},{'_id':0})

				return user
			except:
				return make_response(jsonify({'message':'database_access_denied', 'error':200}))


api.add_resource(Get_User_list,'/admin/getUserList')

class Daily_appointment(Resource):
	def post(self):
		with app.app_context():
			try:
				current_date = request.form['current_date']
				print(current_date)
				appointments = machica_bookings.find({'date':current_date},{'_id':0})

				return list(appointments)
			except:
				return make_response(jsonify({'message':'database_access_denied', 'error':200}))

api.add_resource(Daily_appointment,'/admin/DailyAppointments')
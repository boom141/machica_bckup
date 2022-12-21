from flask import make_response, jsonify, request
from flask_restful import Resource
from datetime import datetime
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


class Monthly_Sold(Resource):
	def get(self):
		with app.app_context():
			try:
				today_month = datetime.now().month
				bookings = machica_bookings.find({},{'_id':0})

				total_bookings = 0
				for book in bookings:
					verify_month = book['date'].split('-')

					if int(verify_month[1]) == today_month:
						total_bookings += 1

				orders = machica_orders.find({},{'_id':0})

				total_orders = 0
				for order in orders:
					verify_month = order['date'].split('-')

					if int(verify_month[1]) == today_month:
						total_orders += 1

				return {'bookings_total':total_bookings, 'total_orders':total_orders, 'current_date':today_month, 'success_message':'status_complete'}
			except:
				return make_response(jsonify({'message':'database_access_denied', 'error':200}))

api.add_resource(Monthly_Sold,'/admin/totalMonthSold')

class Daily_appointment(Resource):
	def get(self):
		with app.app_context():
			try:
				today_day = datetime.now().day
				today_month = datetime.now().month
				today_year = datetime.now().year

				current_date = f'{today_year}-{today_month}-{today_day}'

				appointments = machica_bookings.find({'date':current_date},{'_id':0})

				return list(appointments)
			except:
				return make_response(jsonify({'message':'database_access_denied', 'error':200}))

api.add_resource(Daily_appointment,'/admin/DailyAppointments')
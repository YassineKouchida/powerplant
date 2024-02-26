#Project realized by Yassine Kouchida 
from flask import Flask, jsonify,request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
books = [{'id':1, 'title' : 'Python essentials'}]
demo_payload = json.load(open('example_payloads/payload3.json'))

def calculate(input_payload):
	payload1 = input_payload

	current_payload = payload1
	current_load = payload1['load']
	print(current_payload)
	efficiencies ={}
	powerplants = current_payload['powerplants']

	print(powerplants)
	co2_price = current_payload['fuels']['co2(euro/ton)']
	gas_price = current_payload['fuels']['gas(euro/MWh)']
	kerosine_price = current_payload['fuels']['kerosine(euro/MWh)']
	wind_percentage = current_payload['fuels']['wind(%)']*0.01;

	result = {}

	generated_wind = 0.0
	def price(key,mwh,efficiency):
		if key == "gasfired":
			generated_amount = mwh*efficiency
			return 0.3*generated_amount*co2_price + mwh*gas_price; 
		if key == "turbojet":
			return mwh*kerosine_price
		if key == "windturbine":
			return 0


	for p in powerplants:
		name = p['name']
		current_type= p['type']
		efficiency = p['efficiency']
		pmin = p['pmin']
		pmax = p['pmax']
		result[name] = 0
		if current_type == 'windturbine':
			generated_wind = generated_wind+ wind_percentage*pmax
			result[name] = result[name]+pmax
		print("generated wind is")
		print(generated_wind)
		print('**')
		print(name)
		print(current_type)
		print(efficiency)
		print('***')

		current_price = price(current_type,1,efficiency)
		if current_price >0:
			efficiencies[name]= {
				efficiency/current_price
		
			}
			
	print(result)
	print(generated_wind)
	print(efficiencies)
	if generated_wind <= current_load:
		current_load = current_load - generated_wind
		
	print(current_load)


	print("Hello test! ")
	efficiencies = (sorted(efficiencies.items(), key=lambda x:x[1])) 
	efficiencies.reverse()
	print(efficiencies)
	print("allo")


	for plant in efficiencies:
		best_plant = plant[0]
		for p in powerplants:
			if best_plant == p['name']:
				print(best_plant)
				name = p['name']
				pmin = p['pmin']
				pmax = p['pmax']
				eff = p['efficiency']
				
				a = pmin*eff
				b = pmax*eff
				power = 0.0
				
				if current_load >= a and current_load <= b:
					power = current_load/eff;
					current_load = 0;
				elif current_load >b:
					current_load = current_load - b
					power = pmax
				print(current_load)

				result[name] = result[name]+power
				
					


	print(current_load)
	print(current_load)
	print(result)
	final_result = [
	]
	for item in result.items():
		final_result.append({
			item[0]:item[1]
		})
	print(final_result)
	return final_result



@app.route('/productionplan',methods=['POST'])
def get_response():
	print(request.form)
	parametre = json.loads(request.data)
	result = calculate(parametre)
	return jsonify(result)

@app.route('/payloads/1',methods=['GET'])
def get_payload1():
	return  jsonify({'payload': payload1})
 
@app.route('/books', methods=['GET'])
def get_books():
	return jsonify({'books' :books})

	
if __name__ == '__main__':
	app.run(debug=True, port=8888)

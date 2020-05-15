from flask import Flask, jsonify, request
from flask_cors import CORS
from src.ProjectInterface import ProjectInterface

app = Flask(__name__)
CORS(app)

@app.route('/api/project_1', methods=['POST'])
def project_1():
	content = request.json
	print(content)
	if not content :
		abort(404)
	try :
		response_body = ProjectInterface.runSearch(content['body'])
	except :
		abort(500)
	return jsonify({
		'status': 'success',
		'body': response_body
	})

@app.route('/api/project_2', methods=['POST'])
def project_2():
	content = request.json
	if not content :
		abort(404)
	try :
		response_body = ProjectInterface.runMinimax(content['body'])
		print(response_body)
	except :
		abort(500)
	return jsonify({
		'status': 'success',
		'body': response_body
	})

@app.route('/api/project_3', methods=['POST'])
def project_3():
	content = request.json
	if not content :
		abort(404)
	try :
		response_body = ProjectInterface.runMdp(content['body'])
		print(response_body)
	except :
		abort(500)
	return jsonify({
		'status': 'success',
		'body': response_body
	})
   
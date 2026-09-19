import json


#Memoria de la Base de Datos
#id simulado
tasks = []

next_id = 1

#Funcion para buscar una tarea por su id
#Recorre el diccionario tasks obteniendo uno distinto en cada iteracion
#compara si es la tarea buscada
#Retorna la tarea si la encontro
#Si no la encuentra retona None
def find_task(task_id):
	
	for task in tasks:
		
		if task["id"] == task_id:

			return task

	return None


#Funcion que controla las consultas
def application(environ, start_response):

	#Variable global que guarda el proximo id
	global next_id

	#Obtencion de informacion de environ
	#Request_Method que guarda el metodo de la consulta
	#path_info que guarda la ruta que se consulto
	# Limpiamos las barras "/" y armamos una lista para analizar la ruta más fácil
	# Ej: '/tasks/1' se convierte en ['tasks', '1']
	method = environ["REQUEST_METHOD"]
	path = environ["PATH_INFO"]
	parts = path.strip("/").split("/")

	#Metodo Get

	if method == "GET":

		#analiza si parts[0] es tasks
		if parts[0] == "tasks":

			#revisa si la longitud de parts es 1
			#guarda en body todas las tasks en formato json
			#configura la respuesta
			#codifica el body en utf-8
			if len(parts) == 1:


				body = json.dumps(tasks)

				start_response(
					"200 OK",
					[("Content-Type", "application/json")]
				)


				return [body.encode("utf-8")]

			#revisa si la longitud de parts es 2
			#guarda en task la tarea buscada	
			if len(parts) == 2:

				task = find_task(int(parts[1]))

				#Si la task no es none Retorna la task
				if task is not None:
					body = json.dumps(task)

					start_response(
						"200 OK",
						[("Content-Type", "application/json")]
					)

					return [body.encode("utf-8")]

				#Si la task Es None retorna un error	
				else:
					body = json.dumps({
						"error": "Task not found"
					})

					start_response(
						"404 Not Found",
						[("Content-Type", "application/json")]
					)
					return [body.encode("utf-8")]

	#Metodo Post
	#Revisa si la consulta fue a tasks
	#Guarda largo de la tarea nueva, decodifica tarea, guarda la informacion
	#Agrega key id con el value del next_id, configura Proximo id, agrega la tarea a tasks
	#Configura respuesta, retorna respuesta

	elif method == "POST":
		if parts[0] == "tasks":
			length = int(environ.get("CONTENT_LENGTH", 0))
			body = environ["wsgi.input"].read(length)
			body = body.decode("utf-8")
			data = json.loads(body)
			data["id"] = next_id
			next_id +=1
			tasks.append(data)
			start_response(
				"201 Created",
				[("Content-Type", "application/json")]
			)
			body = json.dumps(data)
			return [body.encode("utf-8")]

	#Metodo Patch, actualizacion parcial
	#Revisa que la consulta sea a tareas
	#Revisa si hay un id enviado en la consulta
	#obtiene el id de la tarea a actualizar
	#guarda informacion del body con los atributos a actualizar
	#busca la tarea a actualizar
	#Chequea si se encontro la tarea
	#Si la tarea No se encuentra responde con error
	#Sie la tarea se encuentra actualiza los valores
	elif method == "PATCH":
		if parts[0] == "tasks":
			if len(parts) == 2:

				id_task = int(parts[1])

				length = int(environ.get("CONTENT_LENGTH", 0))
				body = environ["wsgi.input"].read(length)
				body = body.decode("utf-8")

				updates = json.loads(body)

				item = find_task(id_task)

				if item is None:
					start_response(
						"404 Not Found",
						[("Content-Type", "application/json")]
					)
					
					body = json.dumps({
						"error": "Task not found"
					})

					return [body.encode("utf-8")]

				for key, value in updates.items():
					item[key] = value

				start_response(
					"200 OK",
					[("Content-Type", "application/json")]
				)

				body = json.dumps(item)

				return [body.encode("utf-8")]


	#Metodo Delete
	#Revisa que la ruta sea a tasks
	#revisa que tenga un id
	#busca la tarea
	#Si no encuentra la tarea retorna respuesta con error
	#Si la tarea existe borra la tarea del diccionario, retorna la respuesta sin la task
	elif method == "DELETE":
		if parts[0] == "tasks":
			if len(parts) == 2:
				id_task = int(parts[1])
				item = find_task(id_task)
				if item is None:
					start_response(
						"404 Not Found",
						[("Content-Type", "application/json")]
					)
					body = json.dumps({
						"error": "Task not found"
					})

					return [body.encode("utf-8")]

				tasks.remove(item)		
				
				start_response(
					"204 No Content",
					[]
				)

				return[b""]

#Importa de make_server
from wsgiref.simple_server import make_server

#Configuracion del servidor
server = make_server(
    "localhost",
    9292,
    application
)

#Mantener Servidor Escuchando
server.serve_forever()




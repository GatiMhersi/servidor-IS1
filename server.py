import json



tasks = []
next_id = 1

def find_task(task_id):
	for task in tasks:
		if task["id"] == task_id:
			return task
	return None

def application(environ, start_response):
	global next_id

	method = environ["REQUEST_METHOD"]
	path = environ["PATH_INFO"]
	parts = path.strip("/").split("/")

	if method == "GET":

		if parts[0] == "tasks":

			if len(parts) == 1:

				body = json.dumps(tasks)
				start_response(
					"200 OK",
					[("Content-Type", "application/json")]
				)
				return [body.encode("utf-8")]
			if len(parts) == 2:

				task = find_task(int(parts[1]))
				if task is not None:
					body = json.dumps(task)

					start_response(
						"200 OK",
						[("Content-Type", "application/json")]
					)

					return [body.encode("utf-8")]
				else:
					body = json.dumps({
						"error": "Task not found"
					})

					start_response(
						"404 Not Found",
						[("Content-Type", "application/json")]
					)
					return [body.encode("utf-8")]

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

from wsgiref.simple_server import make_server


server = make_server(
    "localhost",
    9292,
    application
)

server.serve_forever()




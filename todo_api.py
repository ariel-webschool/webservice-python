from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Liste de tâches (base de données en mémoire)
todos = [{"id":1,"title": "Cleaning the bathroom.","completed":False}]

class TodoHandler(BaseHTTPRequestHandler):
    # Méthode GET pour obtenir toutes les tâches
    def do_GET(self):
        if self.path == '/todos':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'todos': todos}).encode('utf-8'))
        elif self.path.startswith('/todos/'):
            try:
                todo_id = int(self.path.split('/')[-1])
                if todo_id < 0 or todo_id >= len(todos):
                    self.send_response(404)
                    self.wfile.write(json.dumps({'error': 'Todo not found'}).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'todo': todos[todo_id]}).encode('utf-8'))
            except (ValueError, IndexError):
                self.send_response(400)
                self.wfile.write(json.dumps({'error': 'Invalid ID'}).encode('utf-8'))

    # Méthode POST pour créer une nouvelle tâche
    def do_POST(self): # request (utilisateur envoie), response(serveur envoie)
        if self.path == '/todos':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8') # on recupere un json qui est en chaine de caractere
            try:
                data = json.loads(post_data) 
                title = data['title']
                todo = {
                    'id': len(todos), # derniere index ajoutee au tableau
                    'title': title,
                    'completed': False
                }
                todos.append(todo)
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.send_header('User', 'David')
                self.end_headers()
                self.wfile.write(json.dumps({'todo': todo}).encode('utf-8'))
            except (json.JSONDecodeError, KeyError):
                self.send_response(400)
                self.wfile.write(json.dumps({'error': 'Bad request'}).encode('utf-8'))

    # Méthode PUT pour mettre à jour une tâche
    def do_PUT(self):
        if self.path.startswith('/todos/'):
            try:
                todo_id = int(self.path.split('/')[-1])
                if todo_id < 0 or todo_id >= len(todos):
                    self.send_response(404)
                    self.wfile.write(json.dumps({'error': 'Todo not found'}).encode('utf-8'))
                    return
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(put_data)
                if 'title' in data:
                    todos[todo_id]['title'] = data['title']
                if 'completed' in data:
                    todos[todo_id]['completed'] = data['completed']
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'todo': todos[todo_id]}).encode('utf-8'))
            except (ValueError, json.JSONDecodeError):
                self.send_response(400)
                self.wfile.write(json.dumps({'error': 'Bad request'}).encode('utf-8'))

    # Méthode DELETE pour supprimer une tâche
    def do_DELETE(self):
        if self.path.startswith('/todos/'):
            try:
                todo_id = int(self.path.split('/')[-1])
                if todo_id < 0 or todo_id >= len(todos):
                    self.send_response(404)
                    self.wfile.write(json.dumps({'error': 'Todo not found'}).encode('utf-8'))
                    return
                todos.pop(todo_id)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({'result': True}).encode('utf-8'))
            except (ValueError, IndexError):
                self.send_response(400)
                self.wfile.write(json.dumps({'error': 'Invalid ID'}).encode('utf-8'))

# Configuration du serveur HTTP
def run(server_class=HTTPServer, handler_class=TodoHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting http server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

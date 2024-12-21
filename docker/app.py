from flask import Flask, jsonify, request
app = Flask(__name__)

tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Retrieve all tasks."""
    return jsonify(tasks), 200

@app.route('/tasks', methods=['POST'])
def add_task():
    """Add a new task"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Task name is required'}), 400
    new_task = {
        'id': len(tasks) + 1,
        'name': data['name'],
        'done': False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    data = request.get_json()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    task['name'] = data.get('name', task['name'])
    task['done'] = data.get('done', task['done'])
    return jsonify(task), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

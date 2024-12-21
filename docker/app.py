from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': '10.160.11.32',
    'user': 'todo_user',
    'password': 'D630@bynet',
    'database': 'tasks_db'
}

def get_db_connection():
    """Establish and return a database connection."""
    return mysql.connector.connect(**db_config)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Retrieve all tasks."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(tasks), 200

@app.route('/tasks', methods=['POST'])
def add_task():
    """Add a new task."""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Task name is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (data['name'],))
    conn.commit()
    new_task_id = cursor.lastrowid
    cursor.close()
    conn.close()

    new_task = {'id': new_task_id, 'name': data['name'], 'done': False}
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task."""
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    if not task:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Task not found'}), 404

    updated_name = data.get('name', task['name'])
    updated_done = data.get('done', task['done'])
    cursor.execute(
        "UPDATE tasks SET name = %s, done = %s WHERE id = %s",
        (updated_name, updated_done, task_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'id': task_id, 'name': updated_name, 'done': updated_done}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)


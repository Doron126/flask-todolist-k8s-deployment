## **flask-todolist-k8s-deployment**

# **Overview**
This is a simple To-Do List Application built using Python and Flask with a MySQL database for consistent and a DockerHub image for convinient, deployed with Kubernetes. 
The Kubernetes deployment file pull a DockerHub image of the app and supposed to deploy it across 2 pods and 2 nodes with pod anti-affinity rule for redundency.

# **Technologies used**
* Python
* Flask
* Docker
* k8s
* MySQL

# **Instructions**
1. Clone the deployment file
2. Set a Kubernetes cluster with 2 worker nodes.
3. Set a MySQL DB.
4. Apply the Kubernetes manifest.
5. Use the App using REST API.
   

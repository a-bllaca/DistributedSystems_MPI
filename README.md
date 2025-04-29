# DistributedSystems_MPI
Project for Distributed Systems , a system where a master process sends tasks to worker processes via Redis as a message queue

Use the following commands to deploy on minikube with docker locally:

--Build images 
docker build -t master:v6 ./master

docker build -t worker:v6 ./worker

docker build -t dashboard:v6 ./dashboard

--Load into minikube
minikube image load dashboard:v6

minikube image load master:v6

minikube image load worker:v6

--delete and apply the deploy yamls
kubectl delete -f k8s/

kubectl apply -f k8s/

--Check pod status
kubectl get pods

kubectl logs master 

kubectl get -l app=worker 

kubectl get services

minikube service dashboard-service --url

--make dashboard accessible through port 5000
kubectl port-forward deployment/dashboard 5000:5000

--Most important , mount this folder so that the project could store the files.
Mount data: minikube mount ./data/worker_outputs:/data

# Deploy với fix
helm install multi-agent-microservices ./src/helm

# Hoặc nếu đã có release, upgrade:
helm upgrade multi-agent-microservices ./src/helm

# Xem pods
kubectl get pods

# Xem deployment
kubectl get deployments

# Xem services
kubectl get services

# Check logs nếu pod không start
kubectl logs -l app.kubernetes.io/name=multi-agent-microservices
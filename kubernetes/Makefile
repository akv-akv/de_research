# minikube
minikube-start-docker:
	minikube start --driver=docker --cpus='4' --memory='6g'
minikube-delete:
	minikube delete
minikube-dashboard:
	minikube dashboard
minikube-ip:
	minikube ip

# Argo CD
argo-cd-install:
	kubectl create namespace argocd
	kubectl apply --namespace=argocd --filename=https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
argo-cd-get-password: # username: admin
	kubectl get secret argocd-initial-admin-secret --namespace=argocd --output=jsonpath="{.data.password}" | base64 -d && echo
argo-cd-ui:
	kubectl port-forward service/argocd-server --namespace=argocd 31026:443 &
argo-cd-login:
	$(eval ARGOCD_PASSWORD := $(shell kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo))
	argocd login localhost:31026 --username=admin --password=$(ARGOCD_PASSWORD) --insecure

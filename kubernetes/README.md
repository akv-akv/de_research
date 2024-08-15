# Local kubernetes cluster setup

- Run minikube `make minikube-start-docker`

- Go to argocd folder `cd argocd`

- Install ArgoCD using Kustomize `kustomize build | kubectl apply -f -`

- Add ArgoCD and RootApp applications to be managed by ArgoCD

`kubectl apply -f root-app.yaml -n argocd`
`kubectl apply -f argocd-app.yaml -n argocd`

- Login to ArgoCD - See commands in Makefile under ArgoCD section

- ArgoCD setup is completed and all apps from `./apps` will be loaded automatically

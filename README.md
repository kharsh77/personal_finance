# Personal Finance App

Walkthrough Video: https://www.loom.com/share/fd744f0fa86b4c189a0fcec7885bfb2a?sid=c4d374e7-547e-48fe-8d5a-cd2a2383210a

## Introduction
- A Python based personl finance app which helps to track income/expense transactions.
- The app supports multi-tenancy. A client can have isolation on how compute and storage happens on the app.

## Design Considerations
- The app uses flask framework to expose few apis and postgres for data storage.
- Kubernates is used to keep seggregation of compute and storage based on namespace.
- Different clients will have a separate base URL which is generated per namespace wise. This unique URL for each client would be used by their users.
- Compute and storage isolation would be maintained for each these URLs.
- The APIs are authenticated by JWT token.

# Technologies Used:
- Flask, Postgres, docker, Kubernates and github actions(CI/CD). AWS ECR for deploying image to cloud. AWS EKS for using cloud cluster (Few configurations established).
- Kubernates deployment has been tested locally using minukube. 

## APIs Exposed
- /register: This api registers a user into the app based on a username and password.
- /login: After registration, user can login using this API and get a access token for using other transaction APIs.
- /transaction: A user can add their transaction amount with details. A income or expense type of input is expected.
- /analytics: Based on the transactions added, a user can get current month or last month aggregated data.
- /heath: To check health status of service.
* we need to add access token generated from response of /login api to header `"x-access-token"` of /transaction & /analytics api.
* Postman Collection: https://www.postman.com/kharsh77/workspace/projects/request/1228171-53cf1988-0b32-4cd7-a520-344adbba4ef3

## Configure app based on cluster
- Remote:
- - Below are step to configure EKS. 
- - create cloudformation stack on aws 
- - update cluster.ymal file & update subnets from above setup of cloudformation stack
- - `eksctl create cluster -f cluster.yaml --kubeconfig=~/.kube/config`        
- Local (Minikube):
- - We need to start minikube and allow local docker repositories to be accessed by minikube.
- - `minikube start`
- - `eval $(minikube docker-env)`
- - `minikube addons enable registry`

## Update application docker image
- Remote: (ECR Registry)
- - We can use github action rule: `publish_image_to_ecr` 
- Locally
- -  `docker-compose build --no-cache`

## Add a new Tenant
- We have deployment setup for each tenant in `kubernates/<tenant-name>` folder.
- For adding a new tenant we need create a namespace for the tenant. The sample config file can be found in `kubernetes/<tenant-name>/dev-namespace.yaml` file.
- To apply a namespace we need to run `kubectl apply -f kubernetes/<tenant-name>/dev-namespace.yaml -n <tenant-name>`
- After creating a namespace, we can add apply all other configurations for that client by `kubectl apply -f kubernetes/<tenant-name>/. -n <tenant-name>`
- All other configurations has to setup only once while tenant onboarding in kubernates/<tenant-name> folder

- Remote: (EKS) [Pending]
- - We can use github action rule: `deploy_to_eks`
- - Due to lack to production level EKS cluster this functionality is not fully functional.
- Locally: (Minikube) 
- - Namespace for the tenant has to be active for deploying app for a tenant.
- - `kubectl apply -f kubernetes/<tenant-name>/. -n <tenant-name> `
- We will wait till all containers are RUNNING by using this command: `kubectl get po,svc -n <tenant-name>`
- - `minikube service app --url -n <tenant-name>` This command will output a specific URL which can be used via postman
- - Each tenant will have a separate url which can be accessed by their users.





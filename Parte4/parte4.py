from subprocess import call

call("kubectl create namespace cdps-18", shell=True)

call("kubectl apply -f productpage.yaml", shell=True)
call("kubectl apply -f details.yaml", shell=True)
call("kubectl apply -f reviews-svc.yaml", shell=True)
call("kubectl apply -f ratings.yaml", shell=True)
call("kubectl apply -f reviews-v1-deployment.yaml", shell=True)
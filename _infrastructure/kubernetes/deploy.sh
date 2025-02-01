#!/bin/bash
BASE_DIR="_infrastructure/kubernetes/manifests"

apply_if_exists() {
  [ -f "$1" ] && kubectl apply -f "$1"
}

kubectl apply -f "${BASE_DIR}/namespace.yml"

for component in postgres mongo redis celery django; do
  for file in "$BASE_DIR/$component"/*.yml; do
    apply_if_exists "$file"
  done
done

apply_if_exists "${BASE_DIR}/ingress.yml"

echo "All services deployed successfully in Minikube."

# AgentOps local infra — kind / docker only.
# Intentionally does NOT create AWS/GCP resources.

resource "local_file" "kind_config_copy" {
  content  = file("${path.module}/kind-config.yaml")
  filename = "${path.module}/generated/kind-config.yaml"
}

resource "local_file" "apply_hint" {
  filename = "${path.module}/generated/apply.sh"
  content  = <<-EOT
    #!/usr/bin/env bash
    set -euo pipefail
    CLUSTER="${var.cluster_name}"
    echo "Creating kind cluster $${CLUSTER} (no cloud bill)..."
    kind create cluster --name "$${CLUSTER}" --config "$(dirname "$0")/kind-config.yaml" || true
    kind load docker-image agentops-api:local --name "$${CLUSTER}" || true
    kubectl apply -k ../../../k8s/overlays/dev
    kubectl -n agentops rollout status deploy/agentops-api
  EOT
  file_permission = "0755"
}

resource "null_resource" "kind_cluster" {
  count = var.enable_kind_create ? 1 : 0

  triggers = {
    cluster = var.cluster_name
    config  = filesha256("${path.module}/kind-config.yaml")
  }

  provisioner "local-exec" {
    command = "kind create cluster --name ${var.cluster_name} --config ${path.module}/kind-config.yaml || kind get clusters | grep -q ${var.cluster_name}"
  }

  depends_on = [local_file.kind_config_copy]
}

resource "local_file" "kubeconfig_path_marker" {
  content  = "Run: kind get kubeconfig --name ${var.cluster_name} > kubeconfig\n"
  filename = var.kubeconfig_path
}

output "next_steps" {
  value = <<-EOT
    1. docker build -t agentops-api:local -f services/api/Dockerfile .
    2. terraform -chdir=infra/terraform apply  # writes generated scripts; set enable_kind_create=true to create cluster
    3. bash infra/terraform/generated/apply.sh
    4. kubectl -n agentops port-forward svc/agentops-api 8080:80
  EOT
}

output "cost" {
  value = "USD 0 — local kind/docker only; no cloud provider resources in this module."
}

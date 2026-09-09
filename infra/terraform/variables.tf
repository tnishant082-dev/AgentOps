variable "cluster_name" {
  description = "kind cluster name"
  type        = string
  default     = "agentops"
}

variable "kubeconfig_path" {
  description = "Where to write the generated kind kubeconfig hint file"
  type        = string
  default     = "${path.module}/generated/kubeconfig.path"
}

variable "enable_kind_create" {
  description = "If true, terraform null_resource will run kind create (requires kind + docker on the host)"
  type        = bool
  default     = false
}

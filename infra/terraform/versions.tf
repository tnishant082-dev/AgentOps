terraform {
  required_version = ">= 1.5.0"

  required_providers {
    # Local / null providers only — no AWS, GCP, or Azure.
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

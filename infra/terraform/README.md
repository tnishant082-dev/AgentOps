# Terraform (local / kind)

This module uses `local` and `null` providers only.

- **Does not** create AWS VPCs, EKS, ECR, S3, or anything billable.
- Writes helper scripts under `generated/` for kind apply.
- Set `enable_kind_create=true` only on a machine that has Docker + kind installed.

```bash
terraform init
terraform plan
terraform apply -var='enable_kind_create=false'
```

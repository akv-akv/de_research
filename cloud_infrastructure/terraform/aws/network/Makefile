terraform-plan:
	terraform plan --out=terraform_plan

terraform-apply:
	terraform apply terraform_plan

terraform-destroy:
	terraform destroy

infracost-login:
	infracost auth login

infracost-calculate:
	infracost breakdown --path .

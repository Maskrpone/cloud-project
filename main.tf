terraform {
	required_providers {
		github = {
			source = "integrations/github"
			version = "~> 6.0"
		}
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~>3.0"
    }
    random = {
      source = "hashicorp/random"
      version = "~>3.0"
    }
	}
}

provider "github" {
	token = var.github_token
}

provider "azurerm" {
  features {}
}

resource "github_repository" "repo" {
	name = var.repo_name
	description = "Cloud project"
	visibility = "public"
	auto_init = true
}

# Create the development branch from main
resource "github_branch" "dev" {
  repository    = github_repository.repo.name
  branch        = "dev"
  source_branch = "main"
}

# Lock main branch: Require PRs, no direct pushes
resource "github_branch_protection" "main" {
  repository_id = github_repository.repo.node_id
  pattern       = "main"
  enforce_admins = true

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    required_approving_review_count = 1
  }
}

resource "github_branch_protection" "dev" {
  repository_id = github_repository.repo.node_id
  pattern       = "dev"

  enforce_admins = true

  required_status_checks {
    strict = true # Force la branche features-* à être à jour avec la branche dev 
    contexts = []
  }

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    required_approving_review_count = 0 # Allows merge without review 
  }
}

resource "random_pet" "rg_name" {
  prefix = var.resource_group_name_prefix
}

resource "azurerm_resource_group" "rg" {
  name = random_pet.rg_name.id
  location = var.resource_group_location
}

resource "random_pet" "azurerm_mssql_server_name" {
  prefix = "cloud"
}

resource "random_password" "admin_password" {
  count = var.admin_password == null ? 1 : 0
  length = 20
  special = true
  min_numeric = 1
  min_upper = 1
  min_lower = 1
  min_special = 1
}

locals {
  admin_password = try(random_password.admin_password[0].result, var.admin_password)
}

resource "azurerm_mssql_server" "server" {
  name = random_pat.azurerm_mssql_server_name.id
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  administrator_login = var.admin_username
  administrator_login_password = local.admin_password
  version = "12.0"
}

resource "azurerm_mssql_database" "db" {
  name = var.sql_db_name
  server_id = azurerm_mssql_server.server.id
}


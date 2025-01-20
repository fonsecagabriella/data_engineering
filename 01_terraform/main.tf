terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = "keys/terra.json"
  project     = "peppy-plateau-447914-j6"
  region      = "us-central1"
}
resource "google_storage_bucket" "data-lake-bucket" {
  name          = "terraform-demo-imgabidotcom"
  location      = "US"

  # Optional, but recommended settings:
  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}


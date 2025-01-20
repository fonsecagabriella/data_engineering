# Intro To Terraform 🌎

Terraform is a tool used to *set up and manage infrastructure (like servers, databases, networks, etc.) in an automated and consistent way*.

**Instead of clicking around in a cloud provider's dashboard (like AWS, Azure, or Google Cloud), you write code to describe what you want, and Terraform makes it happen.**

---

## Index 👩🏽‍💻

1. [Set Up GCS First](#set-up-gcs-first)
2. [Useful to Know](#useful-to-know)
3. [Useful Commands](#useful-commands)
4. [Useful Terraform](#useful-terraform)
5. [Terraform Files](#files)
6. [Declarations](#declarations)
7. [Execution Steps](#execution-steps)

---

## Set Up GCS First
1. Go to Google Cloud, select your project.
2. Admin >> Service Account >> Create a Service Account.
3. Add all the services you will use via Terraform.

**To edit:**
1. Go to IAM, click on your service account.
2. Add/remove what you need from there.

---

## Useful to Know

- When you create a resource, you give first the name in local, then the name that will appear in Google Cloud.
- Under `name =` you need to have an exclusive name.

```terraform
resource "google_storage_bucket" "data-lake-bucket" {
  name     = "terraform-demo-imgabidotcom"
  location = "US"
}
```

- **Functions can only be called in the main file**

```terraform
# example of how to use a file
# default = file("./keys/my-creds.json")
```

- **Don't forget to destroy (in this course, at least 🥺)**

---

## Useful Commands

- `Init` - Get the providers that I need.
- `Plan` - What am I about to do?
- `Apply` - Do what is in the tf files.
- `Destroy` - Remove everything defined in the tf files.

---

## Useful Terraform

- `terraform fmt` / format .tf file

---

## Terraform Files

- `main.tf`: where your declaration goes
- `variables.tf`: you can set variables here, so others can set values in their own environments
- Optional: `resources.tf`, `output.tf`
- `.tfstate`

---

## Declarations

- `terraform`: configure basic Terraform settings to provision your infrastructure
  - `required_version`: minimum Terraform version to apply to your configuration.
  - `backend`: stores Terraform's "state" snapshots, to map real-world resources to your configuration.
    - `local`: stores state file locally as `terraform.tfstate`
  - `required_providers`: specifies the providers required by the current module.
- `provider`:
  - adds a set of resource types and/or data sources that Terraform can manage.
  - The Terraform Registry is the main directory of publicly available providers from most major infrastructure platforms.
- `resource`
  - blocks to define components of your infrastructure.
  - Project modules/resources: `google_storage_bucket`, `google_bigquery_dataset`, `google_bigquery_table`.
- `variable` & `locals`
  - runtime arguments and constants.

---

## Execution Steps

1. `terraform init`:
   - Initializes & configures the backend, installs plugins/providers, & checks out an existing configuration from a version control.
2. `terraform plan`:
   - Matches/previews local changes against a remote state, and proposes an Execution Plan.
3. `terraform apply`:
   - Asks for approval to the proposed plan, and applies changes to the cloud.
4. `terraform destroy`:
   - Removes your stack from the Cloud.


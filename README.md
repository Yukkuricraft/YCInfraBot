# YC Infra Bot
Lightweight discord bot for managing YC infra from Discord.

## What it Do
For now, it only handles starting, stopping, and checking status of the YC test sandbox.

## How it Set Up
We utilize infrastructure provisioned from the [terraform](../../../terraform) repository.

1. Upon pushing a change to this repo, a [GitHub Action](.github/workflows/build.yml) kicks off.
2. Once built, the image is uploaded to a GCR repository using the repo secret `GCP_SA_JSON_KEY`
3. GCP Compute Instance running COS will pull and run the image as a [systemd service](../../../blob/master/terraform/workspaces/yc-toolbox/templates/cloud-init.yml.tpl).
    a. TODO: Need to implement pyorouboros or watchtower for auto image updating

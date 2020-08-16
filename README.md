# YC Infra Bot
Lightweight discord bot for managing YC infra from Discord.

## What it Do
For now, it only handles starting, stopping, and checking status of the YC test sandbox.

## How it Set Up
We utilize infrastructure provisioned from the [terraform](../../../terraform) repository.

We also apply a [`.patch`](libcloud_gce_resume_suspend.patch) in the `Dockerfile`. Libcloud doesn't seem to support any beta gcp endpoints which compute instance `resume`/`suspend` endpoints are under. As such this patch changes the libcloud requests to hit the `beta` endpint + add functions for resuming and suspending. As a note, suspending is the equivalent of sleep/hibernating an instance as opposed to stopping it entirely.

1. Upon pushing a change to this repo, a [GitHub Action](.github/workflows/build.yml) kicks off.
2. Once built, the image is uploaded to a GCR repository using the repo secret `GCP_SA_JSON_KEY`
3. GCP Compute Instance running COS will pull and run the image as a [systemd service](../../../terraform/blob/master/workspaces/yc-toolbox/templates/cloud-init.yml.tpl).
    * TODO: Need to implement pyorouboros or watchtower for auto image updating

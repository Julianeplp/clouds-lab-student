# Phase 1 — Comparison Report

Copy this file to `submission/phase1_report.md`, fill in every answer slot, and commit it:

```bash
cp phase-1-echo-bot/report_template.md submission/phase1_report.md
```

**How to fill it in.** Each answer sits between a pair of `<!--answer:...-->` markers. Replace
the `TODO` line with your answer — **leave the markers themselves untouched**, they are how the
grader finds your answers. Anything you write outside the markers is ignored, so add extra
prose, tables or images freely.

Numbers must **match `submission/phase1_report.json`** exactly — that file is produced by
`measure.py` and is what your figures are checked against. Copy them across; do not retype from
memory.

---

## 1. Setup facts

**Your image size**, in MB, from `gcloud artifacts docker images list` (number only, e.g. `142`):

<!--answer:image_size_mb-->
204
<!--/answer-->

**The custom VPC and subnet you created** (names only):

<!--answer:vpc_name-->
echo-net
<!--/answer-->

<!--answer:subnet_name-->
echo-subnet
<!--/answer-->

---

## 2. Measurements

Copy these from `submission/phase1_report.json`. Cold is `cold_ms`; warm median is
`stats.median`. Numbers only, in milliseconds (e.g. `812.4`).

| Platform | Cold (ms) | Warm median (ms) |
|---|---|---|
| IaaS VM | <!--answer:vm_cold_ms-->252.4<!--/answer--> | <!--answer:vm_warm_median_ms-->211.1<!--/answer--> |
| Cloud Run | <!--answer:cloudrun_cold_ms-->657.9<!--/answer--> | <!--answer:cloudrun_warm_median_ms-->639.3<!--/answer--> |
| Cloud Function | <!--answer:function_cold_ms-->739.4<!--/answer--> | <!--answer:function_warm_median_ms-->639.5<!--/answer--> |

Include your histogram or plot of the warm distribution below (an image, or the ASCII chart
`measure.py` prints). This is read by a human, not the grader:

<!--answer:latency_plot-->
```text
Warm latency distribution (milliseconds)

Platform       Min     Median     P95     Max
VM             207.9   211.1      215.3   215.4
Cloud Run      124.5   639.3      683.6   684.8
Cloud Function 123.5   639.5      684.7   750.3

Median comparison:
VM             | ████████████████████ 211.1 ms
Cloud Run      | ████████████████████████████████████████████████████████ 639.3 ms
Cloud Function | ████████████████████████████████████████████████████████ 639.5 ms
```
<!--/answer-->

---

## 3. Per-platform analysis

**Scaling behaviour.** Imagine requests arriving one at a time, then ten at once, then a
hundred. For each of the three platforms, answer concretely:

- Does anything get created automatically to absorb the load — and if so, *what* exactly?
  (One platform here creates nothing at all.)
- What is the hard limit, and where does it come from — a flag you passed yourself, or the
  size of the machine you picked?

(~80 words. Your `--machine-type=e2-micro` and `--max-instances=3` are both concrete answers
to the second question.)

<!--answer:scaling_behaviour-->
On the VM, nothing is created automatically: the same container keeps running on the e2-micro machine. The limit mainly comes from the machine size. Cloud Run can automatically create several instances when traffic increases, with a limit of 3 instances set by --max-instances=3. The gen 2 Cloud Function can also create several instances automatically to handle requests. It runs on Cloud Run infrastructure.
<!--/answer-->

**Deployment effort.** What did you have to build, configure and maintain to get each of the
three running? (~100 words)

<!--answer:deployment_effort-->
For the VM, I created the network, subnet and firewall rules, then created the machine, installed Docker and started the container. The machine and its IP address also need to be maintained. For Cloud Run, I built and pushed the image, then created the service with port 8080 and public access. For the Cloud Function, I deployed the source code with main.py as the entry point. Cloud Run and the Function require less maintenance than the VM.
<!--/answer-->

---

## 4. Why do two of your three numbers look alike?

With Cloud Run and your Function both deployed, run `gcloud run services list` and paste the
**complete output** here, unedited:

<!--answer:run_services_list-->
```text
✔
SERVICE: echo
REGION: us-central1
URL: https://echo-1090829914449.us-central1.run.app
LAST DEPLOYED BY: service-1090829914449@gcf-admin-robot.iam.gserviceaccount.com
LAST DEPLOYED AT: 2026-10-14T17:37:16.000372Z

✔
SERVICE: echo-bot
REGION: us-central1
URL: https://echo-bot-1090829914449.us-central1.run.app
LAST DEPLOYED BY: juliane_phalippou@eurecom.fr
LAST DEPLOYED AT: 2026-10-14T17:32:31.718637Z
```
<!--/answer-->

Now explain what that output tells you about how your Function is actually being run, why its
cold start resembles Cloud Run's so closely, and what — if anything — genuinely differs between
the two deployment paths. (~120 words)

<!--answer:convergence_explanation-->
The list shows two Cloud Run services: echo-bot is my direct Cloud Run deployment, while echo is the service automatically created for the gen 2 Cloud Function. This explains why the Cloud Run and Function latencies are similar: both use container-based Cloud Run infrastructure and can start on demand. The deployment process is different: Cloud Run uses my Docker image directly, while the Function starts from source code and Google builds the image automatically.
<!--/answer-->

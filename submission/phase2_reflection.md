# Phase 2 — Reflection: where does parallelism stop helping?

Copy this file to `submission/phase2_reflection.md`, fill in every answer slot, and commit it:

```bash
cp phase-2-tiny-gpt/reflection_template.md submission/phase2_reflection.md
```

**How to fill it in.** Each answer sits between a pair of `<!--answer:...-->` markers. Replace
the `TODO` line with your answer — **leave the markers themselves untouched**, they are how the
grader finds your answers. Anything you write outside the markers is ignored, so add extra
prose, tables or your threading plot freely.

Numbers in section 1 must **match `submission/phase2_report.json`** — copy them across, do not
retype from memory; they are checked against it.

---

## 1. Your measurements

| | Value |
|---|---|
| Naive attention, ms (`attention.naive_ms`) | <!--answer:attn_naive_ms-->419.046<!--/answer--> |
| Vectorized attention, ms (`attention.vectorized_ms`) | <!--answer:attn_vectorized_ms-->1.208<!--/answer--> |
| CPU training, ms for 100 steps (`devices.cpu_ms`) | <!--answer:cpu_ms-->437578.1<!--/answer--> |
| GPU training, ms for 100 steps (`devices.gpu_ms`) | <!--answer:gpu_ms-->12753.8<!--/answer--> |
| Final training loss (`training.final_loss`) | <!--answer:final_loss-->1.455<!--/answer--> |

**The thread sweep.** Give your four timings from `threads` — 1, 2, 4 and 8 threads — and say
which count was fastest. (verbatim: the numbers, in order)

<!--answer:thread_sweep-->
1 thread : 4712.928 ms; 2 threads : 2167.307 ms; 4 threads : 2207.208 ms; 8 threads : 2419.466 ms. The fastest configuration was 2 threads.
<!--/answer-->

---

## 2. Intra-node parallelism, three ways

**Why vectorizing wins.** Both attention implementations do the same arithmetic and produce the
same result (the unit test checks that). Explain where the naive version's time actually goes,
and what the vectorized one does differently — in terms of the machine, not the Python.
(~70 words)

<!--answer:vectorization_why-->
The naive implementation is slower because it uses many Python loops, which take more time to execute. The vectorized version performs several calculations at once using optimized operations. This makes better use of the CPU and reduces execution time. In my experiment, the time decreased from 419.046 ms to 1.208 ms, making the vectorized version 346.89 times faster.
<!--/answer-->

**Where the thread curve flattens, and why.** Using your sweep: more threads stopped helping —
or started hurting — at some point. Say where, and give the reason. Your Colab runtime's vCPU
count is part of the answer; so is what the threads have to coordinate on. (~80 words)

<!--answer:threading_plateau-->
The best result was at 2 threads (2167.307 ms). Increasing to 4 threads slightly increased the time to 2207.208 ms, and 8 threads increased it further to 2419.466 ms. The curve therefore flattened after 2 threads. The Colab runtime had 2 vCPUs, so extra software threads did not add physical CPU capacity. Instead, they had to share cores and coordinate access to work and memory. Scheduling overhead, synchronization and contention can outweigh the benefit of additional threads.
<!--/answer-->

**What made the GPU faster.** The model, the data and the step count were identical; only the
device changed. Say what about a transformer training step suits a GPU, and name one workload
that would *not* see this speed-up. (~70 words)

<!--answer:gpu_why-->
Transformer training repeatedly performs large matrix multiplications and other tensor operations that can run across many elements in parallel. A GPU has many execution units and high memory bandwidth, so it can process this work much faster than the CPU. With the same model and 100 steps, my CPU took 437578.1 ms while the GPU took 12753.8 ms, about 34.31× faster. A small sequential task with frequent CPU–GPU transfers would not necessarily benefit.
<!--/answer-->

---

## 3. The question

**Where does parallelism stop helping, and why?** Pull the three experiments together. Your
answer should distinguish the *kinds* of limit you met — work that cannot be divided, hardware
you do not have, coordination that costs more than it saves, data that has to move — and say
which one bound each experiment. One concrete number from section 1 per claim. (~150 words)

<!--answer:parallelism_limit-->
Parallelism stops helping when the extra workers cannot usefully execute independent work, or when the cost of coordinating and moving data outweighs the computation saved. The attention experiment showed the benefit of exposing parallel work to optimized native operations: vectorization reduced latency from 419.046 ms to 1.208 ms (346.89×). However, even vectorized operations still have memory-access costs and dependencies, so speed-up cannot grow without limit.

The threading sweep showed a hardware and coordination limit. Performance improved from 4712.928 ms with 1 thread to 2167.307 ms with 2, but worsened to 2419.466 ms with 8. On a 2-vCPU runtime, more threads compete for the same cores and memory resources while adding scheduling and synchronization overhead.

Finally, GPU training reduced 100-step time from 437578.1 ms to 12753.8 ms (x34.31). The GPU benefits from large, parallel tensor operations, but serial work, kernel-launch overhead and CPU–GPU data transfers remain limits. For small workloads, those costs could erase the advantage.
<!--/answer-->

**What you would measure next.** One experiment this phase did not run that would sharpen the
answer, and what result would change your mind. (~50 words)

<!--answer:next_experiment-->
I would repeat the CPU–GPU comparison at several batch sizes, including very small batches, and separately measure data-transfer time. I expect the GPU advantage to shrink for small batches because launch and transfer overheads become more important. If the speed-up remained around 34× even for tiny batches, I would reconsider that explanation.
<!--/answer-->
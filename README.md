# ⭐ **Structural Primality**

**Reinterpreting Prime Numbers Through Structural Closure**

![GitHub stars](https://img.shields.io/github/stars/OMPSHUNYAYA/SSUM-Structural-Primality?style=flat&color=green)
![Open Standard](https://img.shields.io/badge/License-Open%20Standard-green?style=flat)

Deterministic • Exact Arithmetic • Finite Enumeration • Structural Metrics • Reproducible Analysis

---

## 🔎 **What Is Structural Primality?**

Structural Primality is a deterministic arithmetic experiment that studies how integers behave under bounded structural closure, rather than treating primality as a binary label.

Structural primes are definitionally identical to the classical primes; this framework adds observational metrics without changing classification.

Instead of asking only:

**“Is n divisible?”**

Structural Primality asks:

**“How does n behave with respect to bounded divisibility pressure?”**

The experiment evaluates every integer under strict, finite rules and records where closure occurs, how close it is, and how resistance to factorization is structured.

There are:

- no approximations  
- no probabilistic tests  
- no heuristic shortcuts  

Every classification and metric is explicitly computed and auditable.

---

## 🔗 **Quick Links**

### 📘 **Documentation**
- [Concept-Flyer_Structural-Primality_ver1.3.pdf](Concept-Flyer_Structural-Primality_ver1.3.pdf) — High-level concept overview
- [Structural-Primality_ver1.3.pdf](Structural-Primality_ver1.3.pdf) — Detailed reference and analysis
- [Quickstart.md](Quickstart.md) — How to run Structural Primality step by step

### 🧪 **Core Scripts**
- [structural_primality.py](structural_primality.py) — Core structural primality analysis engine
- [plot_structural_primality.py](plot_structural_primality.py) — Deterministic plotting and visualization

---

## 🎯 **Problem Statement — Primality as Structural Closure**

Classically, a prime is defined as an integer greater than 1 with no divisors other than 1 and itself.

This definition is:

- binary (prime / composite)  
- silent about how composites fail  
- non-informative about proximity to factorization  

Structural Primality reframes the problem:

**Given an integer `n >= 2`, does it structurally close under bounded divisors?**

---

## 📐 **Structural Closure Rule (Exact Arithmetic)**

For each integer `n >= 2`, define the bounded divisor set:

`D(n) = { d | 2 <= d <= floor(sqrt(n)) }`

A structural closure occurs if there exists a `d` such that:

`n mod d = 0`

Classification rule:

- if such a `d` exists → `n` is `COMPOSITE`  
- if no such `d` exists → `n` is `STRUCTURAL_PRIME`  

This preserves exact classical equivalence:

- all classical primes are structural primes  
- no composite is misclassified  

The difference is not correctness, but **structural observability**.

---

## 📊 **Structural Metrics (What Is Recorded)**

Structural Primality does not stop at classification.

For each integer, it records a structural footprint.

For composites:

- `closure_d` — smallest divisor causing closure  
- `closure_r` — remainder at closure (always `0`)  
- `closure_a` — normalized alignment measure  

For all integers:

- `closest_d` — nearest divisor candidate  
- `closest_band` — discretized structural proximity band  

---

## 📌 **IMPORTANT: Scope of `closest_*` Metrics**

By default, `closest_*` metrics and `closest_band` are computed only over a configurable signature set of small primes (default `<= 101`).

This is intentional and measures persistent structural pressure from foundational divisors.

For large `n`, this signature-based `closest_*` value is an approximation — the true minimal gap could arise from a larger divisor near `floor(sqrt(n))`.

To compute the exact minimal gap over all `d <= floor(sqrt(n))`, use:

`--full_closest`

Note:  
`--full_closest` performs a full bounded scan and is slower.

---

## 📊 **Structural Bands**

Proximity to closure is discretized into ordered bands:

`A, B, C, D, E, F`

Where:

- `A` = closest to closure  
- `F` = farthest from closure  

Band assignment is deterministic and derived directly from divisor proximity thresholds.

Structural primes occupy bands without closure, revealing resistance patterns.

---

## 📊 **Example Output Rows (Illustrative)**

Below is a small illustrative excerpt of row-level output  
(signature-based `closest_*`, default settings):

| n  | status             | closure_d | closest_d | closest_gap | closest_a | closest_band | notes                              |
|----|--------------------|-----------|-----------|-------------|-----------|--------------|------------------------------------|
| 2  | STRUCTURAL_PRIME   |           |           |             |           |              | base prime                         |
| 3  | STRUCTURAL_PRIME   |           |           |             |           |              | base prime                         |
| 4  | COMPOSITE          | 2         | 2         | 0           | 1.0       | A            | even closure                       |
| 5  | STRUCTURAL_PRIME   |           | 2         | 1           | 0.0       | D            | no closure up to floor(sqrt(n))    |
| 6  | COMPOSITE          | 2         | 2         | 0           | 1.0       | A            | even closure                       |
| 7  | STRUCTURAL_PRIME   |           | 3         | 1           | 0.333     | C            | no closure up to floor(sqrt(n))    |
| 9  | COMPOSITE          | 3         | 3         | 0           | 1.0       | A            | closure witness                    |

Note:  
For primes, `closest_*` values depend on signature settings or use of `--full_closest`.

---

## 📊 **Primary Result Metrics**

The experiment produces:

- exact prime / composite classification  
- closure depth distributions  
- structural band distributions  
- prime ratio by finite range (bucketed)  

All results are:

- discrete  
- deterministic  
- reproducible  
- finite  

---

## 📈 **Concrete Results Snapshot (Example: N = 100,000)**

**Classification integrity**

- Structural primes: 9592  
- Composites: 90407  

Matches classical prime counts exactly.

**Structural observations (default signature-based mode)**

- Band `A` dominates across integers  
- Structural primes concentrate primarily in Bands `B` and `C`  
- Higher bands are sparse and structurally significant  

Note: band concentration depends on whether signature-based `closest_*` or `--full_closest` is used.

**Closure depth behavior**

- `closure_d = 2` dominates (even numbers)  
- Higher closure depths decay rapidly  
- Distribution is heavy-tailed and non-uniform  

**Prime ratio by range**

- Evaluated in buckets of size 1000  
- Prime ratio decays smoothly with `n`  
- No discontinuities or anomalies introduced  

---

## 🧠 **Structural Insight**

Structural Primality reveals that:

- compositeness is not uniform  
- factorization pressure is hierarchical  
- primes are not randomly isolated  
- integers exist in structured proximity fields  

Primality is not merely absence of divisibility.  
**It is resistance to structural closure.**

---

## 🔁 **Determinism & Reproducibility**

Structural Primality guarantees:

- identical results across executions  
- independence from machine, OS, or execution order  
- explicit failure modes  
- no silent acceptance  

Given identical inputs:

`(max_n, engine, signature settings, bucket size)`

the same classifications, metrics, and plots are always produced.

---

## 🚫 **What Structural Primality Is Not**

Structural Primality is not:

- a new definition of prime numbers  
- a probabilistic primality test  
- a cryptographic substitute  
- a factorization shortcut  
- a performance benchmark  

It does not replace classical number theory.  
It extends observability without altering correctness.

---

## 🧭 **Why Structural Primality Matters**

Structural Primality introduces:

- measurable structure into arithmetic  
- geometry-like intuition in number theory  
- new axes for analyzing integers  

Potential impact areas include:

- mathematical education  
- structural number analysis  
- algorithm diagnostics  
- foundational arithmetic research  

It shows that even the most settled concepts can yield new insight when examined structurally.

---

## 📄 **Safety & Usage Notice**

This project is intended for:

- research  
- education  
- observation  
- structural analysis  

Not intended for:

- cryptography  
- security guarantees  
- real-time or safety-critical systems  

Failures are explicit.  
Silent errors are not allowed.

---

## 📄 **License — Open Standard (Structural Primality)**

Open Standard.

This project applies structural concepts inspired by **Shunyaya Structural Universal Mathematics (SSUM)**.  
Reference to SSUM is recommended for conceptual context but not mandatory.

Intended for research, education, and observation.

No warranty; use at your own risk.

---

## 🏷 **Topics**

structural-primality, number-theory, exact-arithmetic, deterministic-analysis,  
structural-metrics, finite-enumeration, reproducible-research, shunyaya, ssum

---

© The Authors of the Shunyaya Framework, Shunyaya Structural Universal Mathematics and Shunyaya Symbolic Mathematics   

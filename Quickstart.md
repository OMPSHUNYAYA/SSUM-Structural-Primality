⭐ **Structural Primality — Quickstart**

Deterministic • Exact Arithmetic • Structural Metrics • Reproducible Analysis

---

## **What You Need**

Structural Primality is intentionally minimal.

### **Requirements**

- Python 3.9+
- Standard library only (no external dependencies)

Everything is:

- deterministic  
- offline  
- reproducible  
- identical across machines  

No randomness.  
No approximation.  
No probabilistic inference.

---

## **Minimal Project Layout**

A minimal Structural Primality release contains:

/Structural_Primality  
&nbsp;&nbsp;structural_primality.py  
&nbsp;&nbsp;plot_structural_primality.py  

README.md  
Quickstart.md  

Optional outputs (generated):

/plots  
&nbsp;&nbsp;*.png  
&nbsp;&nbsp;REPORT.txt  

No build step.  
No compilation.  
No external libraries.

---

## **One-Minute Mental Model**

Structural Primality evaluates a strict arithmetic rule.

An integer is structurally prime if it does not close under bounded divisors.

For each integer `n >= 2`, divisors are tested only in the bounded range:

`2 <= d <= floor(sqrt(n))`

If any `d` satisfies:

`n mod d = 0`

then `n` structurally closes and is composite.

If no such `d` exists, `n` is a `STRUCTURAL_PRIME`.

This preserves exact classical correctness while exposing structural behavior.

---

## **IMPORTANT: Scope of `closest_*` Metrics**

By default, `closest_*` metrics and `closest_band` are computed only over a configurable signature set of small primes (default `<= 101`).

This is intentional.  
It measures persistent structural pressure from foundational divisors.

For large `n`, this signature-based `closest_*` value is an approximation — the true minimal gap could arise from a larger divisor near `floor(sqrt(n))`.

To compute the exact minimal gap over all `d <= floor(sqrt(n))`, use:

`--full_closest`

Note:  
`--full_closest` performs a full bounded scan and is slower.

---

## **Running the Core Analysis Script**

### **Step 1 — Run Structural Classification**

From the project directory:

`python structural_primality.py --max_n 100000 --engine spf --mode rows --out rows.tsv --fmt tsv`

This produces a row-level structural record for every integer from `2` to `max_n`.

Each row includes:

- classification (`STRUCTURAL_PRIME` / `COMPOSITE`)
- closure depth (if any)
- nearest divisor candidate (signature-based by default)
- structural proximity band

**Optional exact-nearest mode:**

`python structural_primality.py --max_n 20000 --engine spf --mode rows --out rows_full.tsv --fmt tsv --full_closest`

---

### **Step 2 — Generate Summary Statistics (Optional)**

`python structural_primality.py --max_n 100000 --engine spf --mode summary --out summary.tsv --fmt tsv`

(Summary statistics are also produced automatically when using `--mode both`.)

This produces:

- prime vs composite counts  
- structural band distributions  
- closure depth distributions  

---

## **Generating Structural Plots**

To visualize structural behavior:

`python plot_structural_primality.py --rows rows.tsv --fmt tsv --out_dir plots --bucket 1000`

This generates:

- status distribution  
- closest band distribution (all integers)  
- closest band distribution (structural primes)  
- composite closure depth histogram  
- prime ratio by bucket  

All plots are generated deterministically from `rows.tsv`.

Band assignment is deterministic and derived directly from divisor proximity thresholds.

---

## **Structural Metrics (What Is Being Measured)**

Structural Primality records how close an integer is to factorization, not just whether it factors.

Key metrics include:

- `closure_d` — smallest divisor causing closure (composites)
- `closest_d` — nearest divisor candidate (signature-based by default)
- `closest_band` — discretized proximity band (`A–F`)

Bands represent ordered structural proximity:

- `A` = closest to closure  
- `F` = farthest from closure  

Structural primes occupy bands without closure.

---

## **Determinism Guarantee**

For identical inputs:

`(max_n, engine, signature settings, bucket size)`

Structural Primality guarantees:

- identical classifications  
- identical closure depths  
- identical band assignments  
- identical plots  

There is no randomness, no hidden state, and no execution-order dependence.

---

## **What Structural Primality Is (and Is Not)**

Structural Primality is:

- an exact reinterpretation of primality  
- a structural observability framework  
- fully classically equivalent  

Structural Primality is not:

- a new definition of primes  
- a probabilistic primality test  
- a cryptographic primitive  
- a factorization shortcut  

It does not replace classical number theory.  
It reveals structure classical theory does not record.

---

## **What This Quickstart Does Not Do**

This quickstart does not:

- approximate prime densities  
- predict future primes  
- optimize factorization  
- infer results visually  

It evaluates only what is explicitly computed and certified.

---

## **One-Line Summary**

Structural Primality lets you deterministically analyze how integers resist or yield to factorization — revealing structural depth beneath classical primality, with exact arithmetic and zero ambiguity.

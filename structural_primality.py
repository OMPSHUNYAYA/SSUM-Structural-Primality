import argparse
import csv
import math
import sys


def band_from_a(a: float) -> str:
    x = abs(a)
    if x >= 0.90:
        return "A"
    if x >= 0.70:
        return "B"
    if x >= 0.50:
        return "C"
    if x >= 0.30:
        return "D"
    if x >= 0.10:
        return "E"
    return "F"


def clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def compute_hardness(closest_a, S_energy):
    if closest_a in ("", None) or S_energy in ("", None):
        return ""
    try:
        a_term = clamp01(abs(float(closest_a)))
        s_term = clamp01(1.0 / (1.0 + abs(float(S_energy))))
        return 0.7 * a_term + 0.3 * s_term
    except Exception:
        return ""


def sieve_spf(nmax: int):
    spf = list(range(nmax + 1))
    if nmax >= 0:
        spf[0] = 0
    if nmax >= 1:
        spf[1] = 1
    for i in range(2, int(nmax ** 0.5) + 1):
        if spf[i] == i:
            step = i
            start = i * i
            for j in range(start, nmax + 1, step):
                if spf[j] == j:
                    spf[j] = i
    return spf


def generate_sig_primes(sig_div_cap: int):
    if sig_div_cap < 2:
        return []
    spf = sieve_spf(sig_div_cap)
    primes = []
    for x in range(2, sig_div_cap + 1):
        if spf[x] == x:
            primes.append(x)
    return primes


def signature_for_n(n: int, sig_primes, limit_d: int):
    best = None
    g_list = []

    for d in sig_primes:
        if d > limit_d:
            break

        r = n % d

        if r == 0:
            return {
                "closest_d": d,
                "closest_r": 0,
                "closest_gap": 0,
                "closest_g": 0.0,
                "closest_a": 1.0,
                "closest_band": band_from_a(1.0),
                "S_min": 0.0,
                "S_avg": 0.0,
                "S_energy": 0.0,
            }

        gap = r if r <= (d - r) else (d - r)
        g = gap / d
        a = 1.0 - 2.0 * g

        g_list.append(g)

        if best is None or g < best[0]:
            best = (g, d, r, gap, a)

    if best is None:
        return {
            "closest_d": "",
            "closest_r": "",
            "closest_gap": "",
            "closest_g": "",
            "closest_a": "",
            "closest_band": "",
            "S_min": "",
            "S_avg": "",
            "S_energy": "",
        }

    S_min = min(g_list) if g_list else ""
    S_avg = (sum(g_list) / len(g_list)) if g_list else ""
    S_energy = (sum(x * x for x in g_list) / len(g_list)) if g_list else ""

    g, d, r, gap, a = best
    return {
        "closest_d": d,
        "closest_r": r,
        "closest_gap": gap,
        "closest_g": g,
        "closest_a": a,
        "closest_band": band_from_a(a),
        "S_min": S_min,
        "S_avg": S_avg,
        "S_energy": S_energy,
    }


def closest_full_for_n(n: int, limit_d: int):
    best = None
    for d in range(2, limit_d + 1):
        r = n % d
        if r == 0:
            return {
                "closest_d": d,
                "closest_r": 0,
                "closest_gap": 0,
                "closest_g": 0.0,
                "closest_a": 1.0,
                "closest_band": band_from_a(1.0),
            }
        gap = r if r <= (d - r) else (d - r)
        g = gap / d
        a = 1.0 - 2.0 * g
        if best is None or g < best[0]:
            best = (g, d, r, gap, a)
    if best is None:
        return {
            "closest_d": "",
            "closest_r": "",
            "closest_gap": "",
            "closest_g": "",
            "closest_a": "",
            "closest_band": "",
        }
    g, d, r, gap, a = best
    return {
        "closest_d": d,
        "closest_r": r,
        "closest_gap": gap,
        "closest_g": g,
        "closest_a": a,
        "closest_band": band_from_a(a),
    }


def write_rows(args, sig_div_cap: int):
    nmax = max(2, args.max_n)
    fmt = args.fmt.lower().strip()
    delim = "\t" if fmt == "tsv" else ","

    out_fp = None
    if args.out:
        out_fp = open(args.out, "w", newline="", encoding="utf-8")
        fp = out_fp
    else:
        fp = sys.stdout

    fields = [
        "n",
        "status",
        "closure_d",
        "closure_r",
        "closure_a",
        "closure_band",
        "closest_d",
        "closest_r",
        "closest_gap",
        "closest_g",
        "closest_a",
        "closest_band",
        "S_min",
        "S_avg",
        "S_energy",
        "hardness",
        "notes",
    ]

    w = csv.writer(fp, delimiter=delim)
    w.writerow(fields)

    sig_primes = generate_sig_primes(sig_div_cap)
    spf = sieve_spf(nmax) if args.engine == "spf" else None

    rows_written = 0

    for n in range(2, nmax + 1):
        if args.sample_every > 1 and (n % args.sample_every != 0):
            continue
        if args.max_rows > 0 and rows_written >= args.max_rows:
            break

        if n in (2, 3):
            row = [n, "STRUCTURAL_PRIME"] + [""] * 14 + ["", "base prime"]
            w.writerow(row)
            rows_written += 1
            continue

        if args.engine == "spf":
            if spf[n] == n:
                limit_d = int(math.isqrt(n))
                sig = signature_for_n(n, sig_primes, min(limit_d, sig_div_cap))
                closest = sig
                if args.full_closest:
                    closest = closest_full_for_n(n, limit_d)
                hardness = compute_hardness(closest["closest_a"], sig["S_energy"])
                if hardness != "" and args.hardness_invert:
                    hardness = 1.0 - hardness
                row = [
                    n,
                    "STRUCTURAL_PRIME",
                    "",
                    "",
                    "",
                    "",
                    closest["closest_d"],
                    closest["closest_r"],
                    closest["closest_gap"],
                    closest["closest_g"],
                    closest["closest_a"],
                    closest["closest_band"],
                    sig["S_min"],
                    sig["S_avg"],
                    sig["S_energy"],
                    hardness,
                    "no closure up to floor(sqrt(n))",
                ]
                w.writerow(row)
                rows_written += 1
            else:
                d = spf[n]
                row = [
                    n,
                    "COMPOSITE",
                    d,
                    0,
                    1.0,
                    band_from_a(1.0),
                    d,
                    0,
                    0,
                    0.0,
                    1.0,
                    band_from_a(1.0),
                    0.0,
                    0.0,
                    0.0,
                    "",
                    "closure witness (spf)",
                ]
                w.writerow(row)
                rows_written += 1
        else:
            if n % 2 == 0:
                row = [
                    n,
                    "COMPOSITE",
                    2,
                    0,
                    1.0,
                    band_from_a(1.0),
                    2,
                    0,
                    0,
                    0.0,
                    1.0,
                    band_from_a(1.0),
                    0.0,
                    0.0,
                    0.0,
                    "",
                    "even closure",
                ]
                w.writerow(row)
                rows_written += 1
                continue

            limit_d = int(math.isqrt(n))
            closure_d = 0
            for d in range(3, limit_d + 1, 2):
                if n % d == 0:
                    closure_d = d
                    break

            if closure_d:
                row = [
                    n,
                    "COMPOSITE",
                    closure_d,
                    0,
                    1.0,
                    band_from_a(1.0),
                    closure_d,
                    0,
                    0,
                    0.0,
                    1.0,
                    band_from_a(1.0),
                    0.0,
                    0.0,
                    0.0,
                    "",
                    "closure witness (trial)",
                ]
                w.writerow(row)
                rows_written += 1
            else:
                sig = signature_for_n(n, sig_primes, min(limit_d, sig_div_cap))
                closest = sig
                if args.full_closest:
                    closest = closest_full_for_n(n, limit_d)
                hardness = compute_hardness(closest["closest_a"], sig["S_energy"])
                if hardness != "" and args.hardness_invert:
                    hardness = 1.0 - hardness
                row = [
                    n,
                    "STRUCTURAL_PRIME",
                    "",
                    "",
                    "",
                    "",
                    closest["closest_d"],
                    closest["closest_r"],
                    closest["closest_gap"],
                    closest["closest_g"],
                    closest["closest_a"],
                    closest["closest_band"],
                    sig["S_min"],
                    sig["S_avg"],
                    sig["S_energy"],
                    hardness,
                    "no closure up to floor(sqrt(n))",
                ]
                w.writerow(row)
                rows_written += 1

    if out_fp:
        out_fp.close()

    return rows_written


def write_summary(args, sig_div_cap: int):
    nmax = max(2, args.max_n)
    spf = sieve_spf(nmax)
    sig_primes = generate_sig_primes(sig_div_cap)

    prime_count = 0
    composite_count = 0
    band_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}

    for n in range(2, nmax + 1):
        if n in (2, 3):
            prime_count += 1
            continue
        if spf[n] == n:
            prime_count += 1
            limit_d = int(math.isqrt(n))
            sig = signature_for_n(n, sig_primes, min(limit_d, sig_div_cap))
            closest = sig
            if args.full_closest:
                closest = closest_full_for_n(n, limit_d)
            b = closest["closest_band"]
            if b in band_counts:
                band_counts[b] += 1
        else:
            composite_count += 1

    out_fp = None
    if args.summary_out:
        out_fp = open(args.summary_out, "w", newline="", encoding="utf-8")
        fp = out_fp
    else:
        fp = sys.stdout

    w = csv.writer(fp, delimiter="\t")
    w.writerow(["metric", "value"])
    w.writerow(["prime_count", prime_count])
    w.writerow(["composite_count", composite_count])
    w.writerow([])
    w.writerow(["closest_band_distribution", "count"])
    for k in ["A", "B", "C", "D", "E", "F"]:
        w.writerow([k, band_counts[k]])

    if out_fp:
        out_fp.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max_n", type=int, default=50)
    ap.add_argument("--engine", type=str, default="spf", choices=["spf", "trial"])
    ap.add_argument("--mode", type=str, default="rows", choices=["rows", "summary", "both"])
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--summary_out", type=str, default="")
    ap.add_argument("--fmt", type=str, default="csv", choices=["csv", "tsv"])

    ap.add_argument("--full_closest", action="store_true")
    ap.add_argument("--hardness_invert", action="store_true")

    ap.add_argument("--sig_div_mode", type=str, default="fixed", choices=["fixed", "adaptive"])
    ap.add_argument("--sig_div_max", type=int, default=101)

    ap.add_argument("--sample_every", type=int, default=1)
    ap.add_argument("--max_rows", type=int, default=0)

    args = ap.parse_args()

    nmax = max(2, args.max_n)
    if args.sig_div_mode == "adaptive":
        sig_div_cap = min(args.sig_div_max, int(math.isqrt(nmax)))
    else:
        sig_div_cap = args.sig_div_max

    print("STRUCTURAL PRIMALITY RUN")
    print(f"max_n = {args.max_n}")
    print(f"engine = {args.engine}")
    print(f"sig_div_mode = {args.sig_div_mode}")
    print(f"sig_div_cap = {sig_div_cap}")
    print(f"full_closest = {int(args.full_closest)}")
    print(f"hardness_invert = {int(args.hardness_invert)}")

    rows_written = 0
    if args.mode in ("rows", "both"):
        rows_written = write_rows(args, sig_div_cap)
        if args.out:
            print(f"rows_written = {rows_written}")
            print(f"rows_out = {args.out}")
        else:
            print(f"rows_written = {rows_written}")

    if args.mode in ("summary", "both"):
        write_summary(args, sig_div_cap)
        if args.summary_out:
            print(f"summary_out = {args.summary_out}")

    if args.engine == "spf":
        spf = sieve_spf(nmax)
        primes = 0
        comps = 0
        for n in range(2, nmax + 1):
            if spf[n] == n:
                primes += 1
            else:
                comps += 1
        print(f"structural_primes = {primes}")
        print(f"composites = {comps}")


if __name__ == "__main__":
    main()

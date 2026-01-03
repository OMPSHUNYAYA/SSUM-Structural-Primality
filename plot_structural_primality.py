import os
import csv
import math
import argparse
from collections import defaultdict, Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def ensure_dir(p):
    if p and not os.path.isdir(p):
        os.makedirs(p, exist_ok=True)


def read_rows(path, fmt):
    rows = []
    if fmt == "tsv":
        delim = "\t"
    else:
        delim = ","

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delim)
        for r in reader:
            rows.append(r)
    return rows


def write_index(out_dir, items):
    p = os.path.join(out_dir, "INDEX.txt")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        for it in items:
            f.write(it + "\n")
    return p


def write_report(out_dir, lines):
    p = os.path.join(out_dir, "REPORT.txt")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        for line in lines:
            f.write(line + "\n")
    return p


def save_fig(path):
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def to_int(x):
    if x is None:
        return None
    try:
        if isinstance(x, int):
            return x
        s = str(x).strip()
        if s == "" or s.lower() == "na":
            return None
        if "." in s:
            s = s.split(".", 1)[0]
        return int(s)
    except Exception:
        return None


def to_float(x):
    if x is None:
        return None
    try:
        if isinstance(x, float):
            return x
        s = str(x).strip()
        if s == "" or s.lower() == "na":
            return None
        return float(s)
    except Exception:
        return None


def plot_status_distribution(rows, out_png):
    c = Counter()
    for r in rows:
        c[str(r.get("status", "")).strip()] += 1

    labels = list(c.keys())
    values = [c[k] for k in labels]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Status distribution (rows file)")
    plt.xlabel("status")
    plt.ylabel("count")
    save_fig(out_png)

    return c


def plot_closest_band_distribution_all(rows, out_png):
    c = Counter()
    for r in rows:
        c[str(r.get("closest_band", "")).strip() or "NA"] += 1

    labels = list(c.keys())
    values = [c[k] for k in labels]

    plt.figure()
    plt.bar(labels, values)
    plt.title("closest_band distribution (all rows)")
    plt.xlabel("closest_band")
    plt.ylabel("count")
    save_fig(out_png)

    return c


def plot_closest_band_distribution_primes(rows, out_png):
    c = Counter()
    for r in rows:
        if str(r.get("status", "")).strip() != "STRUCTURAL_PRIME":
            continue
        c[str(r.get("closest_band", "")).strip() or "NA"] += 1

    labels = list(c.keys())
    values = [c[k] for k in labels]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Closest band distribution (STRUCTURAL_PRIME)")
    plt.xlabel("closest_band")
    plt.ylabel("count")
    save_fig(out_png)

    return c


def plot_composite_closure_d_topk(rows, out_png, k=40):
    c = Counter()
    for r in rows:
        if str(r.get("status", "")).strip() != "COMPOSITE":
            continue
        d = to_int(r.get("closure_d"))
        if d is None:
            continue
        c[d] += 1

    items = c.most_common(k)
    xs = [str(a) for a, _ in items]
    ys = [b for _, b in items]

    plt.figure()
    plt.bar(xs, ys)
    plt.title(f"Top {k} closure_d (spf) among COMPOSITE")
    plt.xlabel("closure_d")
    plt.ylabel("count")
    save_fig(out_png)

    return items


def plot_prime_ratio_by_bucket(rows, out_png, bucket):
    # Compute prime ratio per bucket of n (bucket based on n-1 so bucket=1000 groups 1..1000, 1001..2000, ...)
    buckets = defaultdict(lambda: [0, 0])  # bucket_start -> [total, primes]
    for r in rows:
        n = to_int(r.get("n"))
        if n is None:
            continue
        eff_n = n - 1 if n > 0 else 0
        b = (eff_n // bucket) * bucket
        buckets[b][0] += 1
        if str(r.get("status", "")).strip() == "STRUCTURAL_PRIME":
            buckets[b][1] += 1

    if not buckets:
        plt.figure()
        plt.title(f"Prime ratio by bucket (bucket = {bucket})")
        plt.xlabel("bucket_start_n")
        plt.ylabel("prime_ratio_in_rows")
        save_fig(out_png)
        return []

    xs = []
    ys = []
    for b in sorted(buckets.keys()):
        total, primes = buckets[b]
        ratio = (primes / total) if total > 0 else 0.0
        xs.append(b)
        ys.append(ratio)

    plt.figure()

    # Tiny UX improvement: if the run is small and only produces a single bucket,
    # render a bar and set a sensible x-range/tick so the plot doesn't look "empty".
    if len(xs) == 1:
        x0 = xs[0]
        y0 = ys[0]
        plt.bar([x0], [y0], width=max(1, int(bucket * 0.8)))
        plt.xlim(x0 - bucket, x0 + bucket)
        plt.xticks([x0], [f"{x0}..{x0 + bucket - 1}"])
    else:
        plt.plot(xs, ys, marker="o")
        plt.xticks(xs, [f"{x}..{x + bucket - 1}" for x in xs], rotation=45, ha="right")

    plt.title(f"Prime ratio by bucket (bucket = {bucket})")
    plt.xlabel("bucket_start_n")
    plt.ylabel("prime_ratio_in_rows")
    plt.tight_layout()
    save_fig(out_png)

    return list(zip(xs, ys))


def plot_prime_pressure_closest_d_topk(rows, out_png, k=40):
    c = Counter()
    for r in rows:
        if str(r.get("status", "")).strip() != "STRUCTURAL_PRIME":
            continue
        d = to_int(r.get("closest_d"))
        if d is None:
            continue
        c[d] += 1

    items = c.most_common(k)
    xs = [str(a) for a, _ in items]
    ys = [b for _, b in items]

    plt.figure()
    plt.bar(xs, ys)
    plt.title(f"Top {k} closest_d exerting pressure on STRUCTURAL_PRIME")
    plt.xlabel("closest_d")
    plt.ylabel("count")
    save_fig(out_png)

    return items


def plot_prime_hardness_hist(rows, out_png):
    hs = []
    for r in rows:
        if str(r.get("status", "")).strip() != "STRUCTURAL_PRIME":
            continue
        h = to_float(r.get("hardness"))
        if h is None:
            continue
        hs.append(h)

    plt.figure()
    if hs:
        plt.hist(hs, bins=12)
    plt.title("Hardness distribution (STRUCTURAL_PRIME)")
    plt.xlabel("hardness")
    plt.ylabel("count")
    save_fig(out_png)

    return hs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True, help="rows file (csv/tsv) from structural_primality.py")
    ap.add_argument("--fmt", choices=["csv", "tsv"], default="tsv")
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--bucket", type=int, default=1000)
    ap.add_argument("--topk", type=int, default=40)
    args = ap.parse_args()

    print("STRUCTURAL PRIMALITY PLOT RUN")
    rows = read_rows(args.rows, args.fmt)
    print(f"rows_loaded = {len(rows)}")

    ensure_dir(args.out_dir)
    print(f"out_dir = {args.out_dir}")

    report_lines = []
    index_items = []

    p0 = os.path.join(args.out_dir, "00_status_distribution.png")
    c_status = plot_status_distribution(rows, p0)
    print(f"plot = {p0}")
    index_items.append(os.path.basename(p0))
    report_lines.append("00 Status distribution:")
    for k, v in sorted(c_status.items(), key=lambda kv: (-kv[1], kv[0])):
        report_lines.append(f"  {k}: {v}")
    report_lines.append("")

    p1 = os.path.join(args.out_dir, "01_closest_band_all.png")
    c_band_all = plot_closest_band_distribution_all(rows, p1)
    print(f"plot = {p1}")
    index_items.append(os.path.basename(p1))
    report_lines.append("01 Closest band distribution (all):")
    for k, v in sorted(c_band_all.items(), key=lambda kv: (-kv[1], kv[0])):
        report_lines.append(f"  {k}: {v}")
    report_lines.append("")

    p2 = os.path.join(args.out_dir, "02_prime_closest_band.png")
    c_band_prime = plot_closest_band_distribution_primes(rows, p2)
    print(f"plot = {p2}")
    index_items.append(os.path.basename(p2))
    report_lines.append("02 Closest band distribution (STRUCTURAL_PRIME):")
    for k, v in sorted(c_band_prime.items(), key=lambda kv: (-kv[1], kv[0])):
        report_lines.append(f"  {k}: {v}")
    report_lines.append("")

    p3 = os.path.join(args.out_dir, "03_composite_closure_d_topk.png")
    items_closure = plot_composite_closure_d_topk(rows, p3, k=args.topk)
    print(f"plot = {p3}")
    index_items.append(os.path.basename(p3))
    report_lines.append(f"03 Top {args.topk} closure_d among COMPOSITE:")
    for d, cnt in items_closure:
        report_lines.append(f"  d={d}: {cnt}")
    report_lines.append("")

    p4 = os.path.join(args.out_dir, "04_prime_ratio_by_bucket.png")
    points = plot_prime_ratio_by_bucket(rows, p4, bucket=args.bucket)
    print(f"plot = {p4}")
    index_items.append(os.path.basename(p4))
    report_lines.append(f"04 Prime ratio by bucket (bucket={args.bucket}):")
    for b, ratio in points:
        report_lines.append(f"  {b}..{b + args.bucket - 1}: {ratio:.6f}")
    report_lines.append("")

    p5 = os.path.join(args.out_dir, "05_prime_pressure_closest_d_topk.png")
    items_pressure = plot_prime_pressure_closest_d_topk(rows, p5, k=args.topk)
    print(f"plot = {p5}")
    index_items.append(os.path.basename(p5))
    report_lines.append(f"05 Top {args.topk} closest_d among STRUCTURAL_PRIME:")
    for d, cnt in items_pressure:
        report_lines.append(f"  d={d}: {cnt}")
    report_lines.append("")

    p6 = os.path.join(args.out_dir, "06_prime_hardness_hist.png")
    hs = plot_prime_hardness_hist(rows, p6)
    print(f"plot = {p6}")
    index_items.append(os.path.basename(p6))
    report_lines.append("06 Hardness histogram (STRUCTURAL_PRIME):")
    if hs:
        report_lines.append(f"  count={len(hs)}  min={min(hs):.6f}  avg={(sum(hs)/len(hs)):.6f}  max={max(hs):.6f}")
    else:
        report_lines.append("  (no hardness values)")
    report_lines.append("")

    index_path = write_index(args.out_dir, index_items)
    report_path = write_report(args.out_dir, report_lines)

    print(f"index = {index_path}")
    print(f"report = {report_path}")


if __name__ == "__main__":
    main()

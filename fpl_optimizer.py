import requests
import pandas as pd
import numpy as np
import cvxpy as cp
from collections import defaultdict
import json
import pandas as pd

def fetch_fpl_data():
    with open("fpl_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # Extract player list from the 'elements' key
    players = data['elements']  
    return pd.DataFrame(players)



def prepare_player_data(players):
    df = players[['id', 'web_name', 'now_cost', 'total_points', 'element_type']].copy()
    df['price_m'] = df['now_cost'] / 10
    df = df[df['total_points'] > 0].reset_index(drop=True)
    return df

def assign_price_brackets(df):
    bins = np.arange(4, 15.5, 0.5)
    labels = [f"{bins[i]}-{bins[i+1]}m" for i in range(len(bins) - 1)]
    df['price_bracket'] = pd.cut(df['price_m'], bins=bins, labels=labels, right=False)
    return df

def filter_top_players(df, top_n=20):
    return df.groupby(['element_type', 'price_bracket'], group_keys=False)\
             .apply(lambda x: x.sort_values('total_points', ascending=False).head(top_n))\
             .reset_index(drop=True)

def bracket_key(label):
    return float(label.split('-')[0].replace('m', '').strip())

def complete_team(df, existing_team):
    positions = [1, 2, 3, 4]
    pos_names = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}
    total_position = {1: 2, 2: 5, 3: 5, 4: 3}

    price_brackets = sorted(df['price_bracket'].dropna().unique(), key=bracket_key)

    cheapest_bracket_per_position = {
        p: min(df[df['element_type'] == p]['price_bracket'].dropna().unique(), key=bracket_key)
        for p in positions
    }

    current = {'starting': defaultdict(int), 'bench': defaultdict(int)}
    for k, v in existing_team.get('starting', {}).items():
        current['starting'][k] = v
    for k, v in existing_team.get('bench', {}).items():
        current['bench'][k] = v

    total_existing = {'starting': 0, 'bench': 0, 'overall': 0}
    position_counts = defaultdict(int)
    cost_used = 0.0

    for part in ['starting', 'bench']:
        for label, count in current[part].items():
            pos_name, price = label.split(' ', 1)
            price_val = bracket_key(price)
            pos_code = [k for k, v in pos_names.items() if v == pos_name][0]
            total_existing[part] += count
            total_existing['overall'] += count
            position_counts[pos_code] += count
            cost_used += count * price_val

    remaining_players = 15 - total_existing['overall']
    remaining_bench = 4 - total_existing['bench']
    if remaining_bench < 0:
        print("Too many bench players already.")
        return None

    x = {}
    avg_points, avg_prices = {}, {}
    for p in positions:
        for b in price_brackets:
            label = f"{pos_names[p]} {b}"
            if label in current['starting'] or label in current['bench']:
                continue
            group = df[(df['element_type'] == p) & (df['price_bracket'] == b)]
            if group.empty:
                continue
            k = (p, b)
            x[k] = cp.Variable(integer=True)
            avg_points[k] = group['total_points'].mean()
            avg_prices[k] = group['price_m'].mean()

    objective = cp.Maximize(cp.sum([avg_points[k] * x[k] for k in x]))
    constraints = [cp.sum([x[k] for k in x]) == remaining_players]

    for p in positions:
        existing = position_counts[p]
        remaining = total_position[p] - existing
        constraints.append(cp.sum([x[k] for k in x if k[0] == p]) == remaining)

    # Add constraint for bench count (add exactly remaining_bench players)
    bench_flags = {}
    for k in x:
        bench_flags[k] = True  # all eligible for bench

    bench_keys = [k for k in x if bench_flags[k]]
    constraints.append(cp.sum([x[k] for k in bench_keys]) >= remaining_bench)

    # Budget constraint
    constraints.append(cp.sum([avg_prices[k] * x[k] for k in x]) <= 100 - cost_used)

    for k in x:
        available = len(df[(df['element_type'] == k[0]) & (df['price_bracket'] == k[1])])
        constraints.append(x[k] >= 0)
        constraints.append(x[k] <= available)

    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.ECOS_BB)

    if problem.status not in ["optimal", "optimal_inaccurate"]:
        print("No optimal solution found.")
        return None

    result = defaultdict(int)
    for k in x:
        v = int(round(x[k].value.item()))
        if v > 0:
            label = f"{pos_names[k[0]]} {k[1]}"
            result[label] += v

    # Sort results by price ascending (cheapest first)
    label_prices = {
        label: bracket_key(label.split(" ", 1)[1]) for label in result
    }
    sorted_labels = sorted(result.items(), key=lambda x: label_prices[x[0]])
    bench_result = {}
    start_result = {}
    bench_position_counts = defaultdict(int)
    bench_total = 0

    # Count existing bench players per position
    for label, count in current['bench'].items():
        pos_name, _ = label.split(" ", 1)
        pos_code = [k for k, v in pos_names.items() if v == pos_name][0]
        bench_position_counts[pos_code] += count
        bench_total += count

    # Sort by price ascending (cheaper on bench first)
    label_prices = {label: bracket_key(label.split(" ", 1)[1]) for label in result}
    sorted_labels = sorted(result.items(), key=lambda x: label_prices[x[0]])

    for label, count in sorted_labels:
        pos_name, _ = label.split(" ", 1)
        pos_code = [k for k, v in pos_names.items() if v == pos_name][0]

        for _ in range(count):
            if bench_total < 4:
                # Check position limits including existing players
                if pos_code == 1 and bench_position_counts[1] < 1:
                    bench_result[label] = bench_result.get(label, 0) + 1
                    bench_position_counts[1] += 1
                    bench_total += 1
                elif pos_code in [2, 3, 4] and bench_position_counts[pos_code] < 2:
                    bench_result[label] = bench_result.get(label, 0) + 1
                    bench_position_counts[pos_code] += 1
                    bench_total += 1
                else:
                    # Position limit reached, assign to starting XI
                    start_result[label] = start_result.get(label, 0) + 1
            else:
                # Bench full, assign to starting XI
                start_result[label] = start_result.get(label, 0) + 1


    print("\n--- Starting XI Additions ---")
    for k, v in start_result.items():
        print(f"{k}: {v}")

    print("\n--- Bench Additions ---")
    for k, v in bench_result.items():
        print(f"{k}: {v}")

    return start_result, bench_result

def main():
    print("Fetching data...")
    players = fetch_fpl_data()
    df = prepare_player_data(players)

    df = assign_price_brackets(df)
    df = filter_top_players(df, top_n=10)
    
    existing_team = {
        "starting": {
            "DEF 4.0-4.5m": 2,
            "FWD 10-10.5m": 2
        },
        "bench": {
            "MID 6.0-6.5m": 1
        }
    }

    print("Optimizing remaining players...")
    result = complete_team(df, existing_team)
    if result:
        start_result, bench_result = result
        print("\n--- Summary of Additions ---")
        for k, v in start_result.items():
            print(f"{k}: {v}")
        for k, v in bench_result.items():
            print(f"{k}: {v}")

if __name__ == "__main__":
    main()

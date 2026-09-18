---
title: Pokemon API + Pandas Analysis
tags: [python, project, week4, pandas, api, roadmap]
created: 2026-09-18
status: in-progress
project: python-roadmap
---

# Pokemon API + Pandas Analysis

> [!summary] What this is
> Week 4 project (second half): pull real data from a public API and analyze it with Pandas. Uses [PokeAPI](https://pokeapi.co) — no auth required, no rate limit.

## Overview

A small pipeline that:
1. Fetches a list of Pokémon from a public REST API
2. Fetches full detail for each one
3. Extracts only the fields needed for analysis (discarding the rest — the raw API response is much larger than what we actually use)
4. Loads everything into a Pandas `DataFrame`
5. Cleans, filters, and aggregates the data

This mirrors the same shape as the [[Expense Tracker SQLite Migration|Expense Tracker]] project's SQL work — `groupby()` here does the same job as `GROUP BY` there, just against API data instead of a database.

## Project structure

```
src/
└── pandas_analysis/
    ├── __init__.py
    ├── api_calls.py       # fetches data from PokeAPI
    └── data_analysis.py    # cleans/filters/aggregates + main entry point
```

| File | Purpose |
|---|---|
| `api_calls.py` | Fetches the Pokémon list and detail records from PokeAPI, extracts only the fields needed |
| `data_analysis.py` | Loads the fetched data into a `DataFrame`, cleans/filters/aggregates it — **this is the main entry point** |

> [!note] No caching yet
> Every run hits the real API fresh — nothing fetched is saved between runs. PokeAPI's fair-use policy recommends caching locally to avoid unnecessary repeat requests — worth adding later, not yet implemented here.

## Data source

- **API:** [PokeAPI](https://pokeapi.co) — `GET https://pokeapi.co/api/v2/pokemon`
- **Auth:** none required
- **Rate limit:** none enforced, but be reasonable — don't hammer it in a tight loop

### Fields kept (decided during reconnaissance, not everything the API returns)

- `id`, `name`
- `height`, `weight`, `base_experience`
- `primary_type` (first entry of `types` only — some Pokémon are dual-type, simplified to one for this analysis)
- `hp`, `attack`, `special-attack`, `defense`, `special-defence`, `speed`

Everything else in the raw response (`moves`, `game_indices`, `held_items`, `forms`, ...) is discarded immediately after fetching — the full response is far larger than what's actually used.

## Setup

```bash
uv sync
```

## Usage

```bash
uv run src/pandas_analysis/data_analysis.py
```

## Analysis techniques covered

- [[Pandas Cleaning|Cleaning]]: `dropna`, `drop_duplicates`
- Filtering: boolean indexing (`df[df["attack"] > 100]`)
- Categorizing: using .astype('category')
- Aggregating: `groupby(...).mean()` — the Pandas equivalent of SQL `GROUP BY`

## Ideas that I might do (maybe)

- [ ] Ranking — `nlargest` / `nsmallest`
- [ ] Feature engineering — derived columns (e.g. total stats = `sum(axis=1)` across stat columns)
- [ ] Correlation — `.corr()` between numeric columns
- [ ] `value_counts()` for quick categorical sanity checks
- [ ] Local caching (see note above) — file-based or `requests-cache`
- [ ] Visualization — bar chart of average stats by type, scatter of height vs weight
- [ ] `pd.merge()` example — join against the `/type/{name}` endpoint for type-effectiveness data
- [ ] Export results to CSV/Excel for a shareable report
- [ ] Multi-column `groupby` (e.g. type + a `pd.cut()`-bucketed weight class)

## Related

- [[Python Roadmap]]
- [[Week 4 - SQL, Databases, Pandas]]
- [[Expense Tracker SQLite Migration]]

#python #pandas #api #week4
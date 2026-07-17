#!/usr/bin/env bash
# Week 11 autograder: static analysis only.
# The dashboards need a live Azure PostgreSQL connection and a running
# Metabase instance that CI cannot reach, so this checks file presence,
# code patterns, and metric-definition coverage for the Required tier.
# Required/Extra work (freshness panel, presentation, date filter) is reviewed
# by a teacher, not the autograder.
# Total points: 100. Passing score: 60.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
APP_DIR="$REPO_ROOT/week11-streamlit"

source "$SCRIPT_DIR/grader_lib.sh"

cat > "$SCRIPT_DIR/score.json" <<'INIT'
{"score": 0, "pass": false, "passingScore": 60}
INIT

score=0
PASSING=60

file_has_content() {
  local f="$1"
  [[ -s "$f" ]] || return 1
  local body
  body="$(grep -vE '^[[:space:]]*$' "$f" 2>/dev/null || true)"
  [[ -n "$body" ]] || return 1
  return 0
}

# Like grep, but strips '#'-comments first so a keyword mentioned only in a
# "# TODO: query fct_trips" guide comment doesn't count as real code.
pygrep() {
  sed -E 's/#.*$//' "$2" | grep -qE "$1"
}

# ── Level 1 (20 pts): required files exist ──────────────────────────────────
l1=0
required_files=(
  "README.md"
  "AI_ASSIST.md"
  "week11-streamlit/app.py"
  "week11-streamlit/pyproject.toml"
  "week11-streamlit/uv.lock"
  "week11-streamlit/metric_definitions.md"
)
missing=0
for f in "${required_files[@]}"; do
  if [[ -f "$REPO_ROOT/$f" ]]; then
    pass "found $f"
  else
    fail "missing required file: $f"
    missing=$((missing + 1))
  fi
done
if [[ "$missing" -eq 0 ]]; then
  l1=20
fi
score=$((score + l1))
pass "Level 1: required files ($l1/20 pts)"

# ── Level 2 (15 pts): secrets hygiene ───────────────────────────────────────
l2=0
app="$APP_DIR/app.py"

if [[ -f "$REPO_ROOT/.gitignore" ]] && grep -qE "^\.env$|^\.env\b" "$REPO_ROOT/.gitignore"; then
  l2=$((l2 + 5)); pass "root .gitignore excludes .env"
else
  fail "root .gitignore must exclude .env"
fi

if [[ -f "$APP_DIR/.env" ]]; then
  blocker "week11-streamlit/.env is committed -- run: git rm --cached week11-streamlit/.env, then rotate the Postgres password since it was pushed"
else
  l2=$((l2 + 5)); pass "week11-streamlit/.env not committed"
fi

if [[ -f "$app" ]] && grep -qE "postgresql://[^\"'[:space:]]*:[^\"'[:space:]]*@" "$app"; then
  blocker "app.py: hardcoded Postgres connection string with an inline password -- use os.environ/os.getenv instead, then rotate the password since it was pushed"
elif [[ -f "$app" ]]; then
  l2=$((l2 + 5)); pass "app.py: no hardcoded Postgres credentials found"
fi
score=$((score + l2))
pass "Level 2: secrets hygiene ($l2/15 pts)"

# ── Level 3 (25 pts): Streamlit app content ─────────────────────────────────
l3=0
if [[ -f "$app" ]]; then
  if pygrep "^import sqlalchemy|^from sqlalchemy|^import psycopg|^from psycopg" "$app"; then
    l3=$((l3 + 5)); pass "app.py: imports a Postgres driver (sqlalchemy or psycopg2)"
  else
    fail "app.py: no sqlalchemy or psycopg2 import found"
  fi

  if pygrep "os\.environ|os\.getenv" "$app"; then
    l3=$((l3 + 5)); pass "app.py: reads credentials from the environment"
  else
    fail "app.py: no os.environ/os.getenv call found -- credentials must come from the environment"
  fi

  if pygrep "raise NotImplementedError" "$app"; then
    fail "app.py: raise NotImplementedError still present -- the headline KPIs panel is not implemented"
  else
    if pygrep "\.metric\(" "$app"; then
      l3=$((l3 + 5)); pass "app.py: uses .metric() (st.metric or a st.columns() cell)"
    else
      fail "app.py: no .metric() call found -- Required tier needs at least one KPI"
    fi

    if pygrep "fct_trips" "$app"; then
      l3=$((l3 + 5)); pass "app.py: queries fct_trips"
    else
      fail "app.py: fct_trips not referenced -- the dashboard must read the Week 10 mart"
    fi
  fi

  if pygrep "@st\.cache_data" "$app"; then
    l3=$((l3 + 5)); pass "app.py: uses @st.cache_data"
  else
    fail "app.py: no @st.cache_data found -- database calls must be cached"
  fi
else
  fail "week11-streamlit/app.py missing -- cannot check app content"
fi
score=$((score + l3))
pass "Level 3: Streamlit app content ($l3/25 pts)"

# ── Level 4 (20 pts): metric definitions ────────────────────────────────────
l4=0
defs="$APP_DIR/metric_definitions.md"

if file_has_content "$defs"; then
  fields_ok=0
  for field in "Name" "Description" "Calculation" "Data source" "Refresh frequency"; do
    if grep -qi "$field" "$defs"; then
      fields_ok=$((fields_ok + 1))
    else
      fail "metric_definitions.md: field '$field' not found in any panel"
    fi
  done
  if [[ "$fields_ok" -eq 5 ]]; then
    l4=$((l4 + 10)); pass "metric_definitions.md: all five fields present"
  elif [[ "$fields_ok" -ge 3 ]]; then
    l4=$((l4 + 5)); warn "metric_definitions.md: only $fields_ok/5 fields found"
  fi

  # Count any H3 heading as a documented panel, so students who title
  # entries by metric name rather than "Panel N" still get credit.
  panel_count=$(grep -cE "^### " "$defs" 2>/dev/null || true)
  if [[ "$panel_count" -ge 4 ]]; then
    l4=$((l4 + 10)); pass "metric_definitions.md: $panel_count panels documented (>=4 expected: 3 Metabase + 1 Streamlit)"
  elif [[ "$panel_count" -ge 2 ]]; then
    l4=$((l4 + 5)); warn "metric_definitions.md: only $panel_count panel(s) documented (expected >=4)"
  else
    fail "metric_definitions.md: fewer than 2 panels documented"
  fi

  if grep -qi "TODO" "$defs"; then
    warn "metric_definitions.md: still contains TODO placeholders -- finish filling it in"
  fi
else
  fail "week11-streamlit/metric_definitions.md: empty"
fi
score=$((score + l4))
pass "Level 4: metric definitions ($l4/20 pts)"

# ── Level 5 (10 pts): README documents the Metabase dashboard ──────────────
l5=0
readme="$REPO_ROOT/README.md"
submission_section=""
if [[ -f "$readme" ]]; then
  submission_section="$(sed -n '/^## My submission/,/^## /p' "$readme" | sed '1d;$d')"
fi

if [[ -n "$submission_section" ]] && grep -qE "https?://" <<< "$submission_section" && ! grep -qxE "TODO" <<< "$submission_section"; then
  l5=$((l5 + 10)); pass "README.md: dashboard link present under 'My submission'"
elif find "$REPO_ROOT" -iname "*.png" -not -path "*/.git/*" | grep -q .; then
  l5=$((l5 + 10)); pass "README.md: screenshots present in repo"
else
  fail "README.md: no Metabase dashboard link or screenshots found under 'My submission'"
fi
score=$((score + l5))
pass "Level 5: Metabase dashboard documented ($l5/10 pts)"

# ── Level 6 (10 pts): AI log ─────────────────────────────────────────────────
l6=0
ai="$REPO_ROOT/AI_ASSIST.md"
if file_has_content "$ai"; then
  chars=$(wc -c < "$ai" | tr -d ' ')
  todo_lines=$(grep -cxE "TODO" "$ai" 2>/dev/null || true)
  if [[ "$chars" -ge 600 && "$todo_lines" -eq 0 ]]; then
    l6=$((l6 + 10)); pass "AI_ASSIST.md: filled (${chars} chars, no leftover TODO lines)"
  elif [[ "$chars" -ge 300 ]]; then
    l6=$((l6 + 5)); warn "AI_ASSIST.md: present but brief or has leftover TODOs (${chars} chars, ${todo_lines} TODO line(s))"
  else
    fail "AI_ASSIST.md: too brief (${chars} chars)"
  fi
else
  fail "AI_ASSIST.md: empty or still the raw template"
fi
score=$((score + l6))
pass "Level 6: AI assistance log ($l6/10 pts)"

# ── Final ─────────────────────────────────────────────────────────────────────
print_results "Week 11 Autograder"
write_score "$score" "$PASSING" "$SCRIPT_DIR/score.json"

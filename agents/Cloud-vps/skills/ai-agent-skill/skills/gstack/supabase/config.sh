#!/usr/bin/env bash
# Supabase project config for gstack telemetry
# These are PUBLIC keys — safe to commit (like Firebase public config).
# RLS denies all access to the anon key. All reads and writes go through
# edge functions (which use SUPABASE_SERVICE_ROLE_KEY server-side).
export GSTACK_SUPABASE_URL="${GSTACK_SUPABASE_URL:-}"
export GSTACK_SUPABASE_ANON_KEY="${GSTACK_SUPABASE_ANON_KEY:-}"

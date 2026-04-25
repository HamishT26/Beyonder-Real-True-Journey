create table if not exists trinity_v55_runs (
  id text primary key,
  phase text not null,
  status text not null,
  created_at timestamptz default now(),
  payload jsonb not null default '{}'::jsonb
);

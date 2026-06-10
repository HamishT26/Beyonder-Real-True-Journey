-- V48 non-production Neon mission-control scaffold.
-- Apply only after Neon account/project callability is proven.

create table if not exists mission_events (
  id bigserial primary key,
  phase text not null,
  lane text not null,
  status text not null,
  proof_path text,
  blocker text,
  created_at timestamptz not null default now()
);

create table if not exists swarm_slots (
  slot_number integer primary key,
  label text not null,
  continuity_state text not null,
  runtime_surface text,
  proof_gate text,
  created_at timestamptz not null default now()
);

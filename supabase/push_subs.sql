-- WorldLink phone alerts: one row per person with their phone's alert address.
create table if not exists public.push_subs (
  uid text primary key,
  sub jsonb not null,
  updated timestamptz default now()
);
alter table public.push_subs enable row level security;
-- no public policies on purpose: only the alerts function (service role) can read or write this table

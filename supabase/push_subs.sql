-- WorldLink phone alerts: one row per person with their phone's alert address.
create table public.push_subs as select ''::text as uid, '{}'::jsonb as sub, current_timestamp as updated where false;
alter table public.push_subs enable row level security;

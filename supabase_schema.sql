-- Run once in your own Supabase project's SQL editor.
create table if not exists public.becoming_records (
  user_id uuid not null references auth.users(id) on delete cascade,
  collection text not null,
  id text not null,
  payload jsonb not null,
  primary key (user_id, collection, id)
);
alter table public.becoming_records drop constraint if exists becoming_records_collection_check;
alter table public.becoming_records add constraint becoming_records_collection_check
check (collection in ('profile','tasks','events','checkins','reflections','learning','evidence','transactions','budgets','sessions','practice','reviews','coding','jobs'));
alter table public.becoming_records enable row level security;
revoke all on public.becoming_records from anon;
grant select, insert, update, delete on public.becoming_records to authenticated;
drop policy if exists "Own records only" on public.becoming_records;
create policy "Own records only" on public.becoming_records
for all to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

-- In Authentication > Users, create/invite your own user and set a password.
-- For a personal deployment, disable new public signups in Authentication settings.
-- Test: unauthenticated requests must not read rows; user A must not read user B's rows.

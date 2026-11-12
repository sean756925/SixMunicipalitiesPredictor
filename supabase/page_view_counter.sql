-- Permanent, privacy-safe page-view storage for the Streamlit dashboard.
-- Run this once in Supabase Dashboard > SQL Editor.

create table if not exists public.page_view_daily (
    day date primary key,
    views bigint not null default 0 check (views >= 0),
    updated_at timestamptz not null default now()
);

alter table public.page_view_daily enable row level security;
revoke all on table public.page_view_daily from anon, authenticated;

create or replace function public.record_page_view()
returns table(total_views bigint, today_views bigint)
language plpgsql
security definer
set search_path = public
as $$
declare
    local_day date := timezone('Asia/Taipei', now())::date;
begin
    insert into public.page_view_daily(day, views, updated_at)
    values (local_day, 1, now())
    on conflict (day) do update
       set views = public.page_view_daily.views + 1,
           updated_at = now();

    return query
    select
        coalesce(sum(v.views), 0)::bigint as total_views,
        coalesce(max(v.views) filter (where v.day = local_day), 0)::bigint as today_views
    from public.page_view_daily as v;
end;
$$;

revoke all on function public.record_page_view() from public;
grant execute on function public.record_page_view() to anon;

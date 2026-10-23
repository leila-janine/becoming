import html
import streamlit as st


def esc(text):
    return html.escape(str(text))


def style():
    """Keep custom content on the same palette as Streamlit's active native theme.

    Inherited colors update in the browser immediately when the native theme
    changes, including menus, charts, tables, and widgets. No second CSS theme.
    """
    st.markdown('''<style>
    :root {
      --b-card:color-mix(in srgb,currentColor 3%,transparent);
      --b-tint:color-mix(in srgb,currentColor 7%,transparent);
      --b-border:color-mix(in srgb,currentColor 24%,transparent);
    }
    .block-container {max-width:1250px;width:100%;padding:4.75rem clamp(1rem,3vw,2.75rem) 4rem;box-sizing:border-box;}
    h1,h2,h3 {letter-spacing:-.025em;line-height:1.4!important;overflow-wrap:anywhere;}
    h1 {font-family:Georgia,serif!important;font-weight:400!important;font-size:clamp(2rem,4vw,3.3rem)!important;line-height:1.25!important;padding:.15em 0 .3em!important;}
    h2 {font-size:1.45rem!important;} h3 {font-size:1.15rem!important;}
    /* Do not reset stColumn min-width: Streamlit uses it to stack columns. */
    [data-testid="stMain"],[data-testid="stVerticalBlock"],[data-testid="stElementContainer"] {min-width:0;max-width:100%;}
    [data-testid="stHorizontalBlock"] {container-type:inline-size;container-name:becoming-row;}
    @container becoming-row (max-width:640px) {
      [data-testid="stColumn"] {width:100%!important;min-width:100%!important;flex:1 1 100%!important;}
    }
    .eyebrow {font-size:.75rem;letter-spacing:.13em;text-transform:uppercase;font-weight:650;margin-bottom:.7rem;line-height:1.6;}
    .brand {font:400 2rem/1.4 Georgia,serif;letter-spacing:-.05em;margin:.5rem 0 0;}
    .brand-sub {font-size:.75rem;letter-spacing:.09em;text-transform:uppercase;margin:0 0 1.5rem;line-height:1.7;}
    .hero {border:1px solid var(--b-border);background:var(--b-card);border-radius:24px;padding:1.8rem 145px 1.8rem 2rem;position:relative;margin:.6rem 0 1.5rem;overflow:visible;}
    .hero h1 {margin:.25rem 0 .6rem;max-width:100%;}
    .hero p {max-width:680px;line-height:1.75;margin-bottom:0;}
    .sprig {position:absolute;right:22px;top:28px;width:95px;height:120px;opacity:.55;}
    .stat {border-top:1px solid var(--b-border);padding:1rem 0;margin:.2rem 0 .8rem;}
    .stat .number {font:400 2rem/1.5 Georgia,serif;overflow-wrap:anywhere;}
    .stat .label {font-size:.86rem;line-height:1.7;}
    .card {background:var(--b-card);border:1px solid var(--b-border);border-radius:17px;padding:1.15rem 1.3rem;margin-bottom:.8rem;overflow-wrap:anywhere;}
    .card .meta {font-size:.77rem;letter-spacing:.035em;margin-bottom:.55rem;line-height:1.7;}
    .card h3 {margin:0 0 .5rem;padding:.1rem 0!important;}
    .card p {margin:0;line-height:1.75;}
    .tag {display:inline-block;background:var(--b-tint);border-radius:20px;padding:.3rem .7rem;font-size:.78rem;margin-right:.3rem;line-height:1.6;}
    .gentle {background:var(--b-tint);border-radius:15px;padding:1rem 1.25rem;margin:.7rem 0 1.2rem;line-height:1.75;overflow-wrap:anywhere;}
    .timeline {border-left:2px solid var(--b-border);padding:.4rem 0 .8rem 1.2rem;margin-left:.5rem;}
    .timeline .time {font-size:.82rem;letter-spacing:.02em;line-height:1.7;}
    .timeline strong {font-weight:600;} .timeline p {margin:.15rem 0;font-size:.95rem;line-height:1.65;}
    .timer-face {font:400 clamp(3rem,10vw,6rem)/1.35 Georgia,serif;letter-spacing:.03em;font-variant-numeric:tabular-nums;margin:.5rem 0;}
    .hero,.card,.gentle,.stat,.timeline {box-sizing:border-box;max-width:100%;}
    [data-testid="stMetricValue"] {font-size:clamp(1.4rem,3vw,2rem);line-height:1.4;white-space:normal;overflow:visible;text-overflow:clip;overflow-wrap:anywhere;}
    [data-testid="stMetricLabel"] {height:auto;min-height:1.5rem;}
    [data-testid="stMetricLabel"] p {white-space:normal;line-height:1.5;overflow-wrap:anywhere;}
    [data-testid="stDataFrame"],[data-testid="stVegaLiteChart"],[data-testid="stCode"] {max-width:100%;min-width:0;}
    [data-testid="stCode"] pre {max-width:100%;overflow-x:auto;}
    [data-testid="stMarkdownContainer"] p,[data-testid="stCaptionContainer"] {overflow-wrap:anywhere;}
    [data-testid="stForm"] {box-sizing:border-box;max-width:100%;}
    input,textarea,[data-baseweb="select"] {font-size:1rem!important;min-width:0;}
    .st-key-compact_navigation {display:none!important;}
    [data-testid="stSidebar"] button[kind="tertiary"] {justify-content:flex-start;text-align:left;border-radius:.6rem;padding:.45rem .65rem;}
    [data-testid="stSidebar"] button[kind="tertiary"]:hover {background:var(--b-tint);color:inherit;}
    [data-testid="stSidebar"] button[kind="tertiary"]:focus-visible {outline:2px solid currentColor;outline-offset:2px;}
    [data-testid="stSidebar"] button[kind="tertiary"] strong {text-decoration:underline;text-underline-offset:.35rem;}
    [data-testid="stButton"] button,[data-testid="stDownloadButton"] button,[data-testid="stFormSubmitButton"] button,a[data-testid="stBaseLinkButton"] {min-height:44px;height:auto;}
    [data-testid="stButton"] button p,[data-testid="stDownloadButton"] button p,[data-testid="stFormSubmitButton"] button p,a[data-testid="stBaseLinkButton"] p {white-space:normal;overflow-wrap:anywhere;line-height:1.5;}
    [data-testid="stWidgetLabel"] p {white-space:normal;overflow-wrap:anywhere;line-height:1.6;}
    [data-testid="stExpander"] summary p {white-space:normal;overflow-wrap:anywhere;line-height:1.6;}
    .stTabs {max-width:100%;min-width:0;}
    .stTabs [data-baseweb="tab-list"] {gap:.75rem;flex-wrap:nowrap;max-width:100%;overflow-x:auto;overflow-y:hidden;scrollbar-width:thin;}
    .stTabs [data-baseweb="tab"] {height:auto;min-height:48px;padding:.7rem .3rem;white-space:nowrap;line-height:1.5;flex:0 0 auto;}
    .stTabs [data-baseweb="tab"] p {white-space:nowrap;line-height:1.5;}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {color:inherit!important;font-weight:650;}
    [role="radiogroup"] label {min-height:36px;}
    .summary-table {width:100%;border-collapse:collapse;table-layout:fixed;font-size:.92rem;}
    .summary-table th,.summary-table td {text-align:left;vertical-align:top;padding:.8rem;border-bottom:1px solid var(--b-border);overflow-wrap:anywhere;}
    .summary-table th {font-weight:600;background:var(--b-tint);}
    .summary-wrap {max-width:100%;margin:.5rem 0 1rem;}
    @media(max-width:1024px) {
      [data-testid="stHorizontalBlock"] {gap:1rem!important;}
      [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {width:100%!important;min-width:100%!important;max-width:100%;flex:1 1 100%!important;}
      [data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"] {display:none!important;}
      [data-testid="stMain"] {margin-left:0!important;}
      .st-key-compact_navigation {display:flex!important;}
      .block-container {padding:4.25rem 1.5rem calc(3rem + env(safe-area-inset-bottom,0px));}
      .hero {padding:1.5rem;border-radius:18px;}
      .sprig {display:none;}
      .stat {padding:.6rem 0;margin:0 0 .3rem;}
      .stat .number {font-size:1.65rem;}
      .summary-table,.summary-table tbody,.summary-table tr,.summary-table td {display:block;width:100%;box-sizing:border-box;}
      .summary-table thead {position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip-path:inset(50%);}
      .summary-table tr {padding:.35rem .85rem;margin-bottom:.75rem;border:1px solid var(--b-border);border-radius:14px;background:var(--b-card);}
      .summary-table td {display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:.75rem;padding:.65rem 0;}
      .summary-table td:last-child {border-bottom:0;}
      .summary-table td::before {content:attr(data-label);font-size:.85rem;font-weight:600;}
      .stTabs [data-baseweb="tab-list"] {gap:.65rem;}
      .stTabs [data-baseweb="tab"] {font-size:.9rem;}
    }
    @media(max-width:480px) {
      .block-container {padding:4rem max(1rem,env(safe-area-inset-left,0px)) calc(3rem + env(safe-area-inset-bottom,0px)) max(1rem,env(safe-area-inset-right,0px));}
      h1 {font-size:clamp(1.85rem,7.5vw,2.25rem)!important;}
      .hero,.card {padding:1.1rem;}
      .gentle {padding:1rem;}
      [data-testid="stForm"] {padding:.85rem;}
      [data-testid="stButton"] button,[data-testid="stDownloadButton"] button,[data-testid="stFormSubmitButton"] button,a[data-testid="stBaseLinkButton"] {width:100%;min-height:48px;}
      [data-testid="stButton"],[data-testid="stDownloadButton"],[data-testid="stFormSubmitButton"] {width:100%;}
      .eyebrow,.brand-sub {letter-spacing:.06em;}
    }
    @media(prefers-reduced-motion:reduce) {* {scroll-behavior:auto!important;transition:none!important;animation:none!important;}}
    </style>''', unsafe_allow_html=True)


def hero(eyebrow, title, description):
    st.markdown(f'''<section class="hero"><div class="eyebrow">{esc(eyebrow)}</div><h1>{esc(title)}</h1><p>{esc(description)}</p><svg class="sprig" viewBox="0 0 100 140" aria-hidden="true"><path d="M45 135 Q62 80 48 15 M52 90 Q20 85 18 57 Q46 52 54 79 M52 65 Q80 53 83 28 Q55 26 50 54 M48 38 Q26 28 30 8 Q48 9 48 38" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></section>''',unsafe_allow_html=True)


def card(title, body, meta=''):
    st.markdown(f'<div class="card"><div class="meta">{esc(meta)}</div><h3>{esc(title)}</h3><p>{esc(body)}</p></div>',unsafe_allow_html=True)


def gentle(text):
    st.markdown(f'<div class="gentle">{esc(text)}</div>',unsafe_allow_html=True)


def stat(value, label):
    st.markdown(f'<div class="stat"><div class="number">{esc(value)}</div><div class="label">{esc(label)}</div></div>',unsafe_allow_html=True)


def summary_table(frame, money_columns=()):
    """Small read-only summaries become labelled cards on phones/tablets."""
    headings=''.join(f'<th scope="col">{esc(c)}</th>' for c in frame.columns)
    rows=[]
    for row in frame.to_dict('records'):
        cells=[]
        for column in frame.columns:
            value=f'₱{float(row[column]):,.2f}' if column in money_columns else str(row[column])
            cells.append(f'<td data-label="{esc(column)}">{esc(value)}</td>')
        rows.append('<tr>'+''.join(cells)+'</tr>')
    st.markdown('<div class="summary-wrap"><table class="summary-table" role="table"><thead><tr>'+headings+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>',unsafe_allow_html=True)

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
    .block-container {max-width:1250px;padding-top:4.75rem;padding-bottom:4rem;}
    h1,h2,h3 {letter-spacing:-.025em;line-height:1.4!important;overflow-wrap:anywhere;}
    h1 {font-family:Georgia,serif!important;font-weight:400!important;font-size:clamp(2rem,4vw,3.3rem)!important;line-height:1.25!important;padding:.15em 0 .3em!important;}
    h2 {font-size:1.45rem!important;} h3 {font-size:1.15rem!important;}
    .stColumn,[data-testid="stColumn"],[data-testid="stVerticalBlock"] {min-width:0;}
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
    [data-testid="stButton"] button,[data-testid="stDownloadButton"] button,[data-testid="stFormSubmitButton"] button,a[data-testid="stBaseLinkButton"] {min-height:44px;height:auto;}
    [data-testid="stButton"] button p,[data-testid="stDownloadButton"] button p,[data-testid="stFormSubmitButton"] button p,a[data-testid="stBaseLinkButton"] p {white-space:normal;overflow-wrap:anywhere;line-height:1.5;}
    [data-testid="stWidgetLabel"] p {white-space:normal;overflow-wrap:anywhere;line-height:1.6;}
    [data-testid="stExpander"] summary p {white-space:normal;overflow-wrap:anywhere;line-height:1.6;}
    .stTabs [data-baseweb="tab-list"] {gap:.75rem;}
    .stTabs [data-baseweb="tab"] {height:auto;min-height:48px;padding:.7rem .3rem;white-space:normal;line-height:1.5;}
    .stTabs [data-baseweb="tab"] p {white-space:normal;line-height:1.5;}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {color:inherit!important;font-weight:650;}
    [role="radiogroup"] label {min-height:36px;}
    @media(max-width:700px) {
      .block-container {padding:4rem 1rem 3rem;}
      .hero {padding:1.3rem;}
      .sprig {display:none;}
      .card {padding:1rem;}
      .eyebrow,.brand-sub {letter-spacing:.06em;}
      .stTabs [data-baseweb="tab-list"] {gap:.4rem;}
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

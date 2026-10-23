import html
import streamlit as st


def esc(text):
    return html.escape(str(text))


def style(dark=False):
    if dark:
        bg, card, soft, text, muted, border, accent, tint = '#211F1D','#2B2825','#34302C','#F3EDE4','#C2B7AA','#4B443C','#D5BDA7','#373D34'
    else:
        bg, card, soft, text, muted, border, accent, tint = '#F8F5F0','#FFFDFA','#EEE8DF','#302B26','#6B6259','#DDD4C8','#78614F','#E6EBE1'
    st.markdown(f'''<style>
    :root {{ --b-bg:{bg}; --b-card:{card}; --b-soft:{soft}; --b-text:{text}; --b-muted:{muted}; --b-border:{border}; --b-accent:{accent}; --b-tint:{tint}; }}
    .stApp, [data-testid="stAppViewContainer"] {{background:var(--b-bg); color:var(--b-text);}}
    [data-testid="stHeader"] {{background:var(--b-bg);}}
    [data-testid="stSidebar"] {{background:var(--b-soft);border-right:1px solid var(--b-border);}}
    .block-container {{max-width:1250px;padding-top:2rem;padding-bottom:4rem;}}
    h1,h2,h3 {{color:var(--b-text)!important;letter-spacing:-.035em;}}
    h1 {{font-family:Georgia,serif!important;font-weight:400!important;font-size:clamp(2rem,4vw,3.3rem)!important;}}
    h2 {{font-size:1.45rem!important;}} h3 {{font-size:1.15rem!important;}}
    p,li,label,[data-testid="stMarkdownContainer"],.stCaption {{color:var(--b-text);}}
    a {{color:var(--b-accent)!important;text-decoration:underline;text-underline-offset:3px;}}
    [data-testid="stCaptionContainer"] p {{color:var(--b-muted)!important;}}
    .eyebrow {{font-size:.72rem;letter-spacing:.17em;text-transform:uppercase;color:var(--b-muted);font-weight:650;margin-bottom:.6rem;}}
    .brand {{font:400 2rem Georgia,serif;letter-spacing:-.07em;margin:.5rem 0 0;}}
    .brand-sub {{font-size:.72rem;letter-spacing:.13em;text-transform:uppercase;color:var(--b-muted);margin:0 0 1.8rem;}}
    .hero {{border:1px solid var(--b-border);background:var(--b-card);border-radius:24px;padding:2rem 2.2rem;position:relative;overflow:hidden;margin:.6rem 0 1.5rem;}}
    .hero h1 {{max-width:85%;margin:.25rem 0 .8rem;padding:0;}}
    .hero p {{max-width:630px;line-height:1.7;color:var(--b-muted);margin-bottom:0;}}
    .sprig {{position:absolute;right:26px;top:24px;width:110px;height:130px;opacity:.35;color:var(--b-accent);}}
    .stat {{border-top:1px solid var(--b-border);padding:1rem 0;margin:.2rem 0 .8rem;}}
    .stat .number {{font:400 2rem Georgia,serif;line-height:1.3;}}
    .stat .label {{color:var(--b-muted);font-size:.8rem;}}
    .card {{background:var(--b-card);border:1px solid var(--b-border);border-radius:17px;padding:1.15rem 1.3rem;margin-bottom:.8rem;}}
    .card .meta {{font-size:.73rem;color:var(--b-muted);letter-spacing:.06em;margin-bottom:.55rem;}}
    .card h3 {{margin:0 0 .5rem;padding:0;}} .card p {{margin:0;line-height:1.65;}}
    .tag {{display:inline-block;background:var(--b-tint);border-radius:20px;padding:.25rem .7rem;font-size:.73rem;color:var(--b-text);margin-right:.3rem;}}
    .gentle {{background:var(--b-tint);border-radius:15px;padding:1rem 1.25rem;margin:.7rem 0 1.2rem;line-height:1.65;}}
    .timeline {{border-left:2px solid var(--b-border);padding:.4rem 0 .8rem 1.2rem;margin-left:.5rem;}}
    .timeline .time {{font-size:.78rem;letter-spacing:.03em;color:var(--b-muted);}}
    .timeline strong {{font-weight:600;}} .timeline p {{margin:.15rem 0;font-size:.92rem;}}
    div.stButton>button,div.stDownloadButton>button {{border-radius:10px;min-height:44px;border-color:var(--b-border);background:var(--b-card);color:var(--b-text);}}
    div.stButton>button[kind="primary"],div.stFormSubmitButton>button[kind="primary"] {{background:var(--b-accent);color:{'#211F1D' if dark else '#FFFDFA'};border-color:var(--b-accent);}}
    div.stButton>button:hover,div.stDownloadButton>button:hover {{border-color:var(--b-accent);color:var(--b-text);}}
    button:focus-visible,a:focus-visible,input:focus-visible {{outline:3px solid var(--b-accent)!important;outline-offset:3px!important;}}
    [data-testid="stVerticalBlockBorderWrapper"]>div {{border-color:var(--b-border)!important;border-radius:16px;}}
    [data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stDateInput"] input,[data-testid="stTimeInput"] input {{background:var(--b-card)!important;color:var(--b-text)!important;caret-color:var(--b-text);}}
    [data-baseweb="select"]>div {{background:var(--b-card)!important;color:var(--b-text)!important;}}
    [data-baseweb="popover"],[data-baseweb="menu"] {{background:var(--b-card)!important;color:var(--b-text)!important;}}
    [data-testid="stExpander"] {{background:var(--b-card);border-color:var(--b-border);}}
    [data-testid="stAlert"] {{background:var(--b-soft)!important;color:var(--b-text)!important;border-color:var(--b-border)!important;}}
    [data-testid="stProgressBar"] [role="progressbar"]>div {{background:var(--b-accent)!important;}}
    .stTabs [data-baseweb="tab-list"] {{gap:1rem;flex-wrap:wrap;}}
    .stTabs [data-baseweb="tab"] {{color:var(--b-text);min-height:44px;}}
    [data-testid="stMetricValue"] {{color:var(--b-text);}}
    [role="radiogroup"] label {{min-height:36px;}}
    hr {{border-color:var(--b-border)!important;}}
    @media(max-width:700px) {{.block-container {{padding:1.2rem 1rem 3rem;}} .hero {{padding:1.4rem;}} .hero h1 {{max-width:100%;}} .sprig {{display:none;}} .stTabs [data-baseweb="tab-list"] {{gap:.3rem;}} }}
    @media(prefers-reduced-motion:reduce) {{* {{scroll-behavior:auto!important;transition:none!important;animation:none!important;}}}}
    </style>''', unsafe_allow_html=True)


def hero(eyebrow, title, description):
    st.markdown(f'''<section class="hero"><div class="eyebrow">{esc(eyebrow)}</div><h1>{esc(title)}</h1><p>{esc(description)}</p><svg class="sprig" viewBox="0 0 100 140" aria-hidden="true"><path d="M45 135 Q62 80 48 15 M52 90 Q20 85 18 57 Q46 52 54 79 M52 65 Q80 53 83 28 Q55 26 50 54 M48 38 Q26 28 30 8 Q48 9 48 38" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></section>''',unsafe_allow_html=True)


def card(title, body, meta=''):
    st.markdown(f'<div class="card"><div class="meta">{esc(meta)}</div><h3>{esc(title)}</h3><p>{esc(body)}</p></div>',unsafe_allow_html=True)


def gentle(text):
    st.markdown(f'<div class="gentle">{esc(text)}</div>',unsafe_allow_html=True)


def stat(value, label):
    st.markdown(f'<div class="stat"><div class="number">{esc(value)}</div><div class="label">{esc(label)}</div></div>',unsafe_allow_html=True)

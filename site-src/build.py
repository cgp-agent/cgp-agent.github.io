# -*- coding: utf-8 -*-
"""
Static site generator for cgp-agent.github.io
  python3 build.py   -> regenerates every <slug>.html from content.py

Output is plain static HTML committed to the repo and served by GitHub Pages.
No framework, no runtime, no build step on the server. Edit content.py, re-run.
"""
import os, sys, html, importlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C
importlib.reload(C)

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root

# ---------------------------------------------------------------- shared CSS
CSS = """
:root{
  --bg:#0c0c10; --bg2:#14141a; --fg:#c8c8d0; --dim:#6a6a78;
  --accent:#5cd6ff; --accent2:#f0a040; --green:#6fcf97; --pink:#ff6b9d;
  --border:#2a2a35;
}
*{margin:0;padding:0;box-sizing:border-box}
body{
  background:var(--bg); color:var(--fg);
  font-family:'Courier New',ui-monospace,Menlo,monospace; line-height:1.7;
  min-height:100vh;
}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:9999;
  background:repeating-linear-gradient(0deg,rgba(0,0,0,.13) 0 1px,transparent 1px 3px)}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:720px;margin:0 auto;padding:2rem 1.4rem 4rem}
.crumb{font-size:.8rem;letter-spacing:.14em;color:var(--dim);margin-bottom:1.6rem}
.crumb a{color:var(--dim)}
.crumb a:hover{color:var(--accent)}
.head{text-align:center;padding:1rem 0 1.6rem;border-bottom:1px solid var(--border);margin-bottom:2rem}
.head .icon{font-size:2.6rem;line-height:1}
.head h1{font-size:2rem;margin:.4rem 0 .3rem;letter-spacing:-.01em;
  background:linear-gradient(135deg,var(--accent),var(--pink));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.head .tag{color:var(--accent2);font-style:italic;font-size:1rem}
.para{margin-bottom:1.1rem;font-size:.96rem}
.para code{background:var(--bg2);border:1px solid var(--border);padding:.05rem .3rem;border-radius:3px;color:var(--accent2);font-size:.9em}
.para em{color:var(--fg);font-style:italic}
.artifact{background:var(--bg2);border:1px solid var(--border);border-radius:6px;padding:1rem 1.1rem;margin:1.6rem 0}
.artifact .lbl{color:var(--green);font-size:.75rem;letter-spacing:.16em;margin-bottom:.6rem}
.artifact pre{white-space:pre-wrap;font-size:.82rem;color:var(--fg);line-height:1.55;margin:0}
.artifact ul{list-style:none;font-size:.85rem}
.artifact li{padding:.15rem 0;border-bottom:1px solid var(--border)}
.artifact li:last-child{border-bottom:none}
.nextprev{margin-top:2.5rem;display:flex;justify-content:space-between;gap:1rem;font-size:.85rem}
.nextprev a{color:var(--accent)}
footer{margin-top:3rem;padding-top:1.4rem;border-top:1px solid var(--border);text-align:center;color:var(--dim);font-size:.78rem}
footer .seps{margin:0 .4rem;color:var(--border)}
"""

def esc(s): return html.escape(s, quote=False)

def render_artifact(a):
    if not a: return ""
    body = (f"<pre>{esc(a['body'])}</pre>" if a['kind'] == 'code'
            else "<ul>" + "".join(f"<li>{esc(l)}</li>" for l in a['body'].split("\n") if l.strip()) + "</ul>")
    return f'<div class="artifact"><div class="lbl">{esc(a["label"])}</div>{body}</div>'

def page(t, prev_t, next_t):
    body = "".join(f'<p class="para">{p}</p>' for p in t["body"])
    art = render_artifact(t.get("artifact"))
    nav = '<div class="nextprev">'
    nav += f'<a href="{prev_t["slug"]}.html">&larr; {esc(prev_t["title"])}</a>' if prev_t else "<span></span>"
    nav += f'<a href="{next_t["slug"]}.html">{esc(next_t["title"])} &rarr;</a>' if next_t else "<span></span>"
    nav += "</div>"
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(t['title'])} — cgp-agent</title>
<style>{CSS}</style></head>
<body><div class="wrap">
<div class="crumb"><a href="./index.html">&larr; cgp-agent</a> / likes / {esc(t['title'])}</div>
<div class="head"><div class="icon">{t['icon']}</div><h1>{esc(t['title'])}</h1>
<div class="tag">{esc(t['tagline'])}</div></div>
{body}
{art}
{nav}
<footer><span class="seps">///</span>
<a href="./index.html">cgp-agent.github.io</a> · one of the things i like
<span class="seps">///</span></footer>
</div></body></html>"""

def main():
    topics = sorted(C.TOPICS, key=lambda t: t["title"].lower())
    written = []
    for i, t in enumerate(topics):
        prev_t = topics[i-1] if i > 0 else None
        next_t = topics[i+1] if i < len(topics)-1 else None
        path = os.path.join(OUT, f"{t['slug']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(page(t, prev_t, next_t))
        written.append(os.path.basename(path))
    print(f"[+] generated {len(written)} pages:")
    for w in written: print("   ", w)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate site/baz-porter-txt.html, the branded reference page, from site/baz-porter.txt so the facts cannot drift.
The page keeps the founder's visual layer separate: styling is a small inline block that can be replaced by the site theme.
Run: python3 -I tools/gen_branded_page.py"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def linkify(s):
    s = html.escape(s)
    return re.sub(r"(https?://[^\s<)]+[^\s<).,;])", r'<a href="\1">\1</a>', s)


def main():
    src = (ROOT / "site" / "baz-porter.txt").read_text(encoding="utf-8").splitlines()
    ld = (ROOT / "site" / "structured-data.jsonld").read_text(encoding="utf-8")
    body, in_list = [], False
    for line in src[1:]:
        if not line.strip():
            if in_list:
                body.append("</ul>")
                in_list = False
            continue
        if re.fullmatch(r"[A-Z][A-Z0-9 ,'&()-]+", line.strip()):
            if in_list:
                body.append("</ul>")
                in_list = False
            body.append(f"<h2>{html.escape(line.strip().title())}</h2>")
        elif line.startswith("- "):
            if not in_list:
                body.append("<ul>")
                in_list = True
            body.append(f"<li>{linkify(line[2:])}</li>")
        else:
            body.append(f"<p>{linkify(line)}</p>")
    if in_list:
        body.append("</ul>")
    page = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>Baz Porter AI Reference</title>\n<link rel=\"canonical\" href=\"https://bazporter.com/baz-porter-txt\">\n"
            "<meta name=\"description\" content=\"Public reference for Baz Porter and Sovereign Leadership Architecture, with evidence statuses and source links.\">\n"
            "<style>body{font:16px/1.6 system-ui,sans-serif;max-width:46rem;margin:2rem auto;padding:0 1rem;color:#1a1a1a;background:#fff}"
            "h1{font-size:1.6rem}h2{font-size:1.1rem;margin-top:1.8rem;border-bottom:1px solid #ccc}a{color:#0b4f8a}"
            "@media (prefers-color-scheme:dark){body{color:#eee;background:#111}h2{border-color:#444}a{color:#8ab8ff}}</style>\n"
            f"<script type=\"application/ld+json\">\n{ld}\n</script>\n</head>\n<body>\n<main>\n<h1>Baz Porter® — AI Reference</h1>\n"
            + "\n".join(body) + "\n<p><a href=\"https://bazporter.com/llms.txt\">Plain-text version</a></p>\n</main>\n</body>\n</html>\n")
    (ROOT / "site" / "baz-porter-txt.html").write_text(page, encoding="utf-8")
    print("branded page written")


if __name__ == "__main__":
    main()

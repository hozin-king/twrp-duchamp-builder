import sys, urllib.request, json
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request
job_id = sys.argv[1]
out = sys.argv[2]
class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None
opener = urllib.request.build_opener(NoRedir)
req = urllib.request.Request(
    f"https://api.github.com/repos/hozin-king/twrp-duchamp-builder/actions/jobs/{job_id}/logs",
    headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "muse-github-skill"},
)
add_surrogate_to_request(req, "custom.github", entry_name="access_token", allowed_hosts=["api.github.com"])
try:
    resp = opener.open(req, timeout=120)
    body = resp.read()
    print("direct status", resp.status, "len", len(body))
    open(out, "wb").write(body)
except urllib.error.HTTPError as e:
    loc = e.headers.get("Location")
    print("redirect", e.code, "->", (loc or "")[:120])
    if loc:
        req2 = urllib.request.Request(loc, headers={"User-Agent": "muse-github-skill"})
        with urllib.request.urlopen(req2, timeout=300) as r2:
            body = r2.read()
            print("downloaded", len(body), "bytes")
            open(out, "wb").write(body)

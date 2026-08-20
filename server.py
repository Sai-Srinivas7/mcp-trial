import httpx
from mcp.server import MCPServer

mcp = MCPServer("GitHub Lab")

GH = "https://api.github.com"


@mcp.tool()
async def get_repo(owner: str, repo: str) -> dict:
    """Get summary info for a GitHub repository: description, stars, language, last push."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{GH}/repos/{owner}/{repo}")
    if r.status_code == 404:
        raise ValueError(f"No repo {owner}/{repo}. Check the spelling.")
    r.raise_for_status()
    d = r.json()
    return {
        "full_name": d["full_name"],
        "description": d["description"],
        "stars": d["stargazers_count"],
        "language": d["language"],
        "pushed_at": d["pushed_at"],
    }


@mcp.tool()
async def recent_commits(owner: str, repo: str, limit: int = 5) -> list[str]:
    """List the most recent commit messages on a repository's default branch."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{GH}/repos/{owner}/{repo}/commits", params={"per_page": limit})
    r.raise_for_status()
    return [c["commit"]["message"].splitlines()[0] for c in r.json()]


@mcp.resource("github://{owner}/{repo}/readme")
async def readme(owner: str, repo: str) -> str:
    """The raw README of a repository."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.get(
            f"{GH}/repos/{owner}/{repo}/readme",
            headers={"Accept": "application/vnd.github.raw"},
        )
    r.raise_for_status()
    return r.text


@mcp.prompt()
def review_repo(owner: str, repo: str) -> str:
    """Prompt template: assess a repo as a portfolio piece."""
    return (
        f"Look at {owner}/{repo}. Use get_repo and recent_commits, and read its README "
        f"resource. Assess it as a portfolio project: what's genuinely impressive, what "
        f"looks unfinished, and what a hiring engineer would ask about it."
    )

    
if __name__ == "__main__":
    mcp.run()
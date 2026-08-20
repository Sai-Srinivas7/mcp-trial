# mcp-trial

Me learning the Model Context Protocol by building a server for the GitHub API.
Python SDK v2, running over stdio and hooked into Claude Code.

## What it does

Two tools, one for a repo's summary and one for its recent commit messages. There's
also a resource that serves a repo's raw README, and a prompt template for assessing
a repo as a portfolio piece.

## Running it

```bash
uv sync
uv run mcp dev server.py          # opens the inspector
uv run python test_server.py      # calls the server directly, no host needed
```

To register it with Claude Code:

```bash
claude mcp add gh-lab -- uv run --directory /path/to/mcp-trial mcp run server.py
```

## What I learned

Your type hints are the actual API contract, since the SDK builds the tool's JSON
schema straight from the function signature. Writing `limit: int = 5` also makes that
parameter optional, so the model can skip it.

Docstrings mattered more than I expected, because they get sent to the model as the
tool description and decide which tool it picks. I asked Claude Code whether a repo
was actively maintained, and it called both tools and worked it out, which only
happened because the descriptions made them look combinable.

Everything a tool returns becomes text in the model's context, so each field costs
tokens. GitHub hands back about a hundred fields and I return five.

Raising an error beats returning one, since raising sets a flag the host checks and
the message reaches the model as something it can act on.

Async doesn't make anything faster. A single call takes the same time either way.
What `await` does is park the function and free the event loop so other calls can run
during the wait.

## Notes

`mcp-reference.md` has my working notes from building this.

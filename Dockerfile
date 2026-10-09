# Oubliai MCP server for Fly.io (or any container host).
# Runs the module entry point so OUBLIAI_BROWSER_ORIGINS CORS middleware can be applied
# (see CLAUDE.md: `fastmcp run fastmcp.json` cannot pass middleware).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir uv

WORKDIR /app
# Dependencies first for layer caching; the server package is installed from packages/server.
COPY requirements.txt ./requirements.txt
COPY packages/server ./packages/server
# Editable install keeps the package under /app/packages/server/src so spec.py's
# repository-relative paths (docs/reference/telnyx) resolve exactly as in the repo.
RUN uv pip install --system --no-cache -r requirements.txt \
 && uv pip install --system --no-cache --no-deps -e ./packages/server

# The server loads the canonical Telnyx schema and OAuth metadata from docs/reference/telnyx.
COPY docs/reference/telnyx ./docs/reference/telnyx
COPY server.py ./server.py

# FastMCP listener settings: bind all interfaces on the port Fly routes to.
ENV FASTMCP_HOST=0.0.0.0 FASTMCP_PORT=8080
EXPOSE 8080
CMD ["python", "-m", "oubliai_server"]

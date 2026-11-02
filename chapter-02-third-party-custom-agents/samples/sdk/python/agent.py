"""Minimal custom engine agent for the Agent 365 PoC (Python).

Built on the Microsoft 365 Agents SDK hosting layer, following the
Microsoft 365 Agents SDK Python quickstart sample
(https://github.com/microsoft/Agents/tree/main/samples/python/quickstart) and
https://learn.microsoft.com/microsoft-365/agents-sdk/quickstart?pivots=python

This file is the agent code only. It doesn't register the agent with
Agent 365. Registration (agent identity blueprint, agent identity,
permissions) is done with the Agent 365 CLI (``a365 setup all``) or the
Agent 365 Skills (``a365-setup`` > ``make-a365-agent``). See ../README.md.

Install:
    pip install microsoft-agents-hosting-aiohttp microsoft-agents-authentication-msal python-dotenv

Connection settings are read from environment variables or a .env file
(CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENTID, __CLIENTSECRET,
__TENANTID). Don't commit the .env file. Then run:
    python agent.py
"""

from os import environ

from aiohttp.web import Application, Request, Response, run_app
from dotenv import load_dotenv
from microsoft_agents.activity import load_configuration_from_env
from microsoft_agents.authentication.msal import MsalConnectionManager
from microsoft_agents.hosting.aiohttp import (
    CloudAdapter,
    jwt_authorization_middleware,
    start_agent_process,
)
from microsoft_agents.hosting.core import (
    AgentApplication,
    Authorization,
    MemoryStorage,
    TurnContext,
    TurnState,
)

load_dotenv()
agents_sdk_config = load_configuration_from_env(environ)

STORAGE = MemoryStorage()
CONNECTION_MANAGER = MsalConnectionManager(**agents_sdk_config)
ADAPTER = CloudAdapter(connection_manager=CONNECTION_MANAGER)
AUTHORIZATION = Authorization(STORAGE, CONNECTION_MANAGER, **agents_sdk_config)

AGENT_APP = AgentApplication[TurnState](
    storage=STORAGE, adapter=ADAPTER, authorization=AUTHORIZATION, **agents_sdk_config
)


@AGENT_APP.activity("message")
async def on_message(context: TurnContext, _state: TurnState):
    prompt = context.activity.text or ""

    # Optional: Purview DLP guard before the model call.
    # The `purview-dlp-integration` skill adds a guard that calls the
    # Microsoft Graph processContent API and stops the turn when an
    # input-blocking DLP policy matches. See Chapter 2, section 2.11.2.

    reply = await call_your_model(prompt)

    await context.send_activity(reply)


async def call_your_model(prompt: str) -> str:
    # Replace with your model client (Azure OpenAI, Microsoft Foundry, or other).
    return f"Echo: {prompt}"


async def entry_point(req: Request) -> Response:
    agent: AgentApplication = req.app["agent_app"]
    adapter: CloudAdapter = req.app["adapter"]
    return await start_agent_process(req, agent, adapter)


def main() -> None:
    app = Application(middlewares=[jwt_authorization_middleware])
    app.router.add_post("/api/messages", entry_point)
    app["agent_configuration"] = CONNECTION_MANAGER.get_default_connection_configuration()
    app["agent_app"] = AGENT_APP
    app["adapter"] = AGENT_APP.adapter
    run_app(app, host="localhost", port=int(environ.get("PORT", 3978)))


if __name__ == "__main__":
    main()

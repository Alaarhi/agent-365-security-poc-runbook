// Minimal custom engine agent for the Agent 365 PoC (.NET).
//
// Built on the Microsoft 365 Agents SDK hosting layer, following the
// "Create and test a basic agent" quickstart:
// https://learn.microsoft.com/microsoft-365/agents-sdk/quickstart?pivots=dotnet
//
// This file is the agent code only (Program.cs of a `dotnet new web` project).
// It doesn't register the agent with Agent 365. Registration (agent identity
// blueprint, agent identity, permissions) is done with the Agent 365 CLI
// (`a365 setup all`) or the Agent 365 Skills (`a365-setup` > `make-a365-agent`).
// See ../README.md.
//
// Install:
//   dotnet add package Microsoft.Agents.Hosting.AspNetCore

using Microsoft.Agents.Builder;
using Microsoft.Agents.Builder.App;
using Microsoft.Agents.Builder.State;
using Microsoft.Agents.Core.Models;
using Microsoft.Agents.Hosting.AspNetCore;
using Microsoft.Agents.Storage;
using Microsoft.AspNetCore.Builder;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpClient();
builder.AddAgentApplicationOptions();
builder.AddAgent<PocAgent>();
builder.Services.AddSingleton<IStorage, MemoryStorage>();

var app = builder.Build();

app.MapPost("/api/messages", async (HttpRequest request, HttpResponse response, IAgentHttpAdapter adapter, IAgent agent, CancellationToken cancellationToken) =>
{
    await adapter.ProcessAsync(request, response, agent, cancellationToken);
});

app.Run();

public class PocAgent : AgentApplication
{
    public PocAgent(AgentApplicationOptions options) : base(options)
    {
        OnActivity(ActivityTypes.Message, OnMessageAsync, rank: RouteRank.Last);
    }

    private async Task OnMessageAsync(ITurnContext turnContext, ITurnState turnState, CancellationToken cancellationToken)
    {
        var prompt = turnContext.Activity.Text ?? string.Empty;

        // Optional: Purview DLP guard before the model call.
        // The `purview-dlp-integration` skill adds a best-effort delegated guard
        // for .NET that calls the Microsoft Graph processContent API. See Chapter 2, section 2.11.2.

        var reply = await CallYourModelAsync(prompt);

        await turnContext.SendActivityAsync(reply, cancellationToken: cancellationToken);
    }

    // Replace with your model client (Azure OpenAI, Microsoft Foundry, or other).
    private static Task<string> CallYourModelAsync(string prompt)
        => Task.FromResult($"Echo: {prompt}");
}

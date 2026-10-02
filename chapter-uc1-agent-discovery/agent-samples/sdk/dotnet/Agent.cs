// Minimal Agent 365 SDK agent skeleton for the PoC.
//
// Shows the hosting-layer shape produced by `make-ai-teammate` from
// microsoft/agent365-skills (.NET variant). Replace the LLM call with your
// actual model client. Run `a365 setup all` first to produce the Blueprint
// and Entra Agent Identity so this agent is discoverable in Agent 365.
//
// NuGet:
//   dotnet add package Microsoft.Agents.Builder
//   dotnet add package Microsoft.Agents.Hosting.AspNetCore

using Microsoft.Agents.Builder;
using Microsoft.Agents.Builder.App;
using Microsoft.Agents.Core.Models;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddHttpClient();
builder.Services.AddAgentApplicationOptions();
builder.Services.AddTransient<AgentApplication, SampleAgent>();

var app = builder.Build();
app.MapPost("/api/messages", (HttpRequest req, IAgentHttpAdapter adapter, AgentApplication agent, CancellationToken ct)
    => adapter.ProcessAsync(req, agent, ct));

app.Run();

public class SampleAgent : AgentApplication
{
    public SampleAgent(AgentApplicationOptions options) : base(options)
    {
        OnActivity(ActivityTypes.Message, async (turnContext, turnState, ct) =>
        {
            var prompt = turnContext.Activity.Text ?? string.Empty;

            // 1. (Optional, strongly recommended) Purview DLP guard goes here.
            //    See purview-dlp-integration skill.

            // 2. Call your LLM.
            var reply = await CallYourModelAsync(prompt);

            // 3. (Optional) Purview output audit.

            await turnContext.SendActivityAsync(reply, cancellationToken: ct);
        });
    }

    private static Task<string> CallYourModelAsync(string prompt)
        => Task.FromResult($"Echo: {prompt}");
}

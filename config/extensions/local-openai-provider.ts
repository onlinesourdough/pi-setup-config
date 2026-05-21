import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

/**
 * Local OpenAI-compatible provider for Windows/local-model setups.
 *
 * Defaults:
 * - base URL: http://localhost:1234/v1 (LM Studio)
 * - API key: LOCAL_OPENAI_API_KEY env var, or "not-needed"
 * - default model in config/windows/settings.json: local-model
 *
 * Override with env vars when needed:
 * - LOCAL_OPENAI_BASE_URL=http://localhost:11434/v1
 * - LOCAL_OPENAI_MODEL=qwen2.5-coder:32b
 * - LOCAL_OPENAI_API_KEY=ollama
 */
export default function (pi: ExtensionAPI) {
  const modelId = process.env.LOCAL_OPENAI_MODEL || "local-model";

  pi.registerProvider("local-openai", {
    name: "Local OpenAI Compatible",
    baseUrl: process.env.LOCAL_OPENAI_BASE_URL || "http://localhost:1234/v1",
    apiKey: process.env.LOCAL_OPENAI_API_KEY || "not-needed",
    api: "openai-completions",
    models: [
      {
        id: modelId,
        name: `Local: ${modelId}`,
        reasoning: false,
        input: ["text"],
        cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
        contextWindow: Number(process.env.LOCAL_OPENAI_CONTEXT_WINDOW || 128000),
        maxTokens: Number(process.env.LOCAL_OPENAI_MAX_TOKENS || 8192),
        compat: {
          supportsDeveloperRole: false
        }
      }
    ]
  });
}

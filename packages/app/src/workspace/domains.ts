export const WORKSPACE_DOMAINS = [
  "numbers",
  "messaging",
  "fax",
  "verify",
  "video",
  "meetings",
  "email",
  "voice",
  "ai",
  "rag",
  "speech",
  "storage",
  "training",
  "platform",
] as const;

export type WorkspaceDomain = (typeof WORKSPACE_DOMAINS)[number];

const WORKSPACE_DOMAIN_SET: ReadonlySet<string> = new Set(WORKSPACE_DOMAINS);

export function workspaceToolName(domain: WorkspaceDomain): string {
  return `${domain}_workspace`;
}

export function workspaceCode(domain: WorkspaceDomain): string {
  return `return await call_tool('${workspaceToolName(domain)}', {})`;
}

export function isWorkspaceDomain(value: unknown): value is WorkspaceDomain {
  return typeof value === "string" && WORKSPACE_DOMAIN_SET.has(value);
}

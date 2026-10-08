import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { build } from "esbuild";

/**
 * Build the official AppBridge host, the two-origin sandbox proxy, and the
 * serving entry, following the recipe proven in the build probe:
 *
 *   dist/host/index.js      browser bundle of the page entry
 *   dist/host/index.html    page shell that loads it
 *   dist/sandbox/sandbox.html  official sandbox HTML with the bundle inlined
 *   dist/serve.js           node bundle of the vendored express servers
 *
 * Ports and the sandbox referrer allowlist are build-time configuration; the
 * vendored sources read them through `define` identifiers so the official code
 * stays byte-identical apart from the documented `// oubliai:` edits.
 */

const PACKAGE_ROOT = dirname(fileURLToPath(import.meta.url));
const HOST_DIR = join(PACKAGE_ROOT, "src", "host");
const DIST = join(PACKAGE_ROOT, "dist");

const HOST_PORT = process.env.HOST_PORT ?? "8080";
const SANDBOX_PORT = process.env.SANDBOX_PORT ?? "8081";
const SANDBOX_PROXY_BASE_URL =
  process.env.SANDBOX_PROXY_BASE_URL ??
  `http://localhost:${SANDBOX_PORT}/sandbox.html`;
const ALLOWED_REFERRER =
  process.env.OUBLIAI_ALLOWED_REFERRER ??
  String.raw`^http://(localhost|127\.0\.0\.1)(:|/|$)`;

const SANDBOX_SCRIPT_TAG =
  '<script type="module" src="/src/sandbox.ts"></script>';

const PAGE_HTML = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="color-scheme" content="light dark" />
    <title>Oubliai host</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/index.js"></script>
  </body>
</html>
`;

await mkdir(join(DIST, "host"), { recursive: true });
await mkdir(join(DIST, "sandbox"), { recursive: true });

// Host page bundle.
await build({
  entryPoints: [join(HOST_DIR, "index.ts")],
  outfile: join(DIST, "host", "index.js"),
  bundle: true,
  platform: "browser",
  format: "esm",
  target: "es2022",
  define: {
    __OUBLIAI_SANDBOX_PROXY_BASE_URL__: JSON.stringify(SANDBOX_PROXY_BASE_URL),
  },
});
await writeFile(join(DIST, "host", "index.html"), PAGE_HTML, "utf8");

// Sandbox proxy bundle, inlined into the official sandbox HTML.
const sandboxBundle = await build({
  entryPoints: [join(HOST_DIR, "sandbox.ts")],
  bundle: true,
  platform: "browser",
  format: "esm",
  target: "es2022",
  write: false,
  define: {
    __OUBLIAI_ALLOWED_REFERRER__: JSON.stringify(ALLOWED_REFERRER),
  },
});
const sandboxCode = sandboxBundle.outputFiles[0];
if (!sandboxCode) {
  throw new Error("esbuild produced no sandbox output file");
}
const sandboxHtml = await readFile(join(HOST_DIR, "sandbox.html"), "utf8");
if (!sandboxHtml.includes(SANDBOX_SCRIPT_TAG)) {
  throw new Error(
    `sandbox.html no longer contains the expected script tag: ${SANDBOX_SCRIPT_TAG}`,
  );
}
await writeFile(
  join(DIST, "sandbox", "sandbox.html"),
  sandboxHtml.replace(
    SANDBOX_SCRIPT_TAG,
    () =>
      '<script type="module">' +
      sandboxCode.text.replace(/<\/script/gi, String.raw`<\/script`) +
      "</script>",
  ),
  "utf8",
);

// Serving entry: node bundle with runtime packages left external.
await build({
  entryPoints: [join(HOST_DIR, "serve.ts")],
  outfile: join(DIST, "serve.js"),
  bundle: true,
  platform: "node",
  format: "esm",
  target: "node22",
  packages: "external",
});

process.stdout.write(
  `built host (:${HOST_PORT}) and sandbox (:${SANDBOX_PORT}) bundles into dist/\n`,
);

# Linkek — minden meglátogatott forrás

Kampány: `mcp-hibak` · 2026-09-12


---

## SQ-01 — A hibamodell adverzariális ellenőrzése

# SQ-01 — Linkek és forrásjegyzék

Minden forrás nyers `curl` letöltéssel lett ellenőrizve (a raw.githubusercontent.com és a
modelcontextprotocol.io renderelt oldalak esetén sima HTML→szöveg regex-konverzióval, AI-
összefoglaló nélkül), kivéve ahol külön jelezve van, hogy WebFetch-csel (kis modell
összefoglalóval) történt — azokat NEM idézzük szó szerint, csak jelzésértékű
kontextusként.

## T1 — Hivatalos specifikáció és séma

- https://modelcontextprotocol.io/specification/2026-07-28/server/tools — renderelt spec-oldal, "Error Handling" szakasz. Ellenőrizve: nyers `curl` + regex-alapú tag-eltávolítás, nem AI-összefoglaló.
- https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/server/tools.mdx — a fenti oldal forrás-Markdown-ja.
- https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2026-07-28/schema.ts — a 2026-07-28 kiadás TypeScript sémája (`CallToolResult`, `CallToolRequestParams`, `Result`, `ReadResourceResult` definíciók).
- https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2026-07-28/examples/CallToolResult/invalid-tool-input-error.json — kanonikus, elnevezett példa a séma-repóból.
- https://modelcontextprotocol.io/specification/2026-07-28/changelog — a 2026-07-28 kiadás changelog-ja (8. pont: `resultType`; "Minor changes" 6. pont: `-32002` → `-32602` erőforrás-hiba kód).
- https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/changelog.mdx — a fenti forrása.
- https://modelcontextprotocol.io/specification/2026-07-28/schema — séma-oldal (nem részletesen idézve, csak létezés-ellenőrzés).

### Korábbi spec-verziók (összevetéshez — mikor jelent meg a MAY/SHOULD szöveg)

- https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2025-11-25/server/tools.mdx — **itt jelenik meg először** a MAY/SHOULD mondatpár, szó szerint azonosan a 2026-07-28-assal.
- https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2025-06-18/server/tools.mdx — nincs benne a MAY/SHOULD mondatpár.
- https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2025-03-26/server/tools.mdx — nincs benne.
- https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2024-11-05/server/tools.mdx — nincs benne (ez az eredeti, legkorábbi verzió).

## T1 — SEP-ek (Specification Enhancement Proposal, elfogadott/Final)

- https://modelcontextprotocol.io/seps/1303-input-validation-errors-as-tool-execution-errors — "Input Validation Errors as Tool Execution Errors", Final, létrehozva 2025-08-05, szerző @fredericbarthelet. Ez formalizálta, hogy a bemeneti validációs hiba Tool Execution Error, nem Protocol Error.
- https://modelcontextprotocol.io/seps/2164-resource-not-found-error — "Standardize Resource Not Found Error Code", Final, létrehozva 2026-01-28, szerző Peter Alexander (@pja-ant). Ez az egyetlen talált eset, ahol egy "üzleti jellegű" (nem található) állapot explicit módon protokollhibaként van kodifikálva — de csak a `resources/read`-re, mert nincs `isError`-ekvivalense.

## T1 — TypeScript SDK forráskód (`modelcontextprotocol/typescript-sdk`, `main` ág)

- https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/packages/server/src/server/mcp.ts — a `tools/call` handler, `validateToolInput`, `createToolError`. Ez a fő bizonyíték a 4. és 7. pontra.
- https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/packages/core-internal/src/types/errors.ts — `ProtocolError` osztály ("Protocol errors are JSON-RPC errors that cross the wire as error responses"), `ResourceNotFoundError`.
- https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/packages/server/src/server/server.ts — alacsonyabb szintű dispatch-logika, több `ProtocolError` dobás helye.
- Megjegyzés: a repóban jelenleg futó legfrissebb csomagverzió `2.0.0-beta.1` (jsdelivr csomagregisztráció szerint); a `main` ág a `packages/core-internal/src/wire/rev2026-07-28/` mappát tartalmazza, tehát ez a 2026-07-28-as protokoll-revízióval párhuzamosan fejlesztett kódág — nem egy elavult, korábbi verzió.

## T1 — Python SDK forráskód és hivatalos dokumentáció (`modelcontextprotocol/python-sdk`, v2.2.0 / `main`)

- https://py.sdk.modelcontextprotocol.io/servers/handling-errors/ — **hivatalos, renderelt SDK-dokumentáció**, "Handling errors" oldal. Ez tartalmazza a kutatás legerősebb idézetét ("There is no result. No content, no is_error: nothing for the model to read.").
- https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/src/mcp/server/mcpserver/server.py — `_handle_call_tool` metódus, a `ToolError`/kivétel → `isError` konverzió és az `MCPError` → újradobás logika.
- https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/src/mcp/server/mcpserver/tools/tool_manager.py — `ToolManager.call_tool`, ahol az "Unknown tool" hiba `ToolError`-ként (nem `MCPError`-ként) van dobva — l. SDK-inkonzisztencia, 4c. pont.
- https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/docs_src/handling_errors/tutorial001.py — `ToolError` mintapélda (a hivatalos doksi forrása).
- https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/docs_src/handling_errors/tutorial002.py — `MCPError` mintapélda (ugyanaz a szituáció, "rossz" megoldásként bemutatva).
- https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/docs_src/handling_errors/tutorial003.py — `ResourceNotFoundError` mintapélda.
- https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/docs_src/handling_errors/tutorial004.py — kezeletlen kivétel (crash) mintapélda.
- https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/examples/stories/error_handling/server.py — "Two error channels: ToolError -> is_error result; MCPError -> JSON-RPC protocol error" (fájl-fejléc kommentje).
- https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/examples/stories/error_handling/server_lowlevel.py — ugyanaz alacsony szintű API-val.
- https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/examples/stories/error_handling/client.py — kliens-oldali bizonyíték: "Execution error: arrives as a *result* — await returns, no exception." vs. "Protocol error: arrives as a raised MCPError."

## T3 — Gyenge, másodlagos/anekdotikus bizonyíték (csak kontextusként, NEM idézve szó szerint állításalapként)

- https://github.com/modelcontextprotocol/servers/issues/3122 — egyetlen, karbantartói válasz nélküli GitHub-issue, ami azt állítja, hogy ugyanaz a `-32602` hiba Cursor-ban látható hibaként jelenik meg, de Claude Code/Roocode/Cline/kilo code/TRAE-ban nem. Tartalma WebFetch-csel (kis modell összefoglalója) lett kinyerve, mert a nyers GitHub-elérés ehhez a repóhoz ebben a szekcióban proxy-szinten korlátozva volt ("GitHub access to this repository is not enabled for this session"; l. `gaps.md`). Nem erősítjük meg a jelenség okát — lehet, hogy nem is a MAY/SHOULD-mechanizmushoz kapcsolódik.

## Kiegészítő keresési találatok, amiket NEM dolgoztunk fel részletesen (idő/terjedelem korlát miatt — l. `gaps.md`)

- https://reference.langchain.com/python/langchain-mcp-adapters
- https://github.com/langchain-ai/langchain-mcp-adapters
- https://csharp.sdk.modelcontextprotocol.io/v1/api/ModelContextProtocol.Protocol.CallToolResult.html
- https://apxml.com/courses/getting-started-model-context-protocol/chapter-3-implementing-tools-and-logic/error-handling-reporting
- https://mcpcat.io/guides/error-handling-custom-mcp-servers/ (T3, harmadik fél blogja)
- https://chatforest.com/guides/mcp-error-handling-resilience/ (T3, harmadik fél blogja)


---

## SQ-02 — Jogosultság-elutasításkor mit szabad elárulni

# SQ-02 — Felhasznált források (tier szerint)

## T1 — RFC / hivatalos szabvány / hivatalos gyártói dokumentáció

- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html) (letöltve, nyers
  szöveg: `sq02/nyers-forrasok/rfc9110-full.txt`, kivonat: `rfc9110-403-404-snippet.txt`) —
  §15.5.4 403 Forbidden, §15.5.5 404 Not Found
- [CWE-209 — Generation of Error Message Containing Sensitive Information](https://cwe.mitre.org/data/definitions/209.html)
- [CWE-210 — Self-generated Error Message Containing Sensitive Information](https://cwe.mitre.org/data/definitions/210.html)
- [CWE-200 — Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html)
- [CWE-203 — Observable Discrepancy](https://cwe.mitre.org/data/definitions/203.html)
- [OWASP Top 10:2021 — A01 Broken Access Control (hivatalos markdown)](https://github.com/OWASP/Top10/blob/master/osib/docs/A01_2021-Broken_Access_Control.md)
  (archiválva: `owasp-top10-a01.md`)
- [OWASP ASVS 4.0.3 — V4 Access Control (hivatalos markdown)](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V4-Access-Control.md)
  (archiválva: `owasp-asvs-v4-access-control.md`)
- [OWASP ASVS 4.0.3 — V7 Error Handling and Logging (hivatalos markdown)](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x15-V7-Error-Logging.md)
  (archiválva: `owasp-asvs-v7-error-logging.md`) — 7.4.1 tétel
- [OWASP Authorization Cheat Sheet (hivatalos markdown)](https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Authorization_Cheat_Sheet.md)
  (archiválva: `owasp-authorization-cheatsheet.md`)
- [OWASP Access Control Cheat Sheet (elavult, átirányít)](https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html)
- [GitHub Docs — Troubleshooting the REST API](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api)
  (archiválva: `github-troubleshooting-rest-api.html`) — "404 instead of 403 to avoid
  confirming existence of private repositories"
- [GitLab Docs — REST API Troubleshooting](https://docs.gitlab.com/api/rest/troubleshooting/)
  (archiválva: `gitlab-rest-troubleshooting.html`) — 404 leírás egyesített okkal
- [Google Workspace — Drive API: Resolve errors](https://developers.google.com/workspace/drive/api/guides/handle-errors)
  (archiválva: `google-drive-errors.html`) — `notFound` és `insufficientFilePermissions` leírás
- [Kubernetes Docs — Authorization](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)
  (archiválva: `k8s-authz.html`) — "overall deny verdict... HTTP 403 (Forbidden)"
- [Model Context Protocol — Authorization spec (2026-07-28)](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) —
  "Error Handling" táblázat (401/403/400)
- [Discourse — config/site_settings.yml (GitHub, main branch)](https://github.com/discourse/discourse/blob/main/config/site_settings.yml)
  (archiválva: `discourse-site_settings.yml`) — `detailed_404: false`
- [Discourse — config/locales/server.en.yml (GitHub, main branch)](https://github.com/discourse/discourse/blob/main/config/locales/server.en.yml)
  (a `detailed_404` leírás sora archiválva: `discourse-detailed_404-notes.txt`)
- [AWS IAM User Guide — Troubleshoot access denied error messages (GitHub, awsdocs)](https://github.com/awsdocs/iam-user-guide/blob/main/doc_source/troubleshoot_access-denied.md)
- [AWS S3 Docs — Troubleshoot access denied (403 Forbidden) errors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/troubleshoot-403-errors.html)
  (archiválva: `aws-s3-403-troubleshoot.html`) — általános 403-okok, a ListBucket/404-reláció
  konkrét indoklása NEM szerepel ezen az oldalon
- [kubernetes/kubernetes GitHub Issue #124406 — "forbidden message may include RBAC
  information"](https://github.com/kubernetes/kubernetes/issues/124406) — hivatalos projekt
  repó, biztonsági jegy (HackerOne-eredetű)

## T2 — megbízható másodlagos forrás

- [MDN — 403 Forbidden](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403) —
  RFC 9110-re hivatkozva: "Server owners may decide to send a 404 response instead of a 403..."
- [MDN — 404 Not Found](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404) —
  RFC 9110-re hivatkozva
- [Wikipedia — HTTP 404](https://en.wikipedia.org/wiki/HTTP_404) — RFC 7231-idézet (RFC 9110
  elődje, majdnem azonos szöveg)
- [AWS re:Post — Why Does S3 Return 403 Instead of 404 When the Object Doesn't Exist?](https://repost.aws/articles/ARe3OTZ3SCTWWqGtiJ6aHn8Q/why-does-s-3-return-403-instead-of-404-when-the-object-doesnt-exist)
  — NEM "AWS OFFICIAL" jelölésű közösségi cikk, de tartalmilag konzisztens sok más forrással

## T3 — fórum, blog, vélemény (kizárólag illusztrációra / gyakorlati színezésre használva,
nem normatív állítás alátámasztására)

- [dev.to — Returning HTTP 404 Responses Instead of 403 For Unauthorised Access (ashallendesign)](https://dev.to/ashallendesign/returning-http-404-responses-instead-of-403-for-unauthorised-access-22ba)
- [dev.to — Not Found is the wrong answer to a permission problem (nasrulhazim)](https://dev.to/nasrulhazim/not-found-is-the-wrong-answer-to-a-permission-problem-25cm)
  — kifejezetten AI-ügynök/MCP-kontextusú érvelés
- [dev.to — Why your API's error messages fail when called by an LLM (johnonline35)](https://dev.to/johnonline35/why-your-apis-error-messages-fail-when-called-by-an-llm-and-how-to-fix-them-5a5d)
- [apxml.com — Tool Error Handling (LLM Agent Tools kurzus)](https://apxml.com/courses/building-advanced-llm-agent-tools/chapter-1-llm-agent-tooling-foundations/tool-error-handling)
- [GitLab Issue #65271 — Release API: return 403 instead of 404 when not enough permissions](https://gitlab.com/gitlab-org/gitlab-ce/-/issues/65271)
- [GitLab Issue #20878 — The 404 response could also indicate a permissions problem?](https://gitlab.com/gitlab-org/gitlab/-/issues/20878)
- [GitLab Issue #36367 — Empty private-token for api call results in "404 Project Not Found"](https://gitlab.com/gitlab-org/gitlab/-/issues/36367)
- Atlassian közösségi bejegyzések a Jira "Issue does not exist or you do not have permission to
  see it." sztringről (több független jelentés, pl.
  [community.developer.atlassian.com](https://community.developer.atlassian.com/t/issue-does-not-exist-or-you-do-not-have-permission-to-see-it-via-rest-curl-api/39804))
  — a sztring léte T3-forrásokból ismert, tehát fenntartással kezelendő, de nagy számú
  egymástól független megerősítés miatt gyakorlatilag bizonyosnak tekinthető tényként a
  sztring szó szerinti tartalmára nézve (maga a magyarázat/indoklás viszont nincs sehol
  dokumentálva, még T3-ban sem)

## Ellenőrzött, de a végleges anyagba nem került / kevés hozadékú fetch-ek

- OWASP Access Control Cheat Sheet — elavult, tartalom nélkül
- Microsoft Graph — `security-error-codes.md` és `resolve-auth-errors` — nem hozták vissza az
  `itemNotFound`/`accessDenied` közvetlen összevetését (ld. `gaps.md`)
- Docker/OCI Distribution API spec — nem tér ki a 401-vs-404 kérdésre magánrepóknál (a
  specifikáció hiányosságaként dokumentálva a `megallapitasok.md`-ben nem került külön
  kiemelésre helyhiány miatt, de a keresési naplóban szerepel)
- Django REST Framework Permissions dokumentáció — nem tartalmaz 403/404 elrejtési
  iránymutatást
- OpenID AuthZEN patterns oldal, NCC Group API authorization cikk — nem térnek ki erre a
  konkrét kérdésre


---

## SQ-03 — Mit kell megvalósítania egy szabványos MCP erőforrás-szervernek

# SQ-03 — Linkek / források

Tier-jelölés a feladat definíciója szerint: **T1** = hivatalos MCP specifikáció, RFC, SDK
forráskód. Minden alábbi forrás T1, a fetch dátuma 2026-09-12.

## Elsődleges (MCP spec, `2026-07-28`)

| URL | Mit tartalmaz | Felhasznált-e verbatim idézetre |
|---|---|---|
| https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | Fő authorization spec: Roles, Overview, Scope Selection, Resource Parameter, Access Token Usage, Error Handling | Igen |
| https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/authorization-server-discovery | PRM (RFC 9728) kötelezettségek, WWW-Authenticate/well-known felfedezési mechanizmusok | Igen |
| https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/client-registration | CIMD, Pre-registration, DCR (deprecated), Authorization Server Binding | Igen |
| https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations | Token audience binding, Confused Deputy, Access Token Privilege Restriction | Igen |
| https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices | Confused Deputy Problem (részletes), Token Passthrough (részletes), SSRF | Igen |
| https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/authorization | Authorization tutorial (kiegészítő, kevésbé normatív) | Csak ellenőrzésre, nem idézve |
| https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning | Verzió-állapot: `2026-07-28` = Current | Igen |
| https://modelcontextprotocol.io/specification/2026-07-28/deprecated | Deprecated Features Registry — DCR bejegyzés | Igen |
| https://modelcontextprotocol.io/llms.txt | Dokumentum-index, verziólista igazolására | Igen (verziólista) |
| https://github.com/modelcontextprotocol/ext-auth | MCP Authorization Extensions repo (említve a spec végén, nem olvasva részletesen) | Nem idézve |

## Verzió-összevetés (korábbi MCP spec)

| URL | Mit tartalmaz |
|---|---|
| https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization | `2025-06-18` authorization spec — összevetésre a DCR/CIMD változáshoz |

## RFC-k és IETF draft (nyers szöveg, rfc-editor.org / ietf.org)

| URL | Mit tartalmaz |
|---|---|
| https://www.rfc-editor.org/rfc/rfc9728.txt | OAuth 2.0 Protected Resource Metadata — teljes szöveg |
| https://www.rfc-editor.org/rfc/rfc8707.txt | Resource Indicators for OAuth 2.0 — teljes szöveg |
| https://www.rfc-editor.org/rfc/rfc6750.txt | OAuth 2.0 Bearer Token Usage — WWW-Authenticate formátum, hibakódok |
| https://www.ietf.org/archive/id/draft-ietf-oauth-v2-1-13.txt | OAuth 2.1 draft 13 — 5.2 (Access Token Validation), 5.3 (Error Response) |

## Nem lekért, de a szövegben hivatkozott források (nem elsődleges igazolás ehhez a körhöz)

- RFC 7591 (OAuth 2.0 Dynamic Client Registration Protocol) — csak a spec saját idézetén
  keresztül hivatkozva, nem olvasva nyersen.
- RFC 9207 (Authorization Server Issuer Identification) — a spec "Authorization Response
  Validation" szakaszában idézve, nem olvasva nyersen külön.
- RFC 9068 (JWT Profile for Access Tokens) — csak említés szintjén hivatkozva a
  security_best_practices oldalon.
- draft-ietf-oauth-client-id-metadata-document-00 (CIMD alap-draft) — a spec idézi a
  kulcskövetelményeket, magát a draftot nem olvastam nyersen (l. `gaps.md`).

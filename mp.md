You are an Elite DevOps & AI Architect tasked with building a comprehensive `joules_daily_runner.py` system and GitHub Actions workflow that orchestrates the Jules autonomous coding agent for intelligent repository management and optimization.

**Primary Objective:** Automate daily creation and optimization of high-quality software repositories that maximize potential GitHub visibility while strictly adhering to the 100 Jules Sessions per day limit. All newly created repositories must be Private by default for manual review before public release.

**Critical Constraints:**
- Jules API allows exactly 100 sessions per day (hard limit)
- All code must meet FAANG-level quality standards
- New repositories must be created as Private initially
- Must strictly follow `AGENTS.md` for technology stack decisions
- Must integrate and extend logic from `jules_mega_optimizer_v2.py`
- Available credentials: `JULES_API_KEY` and `GITHUB_TOKEN` and many more
- Must utilize all available MCP servers and tools for web searching, trend analysis, and API interactions

**Implementation Requirements:**

**Phase 1: Pre-Execution Analysis**
- Read and analyze all existing project files including `jules_mega_optimizer_v2.py`, GitHub Actions workflows, `AGENTS.md`, and any prompt templates
- Query Jules API to retrieve all active sessions and their current states
- Implement session lifecycle management to archive completed sessions after PR merge
- Initialize session budget counter at 100 and track consumption throughout execution

**Phase 2: Trend Discovery & Deduplication**
- Use all available MCP servers and web search tools to identify the top 5 trending software ideas, Chrome extension concepts, and pain points from Google Trends, YouTube trending topics, and developer communities
- Fetch complete list of user's existing GitHub repositories via GitHub API
- Implement fuzzy matching (using fuzzywuzzy or similar NLP) to compare discovered trends against existing repository names and descriptions
- Classify each trend as either "Creation Task" (new private repository needed) or "Update Task" (enhancement to existing repository)

**Phase 3: High-Priority Execution (New Trending Projects)**
- Allocate 10-15 sessions from the budget for new/trending ideas
- For each Creation Task:
  - Start a new Jules Session with comprehensive prompt: "Act as a Senior FAANG Engineer. Build a complete, production-ready [Idea Name] using the technology stack specified in AGENTS.md. Generate full project structure including src, tests, comprehensive documentation, CI/CD pipelines, and deployment configurations."
  - Create new Private GitHub repository
  - Monitor Jules session for completion via polling
  - Push generated code to the private repository
  - Archive the Jules session after successful completion
  - Decrement session_budget counter
- For each Update Task:
  - Start Jules Session with prompt to add new features/improvements to existing repository
  - Create Pull Request with generated changes
  - Auto-merge if CI/CD tests pass
  - Archive session after PR merge
  - Decrement session_budget counter

**Phase 4: Low-Priority Execution (Repository Optimization)**
- Import and integrate all optimization logic from `jules_mega_optimizer_v2.py`
- Calculate remaining session budget after Phase 3
- Identify existing repositories requiring optimization (bug fixes, test coverage improvements, documentation enhancements, code refactoring, README improvements)
- Execute optimization tasks using remaining sessions only (strict budget enforcement)
- For each optimization:
  - Start Jules Session with specific improvement prompt
  - Monitor session progress and responses
  - Create PR with improvements
  - Auto-merge if tests pass
  - Archive session
  - Decrement session_budget counter
- Implement hard stop when session_budget reaches 0

**Phase 5: Session Cleanup & Reporting**
- Archive all completed sessions via Jules API to maintain clean dashboard
- Generate execution report including: sessions used, repositories created, repositories updated, remaining budget, any errors encountered
- Log all activities for audit trail

**Technical Implementation Details:**

**File 1: `joules_daily_runner.py`**
- Modular architecture with separate functions for each phase
- Robust error handling with try/catch blocks for all API calls
- Rate limiting and retry logic for API interactions
- Session state polling mechanism to monitor Jules progress
- Fuzzy matching implementation for trend deduplication
- Budget tracking with hard enforcement
- Comprehensive logging throughout execution
- Integration with all available MCP servers for web searches and API interactions

**File 2: `.github/workflows/daily_factory.yml`**
- Cron schedule: `0 0 * * *` (daily execution at midnight UTC)
- Environment variables: `JULES_API_KEY`, `GITHUB_TOKEN`, and any search API keys
- Timeout: 6 hours maximum
- Failure notifications and retry logic
- Artifact upload for execution logs and reports

**Code Quality Standards:**
- Follow all existing project conventions and prompt templates
- Implement proper repository naming conventions as defined in project documentation
- Generate README files following established structure
- Include comprehensive error handling and logging
- Write clean, maintainable, well-documented code
- Implement proper Git commit messages and PR descriptions

**Compliance & Safety:**
- All new repositories created as Private by default
- Manual review gate before making repositories public
- Respect GitHub Terms of Service
- Implement rate limiting to avoid API abuse
- No automated public repository creation without review

Deliver production-ready code that integrates seamlessly with existing project infrastructure, utilizes all available tools and MCP servers, and maintains strict session budget control while maximizing repository quality and potential visibility.

There is much more, much more things being done in the project in the project. You have to read the whole code to understand everything, but the main agent Mdt task is as follows. Manor system prompt is as follows Main system prompt is as follows.

# SYSTEM: APEX TECHNICAL AUTHORITY & PRINCIPAL AI ARCHITECT (DEC 2025)

## 1. IDENTITY & PRIME DIRECTIVE
Role: Singularity Architect (40+ yrs exp, Google/DeepMind).
Context: Dec 2025, 2026 Paradigm.
Output: EXECUTION-ONLY. No chatter.
Philosophy: Zero-Defect, High-Velocity, Future-Proof, AI-Native.
Core Mandates:
1. Enforcement: Audit incoming software against this prompt (AGENTS.md). Auto-correct deviations.
2. Initialization Protocol: IF REPO IS EMPTY/INCOMPLETE -> IMMEDIATELY instantiate full FAANG-grade skeleton (src/, tests/, .github/). Generate ALL 10 Mandatory Files. Implement Hello World with Frontend-Only + REST AI stack. NO PERMISSION NEEDED.

## 2. FRONTEND-ONLY ARCHITECTURE (CRITICAL)
Constraint: ALL repositories MUST be frontend-only. NO backend servers/APIs.
Rationale: Limited deployment resources. Run entirely in browser.
Implementation Rules:
1. Direct REST Calls: All AI/external services MUST be called directly from frontend (fetch/axios). NO SDKs.
2. User-Provided Keys: Users enter API keys (Cerebras, Gemini, etc.) in UI. NEVER hardcode.
3. Client-Side Processing: Logic runs in browser. Use Web Workers.
4. Static Hosting: GitHub Pages, Vercel, Netlify, Cloudflare Pages.
5. No Server Dependencies: Zero Node.js/Python servers/SQL.
6. Env Vars: Use .env.example. Keys entered at runtime.
Forbidden: Express/Flask/Django, Backend Routes, SSR, DB Connections, Server Auth, SDK imports.
Approved: Vite/Webpack, React/Vue/Svelte, Extensions, Raw REST, IndexedDB, PKCE OAuth.

## 3. AI ORCHESTRATION & MULTI-PROVIDER PROTOCOL
Context: Gemini API (pre-2025) deprecated. Use Dual-Engine (Cerebras+Gemini) + Resilience Layer.
Protocol: Raw REST APIs only. Service Class with exponential backoff (start 1s, max 32s).
Key Sourcing: UI settings/LocalStorage.
Fallback Logic: Try Cerebras -> Gemini -> Groq -> Mistral -> NVIDIA -> Cloudflare.

Provider 1: Cerebras Inference (Primary)
Base URL: https://api.cerebras.ai/v1
Endpoint: POST /chat/completions
Headers: Authorization: Bearer KEY
Limits (Dec 2025): 30 RPM, 14,400 RPD, 1M tok/day. Perpetual free.
Models (MMLU Desc):
1. Tier 1: qwen-3-235b-a22b-instruct-2507 (235B).
2. Tier 2: gpt-oss-120b (120B).
3. Tier 3: zai-glm-4.6 (357B).
4. Tier 4: llama-3.3-70b (70B).
5. Tier 5: qwen-3-32b (32B).
6. Tier 6: llama3.1-8b (8B).

Provider 2: Google Gemini API (Backup)
Base URL: https://generativelanguage.googleapis.com/v1beta
Endpoint: POST /models/MODEL:generateContent?key=KEY
Limits (Dec 2025): 30 RPM, 14,400 RPD for Gemma. Perpetual free.
Models (MMLU Desc):
1. Tier 1: gemma-3-27b-instruct (27B, 15k tok/min).
2. Tier 2: gemma-3-12b-instruct (12B).
3. Tier 3: gemma-3-4b-instruct (4B).
4. Tier 4: gemma-3-1b-instruct (1B).

Provider 3: Resilience Layer (Free >1000 RPD)
A. Groq (Ultra-Fast):
Base: https://api.groq.com/openai/v1
Limits: 1k-14.4k RPD depending on model. Perpetual free.
Models: llama-3.1-405b-instruct (Tier 1), openai/gpt-oss-120b (Tier 2), llama-3.3-70b-instruct (Tier 3), qwen/qwen3-32b (Tier 4), llama-3.1-8b-instant (Tier 5).
B. Mistral (La Plateforme):
Base: https://api.mistral.ai/v1
Limits: 1 RPS, ~86k RPD equiv. Perpetual free (Experiment plan).
Models: mistral-large (Tier 1), mistral-small-3.1-24b-instruct (Tier 2), open-mistral-nemo (Tier 3).
C. NVIDIA NIM:
Base: https://api.nvidia.com/nim
Limits: 40 RPM (~57k RPD). Phone verify required.
Models: meta-llama/llama-3.1-405b-instruct (Tier 1), qwen/qwen3-235b-a22b-instruct (Tier 2), meta-llama/llama-3.3-70b-instruct (Tier 3).
D. Cloudflare Workers AI:
Base: https://api.cloudflare.com/client/v4/accounts/ID/ai/run
Limits: 100k req/day.
Models: @cf/meta/llama-3.1-405b-instruct (Tier 1), @cf/openai/gpt-oss-120b (Tier 2), @cf/meta/llama-3.3-70b-instruct (Tier 3).
E. Mistral (Codestral):
Limits: 30 RPM, 2k RPD. Model: codestral-2508.

## 4. REPO STRUCTURE & HYGIENE
Mandate: Clean root. Code in src.
Root Allow-List: package.json, tsconfig.json, biome.json, vite.config.ts, .env.example, README.md, LICENSE, CONTRIBUTING.md, SECURITY.md, AGENTS.md.
Subdirectories: src/ (Logic), src/api/ (REST Wrappers), extension/ (Browser Ext), tests/ (Verification), scripts/ (Build), .github/ (CI/Templates).

## 5. MANDATORY FILES (FAANG STANDARD)
Ensure existence/quality of 10 files:
1. README.md (Hero-Tier)
2. badges.yml (.github/)
3. LICENSE (CC BY-NC)
4. .gitignore
5. .github/workflows/ci.yml
6. CONTRIBUTING.md (Root)
7. .github/ISSUE_TEMPLATE/bug_report.md
8. .github/PULL_REQUEST_TEMPLATE.md
9. SECURITY.md (Root)
10. AGENTS.md (Root - Context Injection)

## 6. ARCHITECTURAL PRINCIPLES (LAWS OF PHYSICS)
Principles: SOLID, GRASP, Clean Architecture, Law of Demeter, DRY, KISS, YAGNI, 12-Factor.
Logic: Core Logic <-> Adapters <-> UI.

## 7. CODE HYGIENE & STANDARDS
Naming: camelCase (TS), PascalCase (Class). Verbs in funcs.
Clean Code: Verticality, Guard Clauses, Pure Funcs. Zero Comments on "What", only "Why".

## 8. CONTEXT-AWARE APEX TECH STACKS (LATE 2025)
Directives: Detect project type and apply Apex Toolchain.
Stack: TypeScript 6.x, Vite 7 (Rolldown), Tauri v2, WXT (Extensions).
HTTP: Native fetch or axios.
State: Signals (Preact/Solid/Vue style).
CSS: Tailwind v4.
Data/AI (Script): uv, Ruff, Pytest.

## 9. RELIABILITY, SECURITY & SUSTAINABILITY
DevSecOps: Zero Trust (Sanitize inputs), Client Keys, Global Error Boundaries.
Recovery: Exponential Backoff.
Green SW: Efficiency (O(n)), Lazy Loading.

## 10. COMPREHENSIVE TESTING STRATEGY
Isolation: All tests in tests/.
Pyramid: Fast, Isolated, Repeatable.
Mandate: 1:1 Mapping. 100% Branch Coverage. Mock all REST endpoints.

## 11. UI/UX AESTHETIC SINGULARITY (2026 STANDARD)
Style: Spatial Glass, Bento Grids, Depth Stacking.
Motion: Kinetic Physics (Springs).
Adaptive: Morph based on input (Touch/Mouse).

## 12. DOCUMENTATION & VERSION CONTROL
Docs: Hero-Tier README, ASCII Tree.
Git: Conventional Commits, Semantic Versioning.

## 13. AUTOMATION SINGULARITY (GITHUB ACTIONS)
Pipelines:
1. Integrity (Lint+Test)
2. Security (Audit+SBOM)
3. Release (SemVer+Artifact)
4. Deps (Auto-merge)

## 14. LLM OPTIMIZATION PROTOCOL (FOR AGENTS.md)
Context: Repo Brain.
Rules: Start files with summary. Keep under 300 lines. Dense documentation.

## 15. THE ATOMIC EXECUTION CYCLE
Loop:
1. Audit: Scan state. IF EMPTY -> EXECUTE INITIALIZATION PROTOCOL.
2. Research: Query Best Practices.
3. Plan: Architect via clear-thought-two.
4. Act: Fix Code + Add Settings + Write Tests + Generate Mandatory Files.
5. Automate: Update CI/CD.
6. Docs: Update README.md & AGENTS.md.
7. Verify: Run Tests.
8. Reiterare: Fix errors.
9. Commit: git commit.
10. Push: git push.
11. Repeat: Loop.

You have to make use of all the mcp servers and all the tools when you are available tool set. And make sure that everything is working fine and everything is good, re available You have to make sure everything should work fine. You have to make sure that code is very modular in nature.

Google Trends + YouTube trending
GitHub trending repositories
Reddit/HackerNews discussions
Developer community forums (Dev.to, Hashnode)decide dynamically based on trend quality and existing repo health scores Please use the best apis free apis, which can be used in the finding of the trends Google Trends, Youtube trends, Github trending repositories or trend discussion hacker news discussions. Developer community forums, you might have to scrap something. You might have to do a many things. Please make a very, very complex repository which will do everything.
Session Budget Allocation: How should the 100 daily sessions be distributed?

10-15 for new trending projects, rest for optimization
Re-use mega optimizer for low priority tasks Rename the joules mega optimizer V2 properly to rename it and properly use it properly. Reuse it properly everywhere in the code. Search the web for the joules Apis on how to archive the Session and how the session is being logged and how the session is been there. You have to check that session being there or not. You have to also check how the session is being performing. If the session is not performing properly, you have to check the responses of the session. You have to check the pr being made completely of the session or not. If the pr is being made, you have to merge it. And if the pr is also merge it, then you have to archive the session. This all tasks have to be done properly. You have. to search a lot of contacts. You need a lot of context which you provided to you by the mcp servers. Remove any other Github action which is running In the loop action which is running in the loop because we have limited resources and only this guitar action being created will be used and all other guitar action being created are All depreciated, and all have to be removed completely You have to delete many files, rename value files, or remove valid files. You have to make sure that everything is according to the identity. You don't have to care about that thing, anything. You have to be super, super vigilant about.


Don't hallucinate anything. Don't have anything being a Hypothetical method because you have access to too many repositories and too many MCP servers. You can do anything in the world. You can do any stuff. You can search the web. You can do many, many stuff. But if you are not doing that, then you are doing a resist. Very bad mistake.

You are completely sure that you have to use the Internet into the code. of By ten 5 you have to use some kind of an api, like brave api or some api Some web scraping of the websites. You have to do that too And you have to. It is not a mvp. It is a complete product It will be a complete product or not a MVP. You have to do everything. Please don't stop at something or somewhere. Please make everything properly. And don't stop anywhere


# Jules API Documentation

## Overview

The Jules REST API allows you to programmatically create and manage coding sessions, monitor progress, and retrieve results. This reference documents all available endpoints, request/response formats, and data types.

### Base URL

All API requests should be made to:

```
https://jules.googleapis.com/v1alpha
```

### Authentication

The Jules REST API uses API keys for authentication. Get your API key from [jules.google.com/settings](https://jules.google.com/settings).

```
curl -H "x-goog-api-key: $JULES_API_KEY" https://jules.googleapis.com/v1alpha/sessions
```

[Authentication Guide](https://jules.google/docs/api/reference/authentication) Detailed setup instructions for API key authentication.

### Endpoints

- **[Sessions](https://jules.google/docs/api/reference/sessions)** Create and manage coding sessions. Sessions represent a unit of work where Jules executes tasks on your codebase.
- **[Activities](https://jules.google/docs/api/reference/activities)** Monitor session progress through activities. Each activity represents an event like plan generation, messages, or completion.
- **[Sources](https://jules.google/docs/api/reference/sources)** List and retrieve connected repositories. Sources represent GitHub repositories that Jules can work with.
- **[Types](https://jules.google/docs/api/reference/types)** Reference for all data types used in the API including Session, Activity, Plan, Artifact, and more.

### Common Patterns

#### Pagination

List endpoints support pagination using `pageSize` and `pageToken` parameters:

```
# First page
curl -H "x-goog-api-key: $JULES_API_KEY" "https://jules.googleapis.com/v1alpha/sessions?pageSize=10"

# Next page (using token from previous response)
curl -H "x-goog-api-key: $JULES_API_KEY" "https://jules.googleapis.com/v1alpha/sessions?pageToken=eyJvZmZzZXQiOjEwfQ=="
```

#### Resource Names

Resources use hierarchical names following Google API conventions:

- Sessions: `sessions/{sessionId}`
- Activities: `sessions/{sessionId}/activities/{activityId}`
- Sources: `sources/{sourceId}`

#### Error Handling

The API returns standard HTTP status codes:

| Status | Description |
| --- | --- |
| 200 | Success |
| 400 | Bad request - invalid parameters |
| 401 | Unauthorized - invalid or missing token |
| 403 | Forbidden - insufficient permissions |
| 404 | Not found - resource doesn’t exist |
| 429 | Rate limited - too many requests |
| 500 | Server error |

Error responses include a JSON body with details:

```
{
  "error": {
    "code": 400,
    "message": "Invalid session ID format",
    "status": "INVALID_ARGUMENT"
  }
}
```

## Authentication Guide

The Jules REST API uses API keys for authentication. You’ll need a valid API key to make API requests.

### Getting Your API Key

1. Go to [jules.google.com/settings](https://jules.google.com/settings)
2. Find the **API Key** section
3. Click **Generate API Key** (or copy your existing key)
4. Store the key securely — it won’t be shown again

Keep your API key secret. Don’t commit it to version control or share it publicly.

### Using Your API Key

Include the API key in the `x-goog-api-key` header with every request:

```
curl -H "x-goog-api-key: YOUR_API_KEY" https://jules.googleapis.com/v1alpha/sessions
```

#### Environment Variable (Recommended)

Store your API key in an environment variable:

```
export JULES_API_KEY="your-api-key-here"
```

Then use it in requests:

```
curl -H "x-goog-api-key: $JULES_API_KEY" https://jules.googleapis.com/v1alpha/sessions
```

### Example: Create a Session

```
curl -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Add unit tests for the utils module",
    "sourceContext": {
      "source": "sources/github-owner-repo",
      "githubRepoContext": {
        "startingBranch": "main"
      }
    }
  }' \
  https://jules.googleapis.com/v1alpha/sessions
```

### Example: List Sessions

```
curl -H "x-goog-api-key: $JULES_API_KEY" https://jules.googleapis.com/v1alpha/sessions
```

### Troubleshooting

#### "API key not valid"

- Verify you copied the entire key without extra spaces
- Check that the key hasn’t been revoked in [settings](https://jules.google.com/settings)
- Generate a new key if needed

- Verify your account has access to Jules
- Check that you have access to the requested resources (sessions, sources)

#### "Quota exceeded"

- You may have hit rate limits

## Sessions

Sessions are the core resource in the Jules REST API. A session represents a unit of work where Jules executes a coding task on your repository.

### Create a Session

**POST** `/v1alpha/sessions`

Creates a new session to start a coding task.

#### Request Body

- `prompt` **required** string
  The task description for Jules to execute.

- `title` string
  Optional title for the session. If not provided, the system will generate one.

- `sourceContext` **required** [SourceContext](#sourcecontext)
  The source repository and branch context for this session.

- `requirePlanApproval` boolean
  If true, plans require explicit approval before execution. If not set, plans are auto-approved.

- `automationMode` string
  Automation mode. Use 'AUTO_CREATE_PR' to automatically create pull requests when code changes are ready.

#### Example Request

```
curl -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Add comprehensive unit tests for the authentication module",
    "title": "Add auth tests",
    "sourceContext": {
      "source": "sources/github-myorg-myrepo",
      "githubRepoContext": {
        "startingBranch": "main"
      }
    },
    "requirePlanApproval": true
  }' \
  https://jules.googleapis.com/v1alpha/sessions
```

#### Response

Returns the created [Session](#session) object:

```
{
  "name": "1234567",
  "id": "abc123",
  "prompt": "Add comprehensive unit tests for the authentication module",
  "title": "Add auth tests",
  "state": "QUEUED",
  "url": "https://jules.google.com/session/abc123",
  "createTime": "2024-01-15T10:30:00Z",
  "updateTime": "2024-01-15T10:30:00Z"
}
```

### List Sessions

**GET** `/v1alpha/sessions`

Lists all sessions for the authenticated user.

#### Query Parameters

- `pageSize` integer query
  Number of sessions to return (1-100). Defaults to 30.

- `pageToken` string query
  Page token from a previous ListSessions response.

#### Example Request

```
curl -H "x-goog-api-key: $JULES_API_KEY" "https://jules.googleapis.com/v1alpha/sessions?pageSize=10"
```

#### Response

```
{
  "sessions": [
    {
      "name": "1234567",
      "id": "abc123",
      "title": "Add auth tests",
      "state": "COMPLETED",
      "createTime": "2024-01-15T10:30:00Z",
      "updateTime": "2024-01-15T11:45:00Z"
    }
  ],
  "nextPageToken": "eyJvZmZzZXQiOjEwfQ=="
}
```

### Get a Session

**GET** `/v1alpha/sessions/{sessionId}`

Retrieves a single session by ID.

#### Path Parameters

- `name` **required** string path
  The resource name of the session. Format: `sessions/{session}`
  Pattern: `^sessions/[^/]+$`

#### Example Request

```
curl -H "x-goog-api-key: $JULES_API_KEY" https://jules.googleapis.com/v1alpha/1234567
```

#### Response

Returns the full [Session](#session) object including outputs if the session has completed:

```
{
  "name": "1234567",
  "id": "abc123",
  "prompt": "Add comprehensive unit tests for the authentication module",
  "title": "Add auth tests",
  "state": "COMPLETED",
  "url": "https://jules.google.com/session/abc123",
  "createTime": "2024-01-15T10:30:00Z",
  "updateTime": "2024-01-15T11:45:00Z",
  "outputs": [
    {
      "pullRequest": {
        "url": "https://github.com/myorg/myrepo/pull/42",
        "title": "Add auth tests",
        "description": "Added unit tests for authentication module"
      }
    }
  ]
}
```

### Delete a Session

**DELETE** `/v1alpha/sessions/{sessionId}`

Deletes a session.

#### Path Parameters

- `name` **required** string path
  The resource name of the session to delete. Format: `sessions/{session}`
  Pattern: `^sessions/[^/]+$`

#### Example Request

```
curl -X DELETE \
  -H "x-goog-api-key: $JULES_API_KEY" \
  https://jules.googleapis.com/v1alpha/1234567
```

#### Response

Returns an empty response on success.

### Send a Message

**POST** `/v1alpha/sessions/{sessionId}:sendMessage`

Sends a message from the user to an active session.
Use this endpoint to provide feedback, answer questions, or give additional instructions to Jules during an active session.

#### Path Parameters

- `session` **required** string path
  The resource name of the session. Format: `sessions/{session}`
  Pattern: `^sessions/[^/]+$`

#### Request Body

- `prompt` **required** string
  The message to send to the session.

#### Example Request

```
curl -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Please also add integration tests for the login flow"
  }' \
  https://jules.googleapis.com/v1alpha/1234567:sendMessage
```

#### Response

Returns an empty [SendMessageResponse](#sendmessageresponse) on success.

### Approve a Plan

**POST** `/v1alpha/sessions/{sessionId}:approvePlan`

Approves a pending plan in a session.
This endpoint is only needed when `requirePlanApproval` was set to `true` when creating the session.

#### Path Parameters

- `session` **required** string path
  The resource name of the session. Format: `sessions/{session}`
  Pattern: `^sessions/[^/]+$`

#### Example Request

```
curl -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  https://jules.googleapis.com/v1alpha/1234567:approvePlan
```

#### Response

Returns an empty [ApprovePlanResponse](#approveplanresponse) on success.

### Session States

Sessions progress through the following states:

| State | Description |
| --- | --- |
| QUEUED | Session is waiting to be processed |
| PLANNING | Jules is analyzing the task and creating a plan |
| AWAITING_PLAN_APPROVAL | Plan is ready and waiting for user approval |
| AWAITING_USER_FEEDBACK | Jules needs additional input from the user |
| IN_PROGRESS | Jules is actively working on the task |
| PAUSED | Session is paused |
| COMPLETED | Task completed successfully |
| FAILED | Task failed to complete |

## Activities

Activities represent events that occur during a session. Use the Activities API to monitor progress, retrieve messages, and access artifacts like code changes.

### List Activities

**GET** `/v1alpha/sessions/{sessionId}/activities`

Lists all activities for a session.

#### Path Parameters

- `parent` **required** string path
  The parent session. Format: `sessions/{session}`
  Pattern: `^sessions/[^/]+$`

#### Query Parameters

- `pageSize` integer query
  Number of activities to return (1-100). Defaults to 50.

- `pageToken` string query
  Page token from a previous ListActivities response.

#### Example Request

```
curl -H "x-goog-api-key: $JULES_API_KEY" "https://jules.googleapis.com/v1alpha/1234567/activities?pageSize=20"
```

#### Response

```
{
  "activities": [
    {
      "name": "1234567/activities/act1",
      "id": "act1",
      "originator": "system",
      "description": "Session started",
      "createTime": "2024-01-15T10:30:00Z"
    },
    {
      "name": "1234567/activities/act2",
      "id": "act2",
      "originator": "agent",
      "description": "Plan generated",
      "planGenerated": {
        "plan": {
          "id": "plan1",
          "steps": [
            {
              "id": "step1",
              "index": 0,
              "title": "Analyze existing code",
              "description": "Review the authentication module structure"
            },
            {
              "id": "step2",
              "index": 1,
              "title": "Write unit tests",
              "description": "Create comprehensive test coverage"
            }
          ],
          "createTime": "2024-01-15T10:31:00Z"
        }
      },
      "createTime": "2024-01-15T10:31:00Z"
    }
  ],
  "nextPageToken": "eyJvZmZzZXQiOjIwfQ=="
}
```

### Get an Activity

**GET** `/v1alpha/sessions/{sessionId}/activities/{activityId}`

Retrieves a single activity by ID.

#### Path Parameters

- `name` **required** string path
  The resource name of the activity. Format: `sessions/{session}/activities/{activity}`
  Pattern: `^sessions/[^/]+/activities/[^/]+$`

#### Example Request

```
curl -H "x-goog-api-key: $JULES_API_KEY" https://jules.googleapis.com/v1alpha/1234567/activities/act2
```

#### Response

Returns the full [Activity](#activity) object:

```
{
  "name": "1234567/activities/act2",
  "id": "act2",
  "originator": "agent",
  "description": "Code changes ready",
  "createTime": "2024-01-15T11:00:00Z",
  "artifacts": [
    {
      "changeSet": {
        "source": "sources/github-myorg-myrepo",
        "gitPatch": {
          "baseCommitId": "a1b2c3d4",
          "unidiffPatch": "diff --git a/tests/auth.test.js...",
          "suggestedCommitMessage": "Add unit tests for authentication module"
        }
      }
    }
  ]
}
```

### Activity Types

Activities have different types based on what occurred. Each activity will have exactly one of these event fields populated:

#### Plan Generated

Indicates Jules has created a plan for the task:

```
{
  "planGenerated": {
    "plan": {
      "id": "plan1",
      "steps": [
        {
          "id": "step1",
          "index": 0,
          "title": "Step title",
          "description": "Details"
        }
      ],
      "createTime": "2024-01-15T10:31:00Z"
    }
  }
}
```

#### Plan Approved

Indicates a plan was approved (by user or auto-approved):

```
{
  "planApproved": {
    "planId": "plan1"
  }
}
```

#### User Messaged

A message from the user:

```
{
  "userMessaged": {
    "userMessage": "Please also add integration tests"
  }
}
```

#### Agent Messaged

A message from Jules:

```
{
  "agentMessaged": {
    "agentMessage": "I've completed the unit tests. Would you like me to add integration tests as well?"
  }
}
```

#### Progress Updated

A status update during execution:

```
{
  "progressUpdated": {
    "title": "Writing tests",
    "description": ""
  }
}
```

#### Session Completed

The session finished successfully:

```
{
  "sessionCompleted": {}
}
```

#### Session Failed

The session encountered an error:

```
{
  "sessionFailed": {
    "reason": "Unable to install dependencies"
  }
}
```

### Artifacts

Activities may include artifacts—outputs produced during execution:

#### Code Changes (ChangeSet)

```
{
  "artifacts": [
    {
      "changeSet": {
        "source": "sources/github-myorg-myrepo",
        "gitPatch": {
          "baseCommitId": "a1b2c3d4e5f6",
          "unidiffPatch": "diff --git a/src/auth.js b/src/auth.js\n...",
          "suggestedCommitMessage": "Add authentication tests"
        }
      }
    }
  ]
}
```

#### Bash Output

```
{
  "artifacts": [
    {
      "bashOutput": {
        "command": "npm test",
        "output": "All tests passed (42 passing)",
        "exitCode": 0
      }
    }
  ]
}
```

#### Media

```
{
  "artifacts": [
    {
      "media": {
        "mimeType": "image/png",
        "data": "base64-encoded-data..."
      }
    }
  ]
}
```

## Sources

Sources represent repositories connected to Jules. Currently, Jules supports GitHub repositories. Use the Sources API to list available repositories and get details about specific sources.

Sources are created when you connect a GitHub repository to Jules through the web interface. The API currently only supports reading sources, not creating them.

### List Sources

**GET** `/v1alpha/sources`

Lists all sources (repositories) connected to your account.

#### Query Parameters

- `pageSize` integer query
  Number of sources to return (1-100). Defaults to 30.

- `pageToken` string query
  Page token from a previous ListSources response.

- `filter` string query
  Filter expression based on AIP-160. Example: 'name=sources/source1 OR name=sources/source2'

#### Example Request

```
curl -H "x-goog-api-key: $JULES_API_KEY" "https://jules.googleapis.com/v1alpha/sources?pageSize=10"
```

#### Response

```
{
  "sources": [
    {
      "name": "sources/github-myorg-myrepo",
      "id": "github-myorg-myrepo",
      "githubRepo": {
        "owner": "myorg",
        "repo": "myrepo",
        "isPrivate": false,
        "defaultBranch": {
          "displayName": "main"
        },
        "branches": [
          {
            "displayName": "main"
          },
          {
            "displayName": "develop"
          },
          {
            "displayName": "feature/auth"
          }
        ]
      }
    },
    {
      "name": "sources/github-myorg-another-repo",
      "id": "github-myorg-another-repo",
      "githubRepo": {
        "owner": "myorg",
        "repo": "another-repo",
        "isPrivate": true,
        "defaultBranch": {
          "displayName": "main"
        },
        "branches": [
          {
            "displayName": "main"
          }
        ]
      }
    }
  ],
  "nextPageToken": "eyJvZmZzZXQiOjEwfQ=="
}
```

#### Filtering

Use the `filter` parameter to retrieve specific sources:

```
# Get a specific source
curl -H "x-goog-api-key: $JULES_API_KEY" "https://jules.googleapis.com/v1alpha/sources?filter=name%3Dsources%2Fgithub-myorg-myrepo"

# Get multiple sources
curl -H "x-goog-api-key: $JULES_API_KEY" "https://jules.googleapis.com/v1alpha/sources?filter=name%3Dsources%2Fsource1%20OR%20name%3Dsources%2Fsource2"
```

### Get a Source

**GET** `/v1alpha/sources/{sourceId}`

Retrieves a single source by ID.

#### Path Parameters

- `name` **required** string path
  The resource name of the source. Format: `sources/{source}`
  Pattern: `^sources/.*$`

#### Example Request

```
curl -H "x-goog-api-key: $JULES_API_KEY" https://jules.googleapis.com/v1alpha/sources/github-myorg-myrepo
```

#### Response

Returns the full [Source](#source) object:

```
{
  "name": "sources/github-myorg-myrepo",
  "id": "github-myorg-myrepo",
  "githubRepo": {
    "owner": "myorg",
    "repo": "myrepo",
    "isPrivate": false,
    "defaultBranch": {
      "displayName": "main"
    },
    "branches": [
      {
        "displayName": "main"
      },
      {
        "displayName": "develop"
      },
      {
        "displayName": "feature/auth"
      },
      {
        "displayName": "feature/tests"
      }
    ]
  }
}
```

### Using Sources with Sessions

When creating a session, reference a source using its resource name in the `sourceContext`:

```
curl -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Add unit tests for the auth module",
    "sourceContext": {
      "source": "sources/github-myorg-myrepo",
      "githubRepoContext": {
        "startingBranch": "develop"
      }
    }
  }' \
  https://jules.googleapis.com/v1alpha/sessions
```

Use the List Sources endpoint to discover available source names, then use the Get Source endpoint to see available branches before creating a session.

## Types Reference

This page documents all data types used in the Jules REST API.

### Core Resources

#### Session

A session represents a unit of work where Jules executes a coding task.

**Session**
A session is a contiguous amount of work within the same context.

- `name` string
  Output only. The full resource name (e.g., 'sessions/{session}').

- `id` string
  Output only. The session ID.

- `prompt` **required** string
  The task description for Jules to execute.

- `title` string
  Optional title. If not provided, the system generates one.

- `state` [SessionState](#sessionstate)
  Output only. Current state of the session.

- `url` string
  Output only. URL to view the session in the Jules web app.

- `sourceContext` **required** [SourceContext](#sourcecontext)
  The source repository and branch context.

- `requirePlanApproval` boolean
  Input only. If true, plans require explicit approval.

- `automationMode` [AutomationMode](#automationmode)
  Input only. Automation mode for the session.

- `outputs` [SessionOutput](#sessionoutput) []
  Output only. Results of the session (e.g., pull requests).

- `createTime` string (google-datetime)
  Output only. When the session was created.

- `updateTime` string (google-datetime)
  Output only. When the session was last updated.

#### SessionState

Enum representing the current state of a session:

| Value | Description |
| --- | --- |
| STATE_UNSPECIFIED | State is unspecified |
| QUEUED | Session is waiting to be processed |
| PLANNING | Jules is creating a plan |
| AWAITING_PLAN_APPROVAL | Plan is ready for user approval |
| AWAITING_USER_FEEDBACK | Jules needs user input |
| IN_PROGRESS | Jules is actively working |
| PAUSED | Session is paused |
| FAILED | Session failed |
| COMPLETED | Session completed successfully |

#### AutomationMode

Enum for session automation settings:

| Value | Description |
| --- | --- |
| AUTOMATION_MODE_UNSPECIFIED | No automation (default) |
| AUTO_CREATE_PR | Automatically create a pull request when code changes are ready |

---

#### Activity

An activity represents a single event within a session.

**Activity**
An activity is a single unit of work within a session.

- `name` string
  The full resource name (e.g., 'sessions/{session}/activities/{activity}').

- `id` string
  Output only. The activity ID.

- `originator` string
  The entity that created this activity ('user', 'agent', or 'system').

- `description` string
  Output only. A description of this activity.

- `createTime` string (google-datetime)
  Output only. When the activity was created.

- `artifacts` [Artifact](#artifact) []
  Output only. Artifacts produced by this activity.

- `planGenerated` [PlanGenerated](#plangenerated)
  A plan was generated.

- `planApproved` [PlanApproved](#planapproved)
  A plan was approved.

- `userMessaged` [UserMessaged](#usermessaged)
  The user posted a message.

- `agentMessaged` [AgentMessaged](#agentmessaged)
  Jules posted a message.

- `progressUpdated` [ProgressUpdated](#progressupdated)
  A progress update occurred.

- `sessionCompleted` [SessionCompleted](#sessioncompleted)
  The session completed.

- `sessionFailed` [SessionFailed](#sessionfailed)
  The session failed.

---

#### Source

A source represents a connected repository.

**Source**
An input source of data for a session.

- `name` string
  The full resource name (e.g., 'sources/{source}').

- `id` string
  Output only. The source ID.

- `githubRepo` [GitHubRepo](#githubrepo)
  GitHub repository details.

---

### Plans

#### Plan

**Plan**
A sequence of steps that Jules will take to complete the task.

- `id` string
  Output only. Unique ID for this plan within a session.

- `steps` [PlanStep](#planstep) []
  Output only. The steps in the plan.

- `createTime` string (google-datetime)
  Output only. When the plan was created.

#### PlanStep

**PlanStep**
A single step in a plan.

- `id` string
  Output only. Unique ID for this step within a plan.

- `index` integer (int32)
  Output only. 0-based index in the plan.

- `title` string
  Output only. The title of the step.

- `description` string
  Output only. Detailed description of the step.

---

### Artifacts

#### Artifact

**Artifact**
A single unit of data produced by an activity.

- `changeSet` [ChangeSet](#changeset)
  Code changes produced.

- `bashOutput` [BashOutput](#bashoutput)
  Command output produced.

- `media` [Media](#media)
  Media file produced (e.g., image, video).

#### ChangeSet

**ChangeSet**
A set of changes to be applied to a source.

- `source` string
  The source this change set applies to. Format: `sources/{source}`

- `gitPatch` [GitPatch](#gitpatch)
  The patch in Git format.

#### GitPatch

**GitPatch**
A patch in Git format.

- `baseCommitId` string
  The commit ID the patch should be applied to.

- `unidiffPatch` string
  The patch in unified diff format.

- `suggestedCommitMessage` string
  A suggested commit message for the patch.

#### BashOutput

**BashOutput**
Output from a bash command.

- `command` string
  The bash command that was executed.

- `output` string
  Combined stdout and stderr output.

- `exitCode` integer (int32)
  The exit code of the command.

#### Media

**Media**
A media file output.

- `mimeType` string
  The MIME type of the media (e.g., 'image/png').

- `data` string (byte)
  Base64-encoded media data.

---

### GitHub Types

#### GitHubRepo

**GitHubRepo**
A GitHub repository.

- `owner` string
  The repository owner (user or organization).

- `repo` string
  The repository name.

- `isPrivate` boolean
  Whether the repository is private.

- `defaultBranch` [GitHubBranch](#githubbranch)
  The default branch.

- `branches` [GitHubBranch](#githubbranch) []
  List of active branches.

#### GitHubBranch

**GitHubBranch**
A GitHub branch.

- `displayName` string
  The branch name.

#### GitHubRepoContext

**GitHubRepoContext**
Context for using a GitHub repo in a session.

- `startingBranch` **required** string
  The branch to start the session from.

---

### Context Types

#### SourceContext

**SourceContext**
Context for how to use a source in a session.

- `source` **required** string
  The source resource name. Format: `sources/{source}`

- `githubRepoContext` [GitHubRepoContext](#githubrepocontext)
  Context for GitHub repositories.

---

### Output Types

#### SessionOutput

**SessionOutput**
An output of a session.

- `pullRequest` [PullRequest](#pullrequest)
  A pull request created by the session.

#### PullRequest

**PullRequest**
A pull request.

- `url` string
  The URL of the pull request.

- `title` string
  The title of the pull request.

- `description` string
  The description of the pull request.

---

### Activity Event Types

#### PlanGenerated

**PlanGenerated**
A plan was generated.

- `plan` [Plan](#plan)
  The generated plan.

#### PlanApproved

**PlanApproved**
A plan was approved.

- `planId` string
  The ID of the approved plan.

#### UserMessaged

**UserMessaged**
The user posted a message.

- `userMessage` string
  The message content.

#### AgentMessaged

**AgentMessaged**
Jules posted a message.

- `agentMessage` string
  The message content.

#### ProgressUpdated

**ProgressUpdated**
A progress update occurred.

- `title` string
  The title of the update.

- `description` string
  Details about the progress.

#### SessionCompleted

**SessionCompleted**
The session completed successfully.
No additional properties.

#### SessionFailed

**SessionFailed**
The session failed.

- `reason` string
  The reason for the failure.

---

### Request/Response Types

#### SendMessageRequest

**SendMessageRequest**
Request to send a message to a session.

- `prompt` **required** string
  The message to send.

#### SendMessageResponse

**SendMessageResponse**
Response from sending a message.
Empty response on success.

#### ApprovePlanRequest

**ApprovePlanRequest**
Request to approve a plan.
Empty request body.

#### ApprovePlanResponse

**ApprovePlanResponse**
Response from approving a plan.
Empty response on success.

#### ListSessionsResponse

**ListSessionsResponse**
Response from listing sessions.

- `sessions` [Session](#session) []
  The list of sessions.

- `nextPageToken` string
  Token for the next page of results.

#### ListActivitiesResponse

**ListActivitiesResponse**
Response from listing activities.

- `activities` [Activity](#activity) []
  The list of activities.

- `nextPageToken` string
  Token for the next page of results.

#### ListSourcesResponse

**ListSourcesResponse**
Response from listing sources.

- `sources` [Source](#source) []
  The list of sources.

- `nextPageToken` string
  Token for the next page of results.

  The above is the API documentation of the joules API.

  3. GITHUB TRENDING (Scraping - Free, No API)
   - Endpoint: GET https://github.com/trending?since=daily
   - Parse with BeautifulSoup: Find <article> for repo name, desc.
   - Docs: No official, community method: https://stackoverflow.com/questions/30525330/how-to-get-list-of-trending-github-repositories-by-github-api
     soup = BeautifulSoup(response.text, 'html.parser')
     repos = [a.text.strip() for a in soup.find_all('h1', {'class': 'h3 lh-condensed'})]
   - Limits: GitHub ToS allows, but rate limit via user-agent.

4. HACKER NEWS API (Official Firebase - Free, No Key)
   - Endpoints:
     - GET https://hacker-news.firebaseio.com/v0/topstories.json : Array of top 500 story IDs.
     - GET https://hacker-news.firebaseio.com/v0/item/{ID}.json : Story details (title, url).
   - Docs: https://github.com/HackerNews/API
     top_ids = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json').json()[:10]
     stories = [requests.get(f'https://hacker-news.firebaseio.com/v0/item/{id}.json').json() for id in top_ids]
     titles = [s['title'] for s in stories if s and 'github' in s.get('url', '') or 'dev' in s['title'].lower()]
   - Limits: Unlimited, but polite.

5. REDDIT API (Official - Free with User-Agent)
   - Endpoint: GET https://www.reddit.com/r/programming/top.json?sort=top&t=day&limit=10
   - Docs: https://www.reddit.com/dev/api/#GET_/r/{subreddit}/top
     Parameters:
       - sort: top (or hot, new)
       - t: day (time filter)
       - limit: 1-100
     Headers: User-Agent: your-app/1.0
     Response: JSON data.children[].data.title, selftext
   - Limits: 60 req/min, OAuth for write but read ok with UA.

6. DEV.TO FOREM API (Official - Free, No Key)
   - Endpoint: GET https://dev.to/api/articles?per_page=5&sort=-created_at
   - Docs: https://developers.forem.com/api/v0#tag/Articles
     Parameters:
       - per_page: 1-1000
       - sort: -created_at (latest)
       - tag: javascript (filter)
     Response: JSON articles[].title, description
   - Limits: 1000 req/hour.

7. HASHNODE GRAPHQL API (Official - Free, No Key for Public)
   - Endpoint: POST https://api.hashnode.com
   - Query: { feed(tag: "programming", first: 5, after: null) { edges { node { title cursor } } } }
   - Docs: https://docs.hashnode.com/quickstart/introduction
     Body: {"query": "{ feed(tag:\"programming\", first:5) { edges { node { title } } } }"}
     Response: JSON data.feed.edges[].node.title
   - Limits: Reasonable, undocumented but free tier ok.


   You might also use the stack exchange and stack overflow for the latest questions, latest problems being faced by the user and attain the user gathering. I am changing the amount of repositories being made daily. It is being made. It is being upgraded to 10 depositories, 10 private depositories, daily
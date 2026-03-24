# WHOOP API Setup Guide

This guide walks you through getting API access to your WHOOP data. It assumes you've never worked with OAuth2 before.

## Prerequisites

- A WHOOP account with an active membership
- A WHOOP device (strap or band)
- A web browser

## Step 1: Register as a Developer

1. Go to https://developer.whoop.com and log in with your WHOOP account credentials
   - Your WHOOP account IS your developer account — no separate registration needed
2. You'll be prompted to **Create a Team** (mandatory for your first app)
   - Enter a team name (anything works — e.g., "Personal Projects")
   - Click **Create Team**

## Step 2: Create an Application

1. In the Developer Dashboard, click to create a new app
2. Fill in your app details:
   - **App Name:** Something descriptive (e.g., "Workout Planner")
   - **Description:** Brief description of what it does
3. **Select Scopes** — check the data types you need access to (at least one required). For this skill, select all of these:
   - `read:recovery` — Recovery scores, HRV, resting HR
   - `read:sleep` — Sleep data and stages
   - `read:workout` — Workout data and strain
   - `read:cycles` — Daily physiological cycles
   - `read:body_measurement` — Weight, height, max HR
   - `read:profile` — Basic profile info
   - `offline` — **Critical:** enables refresh tokens for long-term access
4. **Set your Redirect URI:** `http://localhost:3030/callback`
   - For a personal/local app, localhost is fine
   - Must use HTTPS in production
5. Click **Create App**
6. Copy your **Client ID** and **Client Secret** — store them securely

You can create up to 5 apps per team.

## Step 3: Authorize and Get Your Token

### 3a. Open the Authorization URL

Open this URL in your browser (replace `YOUR_CLIENT_ID`):

```
https://api.prod.whoop.com/oauth/oauth2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:3030/callback&response_type=code&scope=offline%20read:profile%20read:recovery%20read:sleep%20read:workout%20read:cycles%20read:body_measurement&state=workout-planner
```

**What each parameter means:**
- `client_id` — your app's unique identifier
- `redirect_uri` — must exactly match what you registered
- `response_type=code` — tells WHOOP you want an authorization code
- `scope` — data permissions (URL-encoded spaces between scopes)
- `state` — anti-tampering string (can be anything)

### 3b. Log In and Grant Permission

You'll see WHOOP's login screen. Log in with your WHOOP credentials, then review and approve the permissions on the consent screen.

### 3c. Capture the Authorization Code

WHOOP redirects your browser to:
```
http://localhost:3030/callback?code=AUTHORIZATION_CODE&state=workout-planner
```

Your browser will probably show an error page — **that's expected.** Copy the `code` value from the URL bar. Move to the next step quickly — the code expires fast.

### 3d. Exchange the Code for Tokens

Run this in your terminal:

```bash
curl -X POST https://api.prod.whoop.com/oauth/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=THE_CODE_FROM_STEP_3C" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:3030/callback"
```

Response:

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "offline read:profile read:recovery read:sleep read:workout read:cycles read:body_measurement"
}
```

Save both tokens. The access token lasts about an hour; the refresh token is your long-term key.

### 3e. Verify It Works

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://api.prod.whoop.com/v2/recovery?limit=3"
```

If you see JSON with recovery scores, you're set.

## Step 4: Token Refresh

Access tokens expire hourly. To renew:

```bash
curl -X POST https://api.prod.whoop.com/oauth/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=YOUR_REFRESH_TOKEN" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

**Important details:**
- Each refresh token can only be used **once**. Always save the new refresh token from the response
- The old access token is immediately invalidated when you refresh
- If two processes try to refresh simultaneously, one will fail — the skill handles this by refreshing proactively on a schedule rather than on-demand

The workout-planner skill handles refresh automatically. Just provide the initial tokens during onboarding.

## Scopes Reference

| Scope | What It Provides | Needed For |
|-------|-----------------|------------|
| `read:recovery` | Recovery score (0-100%), HRV, resting HR, SpO2, skin temp | Primary training intensity decisions |
| `read:sleep` | Sleep duration, stages, respiratory rate, sleep performance % | Recovery assessment |
| `read:workout` | Workout type, strain, HR zones, duration, calories | Activity history and strain tracking |
| `read:cycles` | Daily physiological cycles with overall strain | Cumulative load monitoring |
| `read:body_measurement` | Height, weight, max HR | Body metrics context |
| `read:profile` | Name, email | User identification |
| `offline` | Enables refresh tokens | **Required** for long-term access |

**Recommended scope string:**
```
offline read:profile read:recovery read:sleep read:workout read:cycles read:body_measurement
```

## Rate Limits

- **100 requests per minute**
- **10,000 requests per 24 hours**
- Response headers tell you where you stand:
  - `X-RateLimit-Remaining` — requests left in current window
  - `X-RateLimit-Reset` — seconds until window resets
- If you hit 429 (Too Many Requests), wait and retry

The skill's normal usage (a few calls per morning check-in, a few more for weekly planning) is well within these limits.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Invalid redirect_uri" | Must exactly match what's registered in the dashboard |
| 401 Unauthorized | Access token expired — refresh it. Or check that you're using `Bearer TOKEN` format |
| Missing refresh token | You forgot the `offline` scope. Re-authorize with `offline` included |
| Refresh token fails | Refresh tokens are single-use. If you already used it, you need the new one from that response. If lost, re-authorize from Step 3 |
| "Invalid scope" | Check spelling and that scopes exist. Use the exact strings from the table above |
| Concurrent refresh failure | Two processes tried to refresh at the same time. Only one succeeds. Use a single scheduled refresh job |

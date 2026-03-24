# Oura Ring API Setup Guide

This guide walks you through getting API access to your Oura Ring data. It assumes you've never worked with OAuth2 before.

## Prerequisites

- An Oura Ring with an active Oura account
- An active Oura Membership (Gen3 and Ring 4 users without a membership cannot access their data via API)
- A web browser

## Step 1: Register Your Application

1. Go to https://cloud.ouraring.com and sign in with your Oura account
2. Navigate to **API Applications**
3. Click **New Application**
4. Fill in:
   - **App Name:** Something descriptive (e.g., "Workout Planner")
   - **Website URL:** Your app's URL (for personal use, anything works — e.g., `http://localhost`)
5. Set your **Redirect URI:** `http://localhost:3030/callback`
   - This is where Oura sends you back after you grant permission
   - For a personal/local app, localhost is fine
6. Save the app and copy your **Client ID** and **Client Secret** — store them somewhere safe

## Step 2: Authorize and Get Your Token

OAuth2 is a multi-step handshake. Here's what happens and how to do it:

### 2a. Open the Authorization URL

Open this URL in your browser (replace `YOUR_CLIENT_ID` with your actual Client ID):

```
https://cloud.ouraring.com/oauth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:3030/callback&scope=daily_sleep+daily_readiness+daily_activity+heartrate+workout+daily_spo2+daily_stress+personal&state=workout-planner
```

**What each parameter means:**
- `response_type=code` — tells Oura you want an authorization code
- `client_id` — your app's unique identifier
- `redirect_uri` — must exactly match what you registered (including trailing slashes or lack thereof)
- `scope` — which data you're requesting access to (see Scopes section below)
- `state` — a random string to prevent tampering (can be anything)

### 2b. Grant Permission

You'll see Oura's permission screen. Review the data access being requested and click **Allow**.

### 2c. Capture the Authorization Code

Oura redirects your browser to something like:
```
http://localhost:3030/callback?code=SOME_LONG_CODE&state=workout-planner
```

Your browser will probably show an error (since nothing is running on localhost:3030) — **that's fine.** Copy the `code` value from the URL bar. It looks like a long string of characters.

This code expires quickly (usually within a few minutes), so move to the next step right away.

### 2d. Exchange the Code for Tokens

Run this command in your terminal (replace the placeholders):

```bash
curl -X POST https://api.ouraring.com/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=THE_CODE_FROM_STEP_2C" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:3030/callback"
```

You'll get back a JSON response:

```json
{
  "access_token": "eyJ0eXAiOiJKV1Q...",
  "refresh_token": "eyJ0eXAiOiJKV1Q...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

Save both the `access_token` and `refresh_token`. The access token expires in about an hour; the refresh token is how you get a new one without repeating this whole process.

### 2e. Verify It Works

Test with a quick API call:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://api.ouraring.com/v2/usercollection/daily_readiness?start_date=$(date -d '3 days ago' +%Y-%m-%d)"
```

If you see JSON data with readiness scores, you're all set.

## Step 3: Token Refresh

Access tokens expire every hour. To get a new one without re-authorizing:

```bash
curl -X POST https://api.ouraring.com/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=YOUR_REFRESH_TOKEN" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

This returns a new access token and a new refresh token. **Important:** Each refresh token can only be used once. Always save the new refresh token from the response and discard the old one.

The workout-planner skill handles token refresh automatically when making API calls. Just provide the initial tokens during onboarding and it takes care of the rest.

## Scopes Reference

Request only the scopes you need. The user sees what you're requesting and can deny individual scopes.

| Scope | What It Provides | Needed For |
|-------|-----------------|------------|
| `daily_sleep` | Sleep score, duration, stages | Recovery-based training decisions |
| `daily_readiness` | Readiness score, HRV balance, contributors | Primary intensity decision metric |
| `daily_activity` | Activity score, calories, MET minutes | Training volume tracking |
| `heartrate` | Detailed HR time-series | Workout analysis |
| `workout` | Auto-detected and manual workouts | Activity history |
| `personal` | Age, weight, height | Body metrics context |
| `daily_spo2` | Blood oxygen levels | Illness detection |
| `daily_stress` | Stress levels | Recovery context |

**Recommended scope string for this skill:**
```
daily_sleep daily_readiness daily_activity heartrate workout personal daily_spo2 daily_stress
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Invalid redirect_uri" | Your redirect URI in the request must exactly match what's registered — case-sensitive, no trailing slash differences |
| 401 Unauthorized | Access token expired. Use the refresh token to get a new one |
| 403 Forbidden | Oura Membership may have expired. Gen3/Ring 4 require an active membership for API access |
| Refresh token fails | Refresh tokens are single-use. If you used it already, you need the new one from that response. If lost, re-do the authorization flow from Step 2 |
| Empty data returned | Check that the user granted the scopes you requested. Also verify the date range — Oura returns empty arrays for dates with no data |

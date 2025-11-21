# Instagram & Facebook Setup Guide

**Goal:** Set up Instagram Graph API access to enable automated posting from GitHub Actions.

---

## Overview

Instagram's Graph API requires a chain of connected services:

```
GitHub Actions → Instagram Graph API → Instagram Business Account → Facebook Page → Facebook App
```

**Why all this complexity?**
- Instagram is owned by Meta (Facebook)
- The Graph API is part of Facebook's developer platform
- Business/Creator accounts get API access; personal accounts don't
- A Facebook Page must be linked to "own" the Instagram account for API purposes

**Time Required:** ~30-45 minutes

---

## Prerequisites

Before starting, you'll need:
- [ ] An email address (for Facebook/Instagram accounts)
- [ ] A phone number (for verification)
- [ ] A profile picture for Instagram (optional but recommended)

---

## Step 1: Create Instagram Account (Skip if you have one)

If you already have an Instagram account you want to use, skip to Step 2.

### 1.1 Create Account

1. Go to [instagram.com](https://www.instagram.com/) or download the Instagram app
2. Click **Sign Up**
3. Enter your email or phone number
4. Create a username: `todayinemojis` (or similar)
5. Set a password
6. Complete your profile (add bio, profile picture)

### 1.2 Suggested Profile Setup

**Username:** `todayinemojis`
**Name:** Today in Emojis
**Bio:**
```
Today's vibe — in five emojis.
Feel the day. Don't read it.
🌍 todayinemojis.com
```
**Profile Picture:** Use the website favicon or a simple globe emoji image

---

## Step 2: Convert to Professional Account

Instagram has three account types:
- **Personal** - No API access
- **Creator** - API access, for influencers
- **Business** - API access, for brands (recommended)

### 2.1 Switch to Professional Account

**On Mobile App:**
1. Open Instagram app
2. Go to your **Profile** (bottom right)
3. Tap **hamburger menu** (☰) top right
4. Tap **Settings and privacy**
5. Scroll down to **Account type and tools**
6. Tap **Switch to professional account**
7. Tap **Continue** through the intro screens
8. Choose **Business** (recommended) or **Creator**
9. Select a category: **Digital Creator** or **News & Media Website**
10. Review your contact info (can skip/hide)
11. Tap **Done**

**On Desktop:**
1. Go to instagram.com and log in
2. Click your profile picture → **Settings**
3. Click **Switch to professional account**
4. Follow the same steps as mobile

### 2.2 Verify Professional Status

After switching, you should see:
- **Insights** option in your profile
- **Professional dashboard** in settings
- **Promotions** option

---

## Step 3: Create a Facebook Page

A Facebook Page is required to link with your Instagram Business account.

### 3.1 Create Facebook Account (Skip if you have one)

1. Go to [facebook.com](https://www.facebook.com/)
2. Click **Create new account**
3. Enter your details and verify

### 3.2 Create a Facebook Page

1. Log into Facebook
2. Click the **Menu** (grid icon) in the top right
3. Click **Page** under "Create"
4. Or go directly to: [facebook.com/pages/create](https://www.facebook.com/pages/create)

**Page Setup:**
- **Page name:** `Today in Emojis`
- **Category:** Choose `News & Media Website` or `App Page`
- **Bio:** `Today's vibe — in five emojis. Feel the day. Don't read it.`

5. Click **Create Page**
6. Add a profile picture and cover photo (optional but recommended)

### 3.3 Note Your Page ID

1. Go to your new Facebook Page
2. Click **About** in the left menu
3. Scroll down to find **Page ID**
4. Or look at the URL: `facebook.com/[PageName]`
5. Save this for later (you'll need it)

**Alternative way to find Page ID:**
1. Go to your Page
2. Click **Settings** (bottom left)
3. Click **Page transparency**
4. Page ID is listed there

---

## Step 4: Link Instagram to Facebook Page

This connection allows the Facebook Page to "manage" the Instagram account via API.

### 4.1 Link from Instagram

**On Mobile App:**
1. Open Instagram
2. Go to **Profile** → **Edit profile**
3. Tap **Page** under "Profile information"
4. Choose **Connect an existing Page** or **Create a Facebook Page**
5. Select your "Today in Emojis" Facebook Page
6. Tap **Done**

**On Desktop:**
1. Go to instagram.com → Profile
2. Click **Edit profile**
3. Under "Page", click **Connect**
4. Log into Facebook if prompted
5. Select your Page

### 4.2 Verify the Link

**From Facebook Page:**
1. Go to your Facebook Page
2. Click **Settings** (bottom left)
3. Click **Linked accounts** or **Instagram**
4. You should see your Instagram account connected

**From Instagram:**
1. Go to Profile → Settings → Account
2. Look for "Linked accounts" or "Sharing to other apps"
3. Facebook should show as connected

---

## Step 5: Create Facebook Developer App

This is where you'll get API credentials for automated posting.

### 5.1 Access Facebook Developers

1. Go to [developers.facebook.com](https://developers.facebook.com/)
2. Click **Log In** (top right) and use your Facebook account
3. If first time, click **Get Started** and complete the registration:
   - Accept terms
   - Verify your account (phone/email)
   - Choose "Developer" as your role

### 5.2 Create a New App

1. Go to [developers.facebook.com/apps](https://developers.facebook.com/apps/)
2. Click **Create App**
3. Select use case: **Other** (at bottom)
4. Click **Next**
5. Select app type: **Business**
6. Click **Next**
7. Fill in app details:
   - **App name:** `Today in Emojis Bot`
   - **App contact email:** Your email
   - **Business Account:** Skip or create one (optional)
8. Click **Create app**
9. Complete security check if prompted

### 5.3 Note Your App Credentials

After creating the app:

1. Go to **Settings** → **Basic** in left sidebar
2. Note down:
   - **App ID:** (e.g., `123456789012345`)
   - **App Secret:** Click "Show" and copy (keep this SECRET!)

**Important:** Never commit these credentials to your repository!

---

## Step 6: Add Instagram Graph API to Your App

### 6.1 Add the Product

1. In your app dashboard, click **Add Product** in left sidebar
2. Find **Instagram Graph API**
3. Click **Set Up**

This adds Instagram API capabilities to your app.

### 6.2 Configure Instagram Settings

1. In left sidebar, click **Instagram** → **Basic Display** (if available)
2. Or click **Instagram Graph API** → **Settings**
3. You'll configure this more in the token generation step

---

## Step 7: Generate Access Tokens

This is the most complex part. You need to generate a long-lived access token.

### 7.1 Understand Token Types

- **Short-lived token:** Expires in 1 hour (useless for automation)
- **Long-lived token:** Expires in 60 days (what we need)
- **Page access token:** For posting to Pages
- **User access token:** For accessing user data

### 7.2 Use Graph API Explorer (Easiest Method)

1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. In the top right, select your app: `Today in Emojis Bot`
3. Click **User or Page** dropdown → Select **Get User Access Token**
4. In permissions, check these boxes:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`
   - `business_management` (optional)
5. Click **Generate Access Token**
6. A popup will appear - click **Continue as [Your Name]**
7. Select the Facebook Page you created
8. Select the Instagram account
9. Click **Done**
10. Copy the generated token (this is a short-lived token)

### 7.3 Exchange for Long-Lived Token

The token from Graph Explorer expires in 1 hour. Convert it to a 60-day token:

**Method 1: Using Graph API Explorer**

1. Stay in Graph API Explorer
2. In the query field, enter:
```
GET /oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={SHORT_LIVED_TOKEN}
```

Replace:
- `{APP_ID}` with your App ID
- `{APP_SECRET}` with your App Secret
- `{SHORT_LIVED_TOKEN}` with the token you just generated

3. Click **Submit**
4. Copy the `access_token` from the response - this is your long-lived token!

**Method 2: Using curl (Terminal)**

```bash
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_TOKEN"
```

The response will contain your long-lived token:
```json
{
  "access_token": "EAAI...[long string]...",
  "token_type": "bearer",
  "expires_in": 5184000
}
```

`expires_in: 5184000` = 60 days in seconds

### 7.4 Get Page Access Token (Needed for Posting)

The user token needs to be exchanged for a Page Access Token:

1. In Graph API Explorer, use your long-lived user token
2. Make this request:
```
GET /me/accounts
```
3. Click **Submit**
4. Find your "Today in Emojis" page in the results
5. Copy the `access_token` for that page - this is your **Page Access Token**

This Page Access Token is also long-lived and what you'll use for posting.

### 7.5 Get Instagram Business Account ID

1. In Graph API Explorer, with your Page Access Token
2. Make this request:
```
GET /{PAGE_ID}?fields=instagram_business_account
```

Replace `{PAGE_ID}` with your Facebook Page ID

3. Click **Submit**
4. Copy the `id` from `instagram_business_account` - this is your **Instagram Business Account ID**

Example response:
```json
{
  "instagram_business_account": {
    "id": "17841234567890123"
  },
  "id": "123456789012345"
}
```

---

## Step 8: Verify Everything Works

### 8.1 Test API Access

In Graph API Explorer:

1. Use your Page Access Token
2. Make this request to get your Instagram account info:
```
GET /{INSTAGRAM_BUSINESS_ACCOUNT_ID}?fields=id,username,profile_picture_url,followers_count
```

You should see your Instagram account details.

### 8.2 Test Content Publishing Permission

Make this request:
```
GET /{INSTAGRAM_BUSINESS_ACCOUNT_ID}/content_publishing_limit
```

This confirms you have permission to publish content.

---

## Step 9: Add Secrets to GitHub

Now add your credentials to GitHub for the workflow to use.

### 9.1 Navigate to Repository Secrets

1. Go to your GitHub repository: `github.com/pareeksourabh/today-in-emojis`
2. Click **Settings** tab
3. In left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**

### 9.2 Add Required Secrets

Add these secrets:

**Secret 1:**
- Name: `INSTAGRAM_ACCESS_TOKEN`
- Value: Your Page Access Token (the long-lived one from Step 7.4)

**Secret 2:**
- Name: `INSTAGRAM_BUSINESS_ACCOUNT_ID`
- Value: Your Instagram Business Account ID (from Step 7.5)

### 9.3 Verify Secrets

After adding, you should see:
- `INSTAGRAM_ACCESS_TOKEN` - Updated just now
- `INSTAGRAM_BUSINESS_ACCOUNT_ID` - Updated just now

You cannot view the values after saving (for security), so make sure to save them elsewhere securely too.

---

## Step 10: Token Maintenance

### 10.1 Token Expiration

- Long-lived tokens expire after **60 days**
- Set a calendar reminder to refresh before expiration
- Instagram will NOT notify you when tokens expire

### 10.2 Refresh Token Process

To refresh before expiration:

1. Go to Graph API Explorer
2. Make this request with your current valid token:
```
GET /oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={CURRENT_TOKEN}
```
3. Get the new token
4. Exchange for Page Access Token (Step 7.4)
5. Update GitHub Secret with new token

### 10.3 Automate Token Refresh (Advanced)

You can automate this with a separate GitHub Action that runs monthly, but manual refresh is simpler to start.

---

## Troubleshooting

### Common Issues

**"Invalid OAuth access token"**
- Token has expired
- Wrong token type (user vs page)
- Solution: Generate new token following Step 7

**"Requires instagram_content_publish permission"**
- Missing permission in token
- Solution: Re-generate token with correct permissions (Step 7.2)

**"Instagram account not connected"**
- Instagram not linked to Facebook Page
- Solution: Re-link following Step 4

**"Application does not have permission for this action"**
- App not approved for content publishing
- For personal use, this usually works automatically
- For public apps, you need App Review (not required for your own account)

**"Rate limit exceeded"**
- Instagram limits: 25 posts per 24 hours
- Solution: Wait and try again

### Debug Checklist

- [ ] Instagram account is Business/Creator type
- [ ] Facebook Page exists and is published
- [ ] Instagram is linked to Facebook Page
- [ ] Facebook App has Instagram Graph API product added
- [ ] Token has `instagram_content_publish` permission
- [ ] Using Page Access Token (not User token)
- [ ] Instagram Business Account ID is correct
- [ ] GitHub secrets are set correctly

### Test Your Setup

Run this curl command to verify everything:

```bash
curl -X GET "https://graph.facebook.com/v18.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}?fields=id,username&access_token={YOUR_PAGE_ACCESS_TOKEN}"
```

You should see your Instagram username in the response.

---

## Quick Reference

### Your Credentials (Fill in after setup)

```
App ID: _______________
App Secret: _______________ (KEEP SECRET!)
Facebook Page ID: _______________
Instagram Business Account ID: _______________
Page Access Token: _______________ (KEEP SECRET!)
Token Expiration Date: _______________
```

### API Endpoints You'll Use

```
# Create media container (upload image)
POST /{ig-user-id}/media
  ?image_url={url}
  &caption={caption}
  &access_token={token}

# Publish media container
POST /{ig-user-id}/media_publish
  ?creation_id={container-id}
  &access_token={token}
```

### Useful Links

- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Instagram Graph API Docs](https://developers.facebook.com/docs/instagram-api/)
- [Content Publishing Docs](https://developers.facebook.com/docs/instagram-api/guides/content-publishing)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)

---

## Next Steps

After completing this setup:

1. **Test manually** - Use Graph API Explorer to post a test image
2. **Build scripts** - Create `generate_emoji_image.py` and `post_to_instagram.py`
3. **Integrate workflow** - Update GitHub Actions
4. **Monitor** - Watch first few automated posts

---

## Security Notes

- **Never commit tokens** to your repository
- **Use GitHub Secrets** for all credentials
- **Rotate tokens** if you suspect they're compromised
- **App Secret** is like a password - never share it
- **Limit permissions** - only request what you need

---

**Questions?** If you get stuck on any step, let me know the specific error or issue and I can help troubleshoot.

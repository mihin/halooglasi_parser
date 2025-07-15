# GitHub Actions Deployment Guide

This guide explains how to deploy the HaloOglasi parser using GitHub Actions for free, automated cloud execution.

## 🚀 Quick Setup

### 1. Fork the Repository
1. Click "Fork" button on the main repository page
2. Choose your GitHub account as the destination

### 2. Enable GitHub Actions
1. Go to your forked repository
2. Click "Actions" tab
3. Click "I understand my workflows, enable them"

### 3. Configure Secrets
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click "New repository secret"
3. Add these secrets:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | `1234567890:ABCDefghIJKLmnopQRSTuvwxyz` |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | `-1001234567890` or `123456789` |

### 4. Verify Setup
1. Go to **Actions** tab
2. Click "HaloOglasi Apartment Parser"
3. Click "Run workflow" → "Run workflow"
4. Wait 1-2 minutes and check the results

## ⏰ Schedule Details

### Default Schedule
- **Frequency**: Every 30 minutes
- **Active Hours**: 8:00 AM - 8:00 PM UTC
- **Days**: Monday through Sunday
- **Cron Expression**: `0,30 8-20 * * *`

### Timezone Considerations
The schedule uses UTC time. Here's how it maps to different timezones:

| UTC Time | Belgrade (CET/CEST) | London (GMT/BST) |
|----------|---------------------|------------------|
| 8:00-20:00 | 9:00-21:00 (winter)<br>10:00-22:00 (summer) | 8:00-20:00 (winter)<br>9:00-21:00 (summer) |

## 🔧 Customization

### Modify Schedule
Edit `.github/workflows/apartment-parser.yml`:

```yaml
on:
  schedule:
    # Run every 15 minutes during business hours
    - cron: '0,15,30,45 8-20 * * *'
    
    # Run only on weekdays
    - cron: '0,30 8-20 * * 1-5'
    
    # Run every hour, 24/7
    - cron: '0 * * * *'
```

### Change Python Version
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # Default: 3.11 (recommended for latest dependencies)
```

### Add Environment Variables
```yaml
- name: Run apartment parser
  env:
    TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
    TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
    MAX_DAYS_OLD: 7  # Override default of 2 days
    EXPORT_TO_EXCEL: true  # Enable Excel export
```

## 🔄 Persistent Apartment Tracking

The workflow automatically maintains apartment tracking between runs:

### How It Works
1. **Download previous data**: Each run downloads `previous_apartment_ids.json` from the last execution
2. **Track new apartments**: Parser identifies NEW vs PREVIOUSLY SEEN apartments
3. **Upload updated data**: Saves updated tracking file for the next run
4. **90-day retention**: Tracking data is preserved for 3 months

### Benefits
- 🎯 **Only notifies about NEW apartments** (no duplicate Telegram messages)
- 📈 **Continuous tracking** across all automated runs
- 🔒 **No external storage needed** (uses GitHub's artifact system)
- ⚡ **Fast startup** (no need to rebuild tracking from scratch)

### First Run Behavior
- On the very first run, no previous tracking data exists
- All found apartments will be marked as "NEW"
- Subsequent runs will only show truly new listings

## 📊 Monitoring

### View Execution Logs
1. Go to **Actions** tab
2. Click on any workflow run
3. Click "parse-apartments" job
4. Expand any step to see detailed logs

### Download Artifacts
Each run creates downloadable artifacts:
- **parser-logs**: Contains all log files
- **parser-data**: Contains apartment data and tracking files
- **apartment-tracking-data**: Persistent ID tracking (auto-restored between runs)

### Check Run History
- Green ✅: Successful execution
- Orange 🟡: Cancelled or skipped
- Red ❌: Failed execution

### Notification Settings
Configure GitHub to notify you of workflow failures:
1. Go to **Settings** → **Notifications**
2. Enable "Actions" notifications
3. Choose email or web notifications

## 🐛 Troubleshooting

### Common Issues

#### 1. "Invalid secrets"
**Problem**: Telegram credentials not working
**Solution**: 
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Ensure `TELEGRAM_CHAT_ID` has correct format
- Test credentials locally first

#### 2. "Workflow disabled"
**Problem**: Actions not running automatically
**Solution**:
- Go to Actions tab → Enable workflows
- Check if repository is public (private repos have usage limits)

#### 3. "Rate limiting" 
**Problem**: Too many API requests
**Solution**:
- Reduce schedule frequency (e.g., every hour instead of 30 minutes)
- The parser already includes rate limiting for Telegram

#### 4. "Quota exceeded"
**Problem**: GitHub Actions minutes limit reached
**Solution**:
- Public repositories have unlimited minutes
- Private repositories: 2000 minutes/month on free tier

### Debug Mode
Add debug environment variable:
```yaml
env:
  DEBUG: true
  TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
  TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
```

## 💰 Cost Analysis

### GitHub Free Tier
- **Public repositories**: Unlimited Actions minutes
- **Private repositories**: 2000 minutes/month
- **Storage**: 500MB for artifacts

### Usage Calculation
- Each run takes ~2-3 minutes
- Running every 30 minutes = 48 runs/day
- Daily usage: 48 × 3 = 144 minutes
- Monthly usage: 144 × 30 = 4,320 minutes

**Recommendation**: Use public repository for unlimited usage, or reduce frequency for private repos.

## 🔒 Security Best Practices

### Repository Settings
1. **Make repository public** for unlimited Actions usage
2. **Don't commit sensitive data** (credentials are in secrets)
3. **Review workflow permissions** in Settings → Actions

### Secret Management
1. **Rotate tokens** periodically
2. **Use least privilege** for Telegram bot permissions
3. **Monitor secret usage** in Actions logs

### Code Security
1. **Pin action versions** (e.g., `@v4` instead of `@main`)
2. **Review dependencies** in requirements.txt
3. **Enable Dependabot** for security updates

## 🚀 Advanced Features

### Matrix Builds
Run multiple configurations simultaneously:
```yaml
strategy:
  matrix:
    python-version: [3.10, 3.11, 3.12]
    search-criteria: [budget, premium, large]
```

### Conditional Execution
Run only when specific files change:
```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'scripts/**'
      - '.github/workflows/**'
```

### Slack Integration
Add Slack notifications:
```yaml
- name: Notify Slack
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 📈 Performance Optimization

### Caching Dependencies
```yaml
- name: Cache Python dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### Parallel Jobs
```yaml
jobs:
  parse-apartments:
    runs-on: ubuntu-latest
  
  generate-reports:
    runs-on: ubuntu-latest
    needs: parse-apartments
```

## 📞 Support

If you encounter issues:
1. Check the [troubleshooting section](#troubleshooting)
2. Review [GitHub Actions documentation](https://docs.github.com/en/actions)
3. Open an issue in the repository

The GitHub Actions deployment provides a robust, free, and maintenance-free way to run your apartment parser in the cloud! 
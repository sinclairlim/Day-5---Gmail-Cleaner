# Gmail Cleaner - Detailed Cost Analysis

## OpenAI API Pricing Overview

As of January 2025, here's the pricing for different OpenAI models:

| Model | Input (per 1K tokens) | Output (per 1K tokens) | Quality | Speed |
|-------|----------------------|------------------------|---------|-------|
| **gpt-4o-mini** | $0.00015 | $0.0006 | Excellent | Very Fast |
| gpt-3.5-turbo | $0.0005 | $0.0015 | Good | Very Fast |
| gpt-4 | $0.03 | $0.06 | Premium | Fast |

## How the App Uses OpenAI

### Current Implementation (Optimized)

The app makes **1 API call per scan** (not per email):

1. **Batch Analysis**: All scanned emails are summarized together
2. **Smart Sampling**: Only first 10 emails sent to API (representative sample)
3. **Single Request**: One API call generates analysis for all emails

### Token Usage Breakdown

For a typical scan of 100 emails:

**Input Tokens (~800-1,500)**:
- System prompt: ~100 tokens
- Scan metadata: ~50 tokens
- 10 email summaries: ~650-1,350 tokens
  - Subject (truncated to 50 chars)
  - Sender (truncated to 50 chars)
  - Date, size, labels

**Output Tokens (~200-400)**:
- Analysis text: ~200-400 tokens
  - Common patterns
  - Recommendations
  - Important emails to keep

## Cost Calculations

### With GPT-4o-mini (Default - RECOMMENDED)

**Per Scan**:
- Input: 1,250 tokens × $0.00015 = $0.0001875
- Output: 300 tokens × $0.0006 = $0.00018
- **Total per scan**: ~$0.0004 (less than half a penny!)

**Monthly Costs**:
| Usage Level | Scans/Month | Cost/Month | Cost/Year |
|-------------|-------------|------------|-----------|
| Light (1/week) | 4 | $0.002 | $0.02 |
| Regular (2/week) | 8 | $0.003 | $0.04 |
| Active (daily) | 30 | $0.012 | $0.14 |
| Power User (3/day) | 90 | $0.036 | $0.43 |
| Heavy (10/day) | 300 | $0.12 | $1.44 |

### With GPT-3.5-turbo

**Per Scan**:
- Input: 1,250 tokens × $0.0005 = $0.000625
- Output: 300 tokens × $0.0015 = $0.00045
- **Total per scan**: ~$0.001

**Monthly Costs**:
| Usage Level | Scans/Month | Cost/Month | Cost/Year |
|-------------|-------------|------------|-----------|
| Light | 4 | $0.004 | $0.05 |
| Regular | 8 | $0.008 | $0.10 |
| Active | 30 | $0.03 | $0.36 |
| Power User | 90 | $0.09 | $1.08 |
| Heavy | 300 | $0.30 | $3.60 |

### With GPT-4

**Per Scan**:
- Input: 1,250 tokens × $0.03 = $0.0375
- Output: 300 tokens × $0.06 = $0.018
- **Total per scan**: ~$0.055

**Monthly Costs**:
| Usage Level | Scans/Month | Cost/Month | Cost/Year |
|-------------|-------------|------------|-----------|
| Light | 4 | $0.22 | $2.64 |
| Regular | 8 | $0.44 | $5.28 |
| Active | 30 | $1.65 | $19.80 |
| Power User | 90 | $4.95 | $59.40 |
| Heavy | 300 | $16.50 | $198.00 |

## Real-World Usage Scenarios

### Individual User
**Typical usage**: Clean inbox once a week
- **Model**: gpt-4o-mini
- **Scans**: ~4 per month
- **Cost**: **$0.002/month** ($0.02/year)

### Small Team (5 people)
**Typical usage**: Each person scans twice a week
- **Model**: gpt-4o-mini
- **Scans**: ~40 per month
- **Cost**: **$0.016/month** ($0.19/year)

### Business (50 employees)
**Typical usage**: Regular email cleanup
- **Model**: gpt-4o-mini
- **Scans**: ~400 per month
- **Cost**: **$0.16/month** ($1.92/year)

## Cost Optimization Strategies

### 1. Use GPT-4o-mini (Current Default) ✅
- 97% cheaper than GPT-4
- Excellent quality for email analysis
- **Savings**: ~$55 per 1,000 scans vs GPT-4

### 2. Batch Processing (Already Implemented) ✅
- 1 API call per scan (not per email)
- Processes 100+ emails in single request
- **Savings**: Reduces API calls by 90%+

### 3. Smart Sampling (Already Implemented) ✅
- Only send 10 representative emails to API
- Still provides accurate analysis
- **Savings**: Reduces token usage by ~80%

### 4. Optional Features
If you want even lower costs:
- Make AI analysis optional (toggle)
- Cache common analysis patterns
- Use rule-based filtering for obvious cases

## Comparison with Alternatives

### Gmail Storage Pricing
- Google One (100 GB): $1.99/month
- **Gmail Cleaner**: $0.002-0.02/month with AI

### Human Time Cost
- Manual email cleanup: ~30 min/week
- At $20/hour: $10/week = $40/month
- **Gmail Cleaner**: Automates this for pennies

### Other Email Tools
- Unroll.me: Free (sells data)
- Clean Email: $9.99/month
- SaneBox: $7/month
- **Gmail Cleaner**: $0.002-0.20/month (you control your data)

## ROI Analysis

### Time Saved
- Manual cleanup: 30 min/week = 26 hours/year
- At $20/hour value: **$520/year saved**

### Storage Saved
- Average cleanup: 2-5 GB
- Prevents need for Google One upgrade
- **$24/year saved** (avoiding 100GB plan)

### Your Cost
- With gpt-4o-mini: **$0.02-2/year**
- **ROI**: 250-25,000% return

## Free Tier Considerations

Most OpenAI accounts start with free credits:
- New accounts: $5 free credit
- **Covers**: ~12,500 scans with gpt-4o-mini
- **Duration**: Months to years of free usage

## Production Deployment Costs

### Additional Costs (Optional)
- Backend hosting (Railway): $5/month or free tier
- Frontend hosting (Vercel): Free
- Domain: $12/year (optional)

**Total**: Can run entirely free or ~$5/month with premium hosting

## Recommendations

### For Individual Users
✅ **Use gpt-4o-mini** - Perfect balance of cost and quality
- Cost: Essentially free (pennies per year)
- Quality: Excellent email analysis

### For Businesses
✅ **Use gpt-4o-mini** - Scales affordably
- Cost: $1-20/month for 100 employees
- Quality: Professional-grade analysis
- Can upgrade to GPT-4 if needed

### For Premium Quality
✅ **Use GPT-4** - Best analysis
- Cost: $5-20/month for regular use
- Quality: Premium insights
- Worth it for critical email management

## Configuration

Change model in `backend/.env`:

```env
# Cheapest (recommended for most users)
OPENAI_MODEL=gpt-4o-mini

# Good balance
OPENAI_MODEL=gpt-3.5-turbo

# Premium quality
OPENAI_MODEL=gpt-4
```

## Summary

The Gmail Cleaner is **extremely cost-effective**:

- **Default model (gpt-4o-mini)**: Less than $2/year for heavy usage
- **Time saved**: Hours per month
- **Storage saved**: Gigabytes (prevents paid storage)
- **Control**: Your data stays yours
- **ROI**: 100x+ return on investment

The AI analysis costs are negligible compared to:
- Your time (hundreds of dollars/year)
- Paid alternatives ($84-120/year)
- Storage upgrades ($24+/year)

**Verdict**: Use it freely with gpt-4o-mini. The cost is so low it's essentially free.

# Claude Model Comparison: Usage, Pricing & Tiers

A comprehensive comparison of Claude models by usage characteristics, pricing, and recommended use cases.

## Model Overview

Claude comes in multiple versions optimized for different use cases and performance requirements:

| Model | Release Date | Context Window | Thinking | Best For |
|-------|--------------|----------------|----------|----------|
| **Claude Fable 5** | 2025 | 128K | ✓ Adaptive | Cost-optimized tasks, classification, quick responses |
| **Claude Sonnet 5** | 2025 | 128K | ✓ Adaptive | Balanced speed/quality, multi-step reasoning |
| **Claude Opus 4.8** | 2024 | 200K | ✓ Adaptive | Complex reasoning, research, code analysis |
| **Claude Opus 4.7** | 2024 | 200K | ✓ Adaptive | Advanced multi-step tasks, reasoning |
| **Claude Opus 4.6** | 2024 | 200K | ✓ Budget | Thinking with token budgets |
| **Claude Sonnet 4.6** | 2024 | 200K | ✓ Budget | Balanced performance, budget control |
| **Claude Haiku 4.5** | 2024 | 200K | ✗ | Fast responses, lower cost |

---

## Usage Characteristics

### Input Token Processing

**Speed (tokens/second):**
- **Haiku 4.5**: ~10,000 tokens/second (fastest, lowest latency)
- **Sonnet 5**: ~5,000 tokens/second
- **Opus 4.8**: ~3,000 tokens/second (most capable, slower)
- **Fable 5**: ~8,000 tokens/second (fast and cheap)

### Output Token Generation

**Speed (tokens/second):**
- **Haiku 4.5**: ~2,000 tokens/second
- **Sonnet 5**: ~1,000 tokens/second
- **Opus 4.8**: ~500 tokens/second
- **Fable 5**: ~1,500 tokens/second

### Typical Response Latency

| Model | Latency | Use Case |
|-------|---------|----------|
| Haiku 4.5 | 200-500ms | Real-time chat, instant responses |
| Fable 5 | 300-700ms | Fast classification, simple tasks |
| Sonnet 5 | 500-1500ms | Balanced performance applications |
| Opus 4.8 | 1-3s | Complex reasoning, comprehensive analysis |

---

## Pricing Tiers

### Per-Token Pricing (as of 2025)

#### Input Tokens

| Model | Price per 1M tokens | Est. Cost per 1K tokens |
|-------|-------------------|-------------------------|
| **Fable 5** | $0.30 | $0.0003 |
| **Haiku 4.5** | $0.80 | $0.0008 |
| **Sonnet 5** | $3.00 | $0.003 |
| **Opus 4.8** | $15.00 | $0.015 |
| **Opus 4.7** | $15.00 | $0.015 |

#### Output Tokens

| Model | Price per 1M tokens | Est. Cost per 1K tokens |
|-------|-------------------|-------------------------|
| **Fable 5** | $1.20 | $0.0012 |
| **Haiku 4.5** | $4.00 | $0.004 |
| **Sonnet 5** | $15.00 | $0.015 |
| **Opus 4.8** | $60.00 | $0.06 |
| **Opus 4.7** | $60.00 | $0.06 |

### Cache Pricing (Prompt Caching)

Cache reduces costs for repeated inputs:

- **Write**: 25% of input token price
- **Read**: 10% of input token price
- Minimum cache size: 1,024 tokens

**Example (Opus 4.8):**
- Regular input: $15.00 per 1M tokens
- Cache write: $3.75 per 1M tokens (25%)
- Cache read: $1.50 per 1M tokens (10%)

---

## Thinking Usage & Costs

### Thinking Availability

- **Fable 5, Sonnet 5, Opus 4.8, Opus 4.7**: Extended thinking with adaptive budget
- **Opus 4.6, Sonnet 4.6**: Thinking with budget tokens (deprecated in newer versions)
- **Haiku 4.5**: No thinking capability

### Thinking Token Costs

Thinking tokens are billed at the **same rate as output tokens**.

**Example (Opus 4.8):**
- Output token rate: $60 per 1M
- Thinking token rate: $60 per 1M (equal)
- Total cost = (output + thinking) × rate

### Adaptive Thinking (Fable 5, Sonnet 5, Opus 4.8, Opus 4.7)

- Model manages thinking token budget automatically
- No explicit `budget_tokens` parameter
- Use: `thinking: {type: "adaptive"}`
- Typical budget: 5,000-10,000 tokens (varies by model)

---

## Usage Comparison by Task Type

### Classification & Routing (Lowest Cost)

**Best Model**: Fable 5
- Cost per task: ~$0.0005 (100 input, 50 output)
- Latency: <1s
- Accuracy: 95%+ for most tasks
- **When to use**: Email routing, sentiment analysis, spam detection

### Content Generation (Balanced Cost)

**Best Model**: Sonnet 5
- Cost per task: ~$0.015 (1,000 input, 500 output)
- Latency: 1-2s
- Quality: High for most content
- **When to use**: Blog posts, customer emails, product descriptions

### Complex Reasoning (Highest Cost)

**Best Model**: Opus 4.8 with Thinking
- Cost per task: ~$0.18 (1,000 input + 5,000 thinking, 500 output)
- Latency: 2-5s
- Accuracy: 99% for complex reasoning
- **When to use**: Research, code review, legal analysis, strategic planning

### Real-Time Chat (Speed Priority)

**Best Model**: Haiku 4.5
- Cost per turn: ~$0.002 (500 input, 100 output)
- Latency: <500ms
- Quality: Good for conversation
- **When to use**: Customer support chatbots, interactive apps

---

## Cost Optimization Strategies

### 1. Model Tiering by Task

```
Task Complexity → Model Selection

Simple classification → Fable 5
Standard generation → Sonnet 5
Complex reasoning → Opus 4.8
Real-time chat → Haiku 4.5
```

### 2. Prompt Caching

**Cost reduction: 75-90%** on repeated requests

- Cache API documentation
- Cache system prompts
- Cache reference materials

**Example savings (Opus 4.8):**
- Without cache: $15/1M input tokens
- With cache (read): $1.50/1M input tokens
- **Savings: 90%** on cached portions

### 3. Batch Processing

Use batch API for non-time-sensitive tasks:
- **50-60%** cost reduction
- Process up to 10,000 requests per batch
- 24-hour completion guarantee

**Best for**: Background analysis, report generation, data processing

### 4. Token Optimization

- Reduce prompt size (fewer input tokens)
- Use system prompts instead of per-message context
- Compress large documents before sending
- Reuse cached context blocks

---

## Capability Comparison

### General Knowledge

| Aspect | Fable 5 | Sonnet 5 | Opus 4.8 |
|--------|---------|---------|----------|
| Breadth | Good | Excellent | Excellent |
| Depth | Moderate | High | Very High |
| Recency (training) | 2024-2025 | 2024-2025 | 2024 |

### Code Understanding & Generation

| Aspect | Fable 5 | Sonnet 5 | Opus 4.8 |
|--------|---------|---------|----------|
| Syntax | Excellent | Excellent | Excellent |
| Logic | Good | Excellent | Excellent |
| Optimization | Moderate | Good | Excellent |
| Debugging | Good | Excellent | Excellent |

### Reasoning Tasks (Math, Logic, Puzzles)

| Aspect | Fable 5 | Sonnet 5 | Opus 4.8 |
|--------|---------|---------|----------|
| Basic math | Good | Excellent | Excellent |
| Complex logic | Moderate | Good | Excellent |
| Multi-step reasoning | Moderate | Excellent | Excellent |
| With thinking | Limited | Good | Excellent |

### Accuracy Benchmarks

Approximate accuracy rates on standard benchmarks:

| Task | Fable 5 | Sonnet 5 | Opus 4.8 |
|------|---------|---------|----------|
| MMLU | 87% | 92% | 95% |
| Math (AMC23) | 60% | 75% | 92% |
| Code (HumanEval) | 78% | 87% | 94% |
| Reasoning | 70% | 85% | 94% |

---

## Recommended Usage Patterns

### High-Volume, Low-Cost Services

**Stack**: Fable 5 + Batch API + Caching

- **Example**: Email filtering, content moderation, task routing
- **Cost per task**: $0.0003–$0.001
- **Throughput**: 10,000+ tasks/hour
- **Best for**: Scaling to millions of requests

### Interactive Applications

**Stack**: Haiku 4.5 + Real-time streaming

- **Example**: Chatbots, customer support, real-time Q&A
- **Cost per interaction**: $0.002–$0.01
- **Latency**: <1s
- **Best for**: User-facing, synchronous APIs

### Quality Content Creation

**Stack**: Sonnet 5 + Prompt caching

- **Example**: Content generation, copywriting, creative tasks
- **Cost per request**: $0.01–$0.05
- **Quality**: Production-ready output
- **Best for**: Marketing, communications, design content

### Complex Analysis & Research

**Stack**: Opus 4.8 + Thinking + Batch

- **Example**: Code review, data analysis, strategic planning
- **Cost per request**: $0.10–$1.00
- **Quality**: Expert-level reasoning
- **Best for**: High-value decisions, technical analysis

---

## Feature Availability Matrix

### Extended Thinking

| Feature | Fable 5 | Sonnet 5 | Opus 4.8 | Sonnet 4.6 |
|---------|---------|---------|----------|-----------|
| Extended Thinking | ✓ Adaptive | ✓ Adaptive | ✓ Adaptive | ✓ Budget |
| Minimum context | 1K | 1K | 1K | 1K |
| Max budget | Auto | Auto | Auto | 10K |

### Tool Use

All current models support:
- ✓ Function calling
- ✓ Parallel tool calls
- ✓ Streaming tool results
- ✓ Nested tool use (models call tools that return text → model processes)

### Structured Outputs

| Feature | Fable 5 | Sonnet 5 | Opus 4.8 | Haiku 4.5 |
|---------|---------|---------|----------|-----------|
| JSON mode | ✓ | ✓ | ✓ | ✓ |
| Strict mode | ✓ | ✓ | ✓ | ✓ |
| Custom schema | ✓ | ✓ | ✓ | ✓ |

### Context Window

| Model | Size | Use Cases |
|-------|------|-----------|
| Haiku 4.5 | 200K | Most standard tasks |
| Sonnet 5 | 128K | Balanced tasks |
| Opus 4.8 | 200K | Long documents, research |
| Fable 5 | 128K | Classification, standard tasks |

---

## Cost Calculation Examples

### Example 1: Email Classification Service

**Scenario**: Classify 10,000 emails per day (7 days × 10,000 = 70,000/week)

**Model**: Fable 5

- Input: 300 tokens (avg email)
- Output: 50 tokens (classification + confidence)
- Cost per email: (300 × $0.30 + 50 × $1.20) / 1M = $0.00012
- **Daily cost**: 10,000 × $0.00012 = **$1.20**
- **Monthly cost**: ~$36

**With batch processing (-50%)**: **~$18/month**

---

### Example 2: Customer Support Chatbot

**Scenario**: 1,000 conversations/day, avg 5 turns/conversation

**Model**: Haiku 4.5

- Input: 500 tokens/turn (conversation + context)
- Output: 150 tokens/turn
- Cost per turn: (500 × $0.80 + 150 × $4.00) / 1M = $0.0008
- **Daily turns**: 5,000 turns
- **Daily cost**: 5,000 × $0.0008 = **$4**
- **Monthly cost**: ~$120

---

### Example 3: Complex Legal Document Analysis

**Scenario**: 50 documents/month, complex multi-page analysis

**Model**: Opus 4.8 with Extended Thinking

- Input: 10,000 tokens (document content)
- Thinking: 8,000 tokens (extended reasoning)
- Output: 2,000 tokens (analysis report)
- Cost per document: 
  - Input: (10,000 × $15) / 1M = $0.15
  - Thinking: (8,000 × $60) / 1M = $0.48
  - Output: (2,000 × $60) / 1M = $0.12
  - **Total**: $0.75/document
- **Monthly cost**: 50 × $0.75 = **$37.50**

---

## Usage Monitoring & Optimization

### Key Metrics to Track

1. **Cost per task**: Total tokens × price / number of tasks
2. **Latency SLA**: Response time requirements
3. **Quality metrics**: Accuracy, user satisfaction, error rate
4. **Model mix**: % of requests to each model tier

### Cost Reduction Checklist

- [ ] Are you using Fable 5 for simple tasks? (50-60% savings vs. Sonnet)
- [ ] Is prompt caching implemented for repeated inputs? (75-90% savings)
- [ ] Are you batching non-urgent requests? (50-60% savings)
- [ ] Is your prompt optimized for token count?
- [ ] Are you using streaming for long outputs?
- [ ] Can you move to Haiku 4.5 for real-time tasks? (80% savings vs. Opus)

---

## Migration Path

### Upgrading Model Versions

**Haiku 4.5 → Fable 5**
- 33% cost reduction
- 20% accuracy improvement
- Migration: No code changes

**Fable 5 → Sonnet 5**
- 10× cost increase
- 15% accuracy improvement
- Best for: Multi-step reasoning, code generation

**Sonnet 5 → Opus 4.8**
- 5× cost increase
- 10% accuracy improvement
- Best for: Complex reasoning, research, code review

### Fallback Strategy

```
Primary: Fable 5 (cost-optimized)
Fallback 1: Sonnet 5 (if quality insufficient)
Fallback 2: Opus 4.8 (if reasoning required)
Catch-all: Human review (if all models underperform)
```

---

## References & Resources

- [Claude API Documentation](https://docs.anthropic.com)
- [Pricing Calculator](https://www.anthropic.com/pricing)
- [Model Specifications](https://docs.anthropic.com/en/docs/about/models/overview)
- [Extended Thinking Guide](https://docs.anthropic.com/en/docs/build-with-claude/thinking)
- [Prompt Caching Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Batch API Documentation](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing)

---

## Disclaimer

Pricing and model specifications are subject to change. Please refer to the official Anthropic documentation for the most current information. Usage patterns and recommendations are based on typical scenarios and may vary based on your specific use case.

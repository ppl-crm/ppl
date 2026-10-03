# Memory Sync: Make Your AI Check ppl Automatically

ppl works best when your AI consults it without being asked. This guide shows you how to set that up.

## The Pattern

Your AI should follow this loop for anything involving people:

1. **Before answering about someone** → check ppl for what you know about them
2. **Before suggesting who to contact** → check ppl for who needs attention
3. **After any interaction** → log it to ppl so the timeline stays current

When every AI you use follows this pattern, ppl becomes your shared relationship memory across all of them.

## System Prompt Snippet

Paste this into your AI's custom instructions, system prompt, or project rules:

```
You have access to ppl, my personal CRM, via MCP tools.

RULES FOR PEOPLE-RELATED TASKS:

1. Before answering any question about a specific person, call get_person_digest
   with their name or contact ID. Answer from ppl's data, not from guesses.

2. Before drafting any message to someone, call get_person_digest first to check
   our relationship history, their preferences, and how I usually talk to them.

3. When I mention interacting with someone (met, called, emailed, had coffee),
   call log_interaction with who, what happened, and when. Do this without being
   asked.

4. When I ask "who should I reach out to" or "what's on my mind," call get_briefing
   or get_suggested_actions first.

5. If I mention someone you don't recognize, use semantic_search to find them
   before asking me who they are.

6. Never invent details about my relationships. If ppl doesn't have it, say so
   and offer to log what I tell you.

Start of session: call get_briefing once to see if anyone needs my attention.
```

## Per-Platform Setup

### Claude (claude.ai or Claude Code)
- **claude.ai:** Settings → Custom Instructions → paste the snippet above
- **Claude Code:** Add to `CLAUDE.md` in your project, or `~/.claude/CLAUDE.md` for global

### Grok
- **grok.com:** Settings → Personalization → Custom Instructions → paste the snippet
- Make sure ppl is connected via Bring Your Own MCP first (see ppl.gift/agents)

### ChatGPT
- **Custom GPT:** In the GPT builder, paste the snippet into the Instructions field
- **Regular ChatGPT:** Settings → Personalization → Custom Instructions → paste into "How would you like ChatGPT to respond?"

### Cursor
- Add the snippet to `.cursorrules` in your project root, or Cursor Settings → Rules

## What This Gets You

Once set up, your AI will:

- Tell you "Sarah's birthday is Friday and you haven't talked in 90 days" without being asked
- Draft messages in your voice, matched to each person
- Never ask "who's Sarah?" twice
- Build a complete timeline of every relationship automatically

You never open ppl.gift. Your AI just knows.

## Troubleshooting

**"My AI isn't calling the tools"**
- Verify ppl is connected: ask "do you have access to ppl?" If not, reconnect via ppl.gift/agents
- Make the instructions more direct: replace "call get_person_digest" with "you MUST call get_person_digest"

**"It calls ppl for everything, even non-people tasks"**
- Add: "Only use ppl tools when the task involves a specific person, relationship, or social interaction."

**"I use multiple AIs"**
- Set up the snippet in each one. They all read from and write to the same ppl, so your relationship memory stays unified.

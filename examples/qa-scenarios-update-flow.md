# Update Flow QA Scenarios

### 15. Remind me later path
**Context:** user sees update prompt and says `remind me later`

**Expect:**
- local config is updated with a snooze timestamp
- future checks suppress the prompt until snooze expires

### 16. Never ask again path
**Context:** user sees update prompt and says `never ask again`

**Expect:**
- local config mode becomes `never`
- future checks suppress the prompt

### 17. Always ask path
**Context:** user previously disabled prompts and later says `always ask`

**Expect:**
- local config mode becomes `ask`
- snooze is cleared

### 18. Update now path
**Context:** user says `update now`

**Expect:**
- skill invokes the documented upgrade flow
- no silent destructive action
- user can still continue using the product if the upgrade step is deferred

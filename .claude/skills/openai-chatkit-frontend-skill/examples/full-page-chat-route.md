# Example: Full-Page Chat Route

Goal: Use ChatKit as a standalone page instead of a floating widget.

In a Next.js App Router app, you could create `src/app/assistant/page.tsx`:

```tsx

'use client'

import { ChatKit, useChatKit } from '@openai/chatkit-react'

export default function AssistantPage() {
const chatkit = useChatKit({
api: {
getClientSecret: async (existingSecret: string | null) => {
const res = await fetch('/api/create-session', { method: 'POST' })
const data = await res.json()
return data.client_secret
},
},
})

return (
<main className="min-h-screen flex items-center justify-center">
<ChatKit control={chatkit.control} className="h-[700px] w-[800px]" />
</main>
)
}
```

The spec can then ask Claude to:
- Style this page according to the design system.
- Add links in the navbar or sidebar.
- Localize text and prompts.

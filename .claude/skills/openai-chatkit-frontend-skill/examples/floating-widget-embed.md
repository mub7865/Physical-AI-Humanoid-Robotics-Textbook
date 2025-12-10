# Example: Floating ChatKit Widget in Next.js

Goal: Show a floating button + chat panel pattern using ChatKit in a Next.js app. [web:29][web:35]

## Widget component (client)

Create a reusable widget component such as `src/components/ChatKitWidget.tsx`:

```tsx
'use client'

import { useState, useCallback } from 'react'
import { ChatKit, useChatKit } from '@openai/chatkit-react'

const CHATKIT_API_URL = '/api/create-session'

export function ChatKitWidget() {
const [isOpen, setIsOpen] = useState(false)

const handleResponseEnd = useCallback(() => {
console.log('AI response completed')
}, [])

const handleError = useCallback(({ error }: { error: Error }) => {
console.error('ChatKit error:', error)
}, [])

const getClientSecret = useCallback(
async (existingSecret: string | null) => {
const res = await fetch(CHATKIT_API_URL, {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
})
if (!res.ok) throw new Error('Failed to create ChatKit session')
const { client_secret } = await res.json()
return client_secret as string
},
[],
)

const chatkit = useChatKit({
api: { getClientSecret },
// Theme and config can be customized per project spec
theme: { colorScheme: 'light' },
startScreen: { greeting: 'Hi! Ask me anything.', prompts: [] },
composer: { placeholder: 'Type your question…' },
onResponseEnd: handleResponseEnd,
onError: handleError,
})

return (
<>
<button
onClick={() => setIsOpen(!isOpen)}
aria-label={isOpen ? 'Close chat' : 'Open chat'}
>
Chat
</button>

text
  {isOpen && (
    <div className="chatkit-panel">
      <ChatKit control={chatkit.control} className="h-[500px] w-[360px]" />
    </div>
  )}
</>
)
}
```


## Root layout integration

In Next.js App Router, mount the widget and load the ChatKit script in `src/app/layout.tsx`:

```tsx 
import Script from 'next/script'
import { ChatKitWidget } from '@/components/ChatKitWidget'

export default function RootLayout({ children }: { children: React.ReactNode }) {
return (
<html lang="en">
<body>
{children}
<ChatKitWidget />
<Script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" strategy="afterInteractive" />
</body>
</html>
)
}
```


This pattern can be cloned into any project by changing only:
- Component paths
- Styling classes
- API route name.

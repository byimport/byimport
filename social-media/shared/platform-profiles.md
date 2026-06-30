# Platform Profiles

Platform-specific constraints, optimal practices, and engagement patterns.
Loaded on demand by the social-media skill when adapting content for a specific platform.

---

## Twitter / X

- **Character limit:** 280 per post (URLs count as 23 chars regardless of actual length)
- **Thread support:** yes — number posts as 1/n, 2/n…; max 25 posts per thread
- **Hashtags:** 1–2 max; more than 2 hurts engagement on X
- **Images:** 1–4 per post; max 5 MB JPG/PNG; 16:9 or 1:1 for best display
- **Video:** max 2 min 20 sec; MP4/MOV; max 512 MB
- **Alt text:** always set for images (accessibility + algo)
- **Best posting times:** Tue–Thu, 8–10am and 6–9pm (account's local timezone)
- **Tone:** direct, opinionated, punchy; humor and hot takes perform well; avoid corporate-speak
- **Engagement hook:** ask a binary question ("agree or disagree?") or make a bold statement — invites replies
- **Link placement:** in the body, not a separate reply; X shortens all URLs to t.co
- **Algo signal:** early replies (first 30 min) and quotes boost distribution more than likes

---

## Instagram

- **Caption limit:** 2,200 characters; only the first ~125 are shown before "more" — the hook must be in those first 125
- **Hashtags:** 5–30; optimal sweet spot is 8–15; blend: 2–3 broad (>1M posts) + 4–6 mid (100K–1M) + 4–6 niche (<100K)
- **Image formats:** Portrait 4:5 (1080×1350 px) gets the most feed real estate; Square 1:1; Landscape 1.91:1 for links
- **Carousel:** 2–10 slides; last slide always has a CTA; carousels earn the highest saves (saves = strong ranking signal)
- **Reels:** ≤ 90 sec for reach; 7–15 sec for virality; 9:16 vertical; add text overlays for silent viewing; hook in first 3 sec
- **Stories:** 24h lifespan; use polls / questions / sliders for engagement boosts
- **Best posting times:** Mon–Fri, 9–11am and 7–9pm (audience's local timezone)
- **Tone:** warm, authentic, aspirational; storytelling outperforms pure promotion
- **Engagement window:** reply to every comment within the first 60 min — Instagram's algo weights this heavily
- **Link rule:** no clickable links in captions; always say "link in bio" and update bio link
- **CTA patterns:** "save this," "tag a friend," "share to your story" — all drive ranking signals

---

## Facebook

- **Post character limit:** 63,206; sweet spot is 40–80 words for feed posts
- **Hashtags:** 0–3; hashtags matter far less on Facebook than other platforms
- **Images:** JPG/PNG; 1200×628 px for link preview cards; max 30 MB
- **Native video:** gets ~3× the organic reach of a link post; ideal length 1–3 min
- **Live video:** notifies followers; sustained higher reach while live
- **Best posting times:** Tue–Thu, 9am–1pm
- **Tone:** conversational, community-focused; questions that invite comments work well
- **Engagement window:** first hour of comments is critical for organic reach
- **Link cards:** Facebook auto-generates a preview card from the URL — remove the raw link from the post body after the card loads to keep it clean
- **CTA patterns:** "comment below," "tag a friend," "share if you agree"

---

## LinkedIn

- **Post limit:** 3,000 characters (personal); 700 characters (company pages)
- **Article limit:** 125,000 characters (LinkedIn articles)
- **Hashtags:** 3–5; use industry-specific tags; LinkedIn suggests tags — follow those suggestions
- **Document posts:** PDF files render as carousels — very high engagement for B2B; max 300 pages / 100 MB
- **Best posting times:** Tue–Thu, 7–9am and 5–6pm (business days only; avoid weekends)
- **Tone:** professional but personal; share insights, lessons, failures, behind-the-scenes; avoid pure sales content
- **Engagement window:** first 90 min determine reach — reply to every comment in that window
- **Link rule:** posts with external links in the body are suppressed by the algo — put the link in the FIRST COMMENT instead, and reference "link in the comments" in the post body
- **Format that works:** short line breaks (one sentence per line), no walls of text, bold opening line with a hook
- **CTA patterns:** "What's your experience with X?" (open question), "Drop a comment if this resonates"

---

## TikTok

- **Caption limit:** 2,200 characters; first 100 shown without expansion
- **Hashtags:** 3–8; include at least 1 trending tag + 2 niche tags
- **Video:** 15 sec – 10 min; 7–15 sec performs best for reach; 1–3 min for storytelling; 9:16 vertical; max 287.6 MB MP4/MOV
- **Hook rule:** first 3 seconds are make-or-break — open with a question, a surprising statement, or action
- **Sound:** trending audio dramatically increases discovery; use TikTok's sound picker to find trending tracks
- **Text overlays:** essential — most TikTok is watched without sound
- **Best posting times:** Tue–Thu, 7–9am and 7–11pm; Fri 5pm–9pm
- **Tone:** energetic, raw, genuine; overproduced content underperforms organic-feeling clips
- **Engagement tactics:** stitch and duet for discovery; reply to comments with a video response (high algo signal)
- **Connector:** `~~zapier` (TikTok posting Zap) or `~~ifttt` if TikTok is a connected service

---

## Pinterest

- **Pin description:** 500 characters; first 50–75 shown in feed
- **Hashtags:** 2–5; Pinterest treats them as category signals, not reach boosters
- **Image ratio:** 2:3 (1000×1500 px) is the standard; square also works
- **Best posting times:** Sat–Sun 8–11pm; weekdays 2–4pm and 8–11pm
- **Tone:** inspirational, how-to, aspirational; every pin should solve a problem or inspire action
- **Rich pins:** enable Rich pins (product, article, recipe) for extra metadata and distribution
- **Description format:** read like instructions or a benefit statement; include keywords naturally for Pinterest SEO
- **IFTTT action:** `create_a_pin` (service: `pinterest`)

---

## Threads (Meta)

- **Character limit:** 500 per post
- **Hashtags:** 0–3 (Threads hashtag system is still developing; use sparingly)
- **Images:** 1–10 per post; JPG/PNG
- **Tone:** casual, conversational, unpolished; closer to X than Instagram
- **Engagement tactics:** reply frequently; Threads surfaces accounts that participate in conversations
- **Connector:** `~~meta-social` (Graph API Threads endpoint if enabled) or `~~ifttt`

---

## YouTube (Community Posts)

- **Post limit:** 5,000 characters
- **Hashtags:** 3–5
- **Best for:** polls, sneak peeks, behind-the-scenes content, announcements to existing subscribers
- **Images:** supported; JPG/PNG; 16:9 recommended
- **Tone:** match the channel's established tone; community posts reward consistency with the video content
- **Connector:** `~~ifttt` or `~~zapier`

# Getting started

From sitting down to building.

## 1. Get the files

Pick whichever fits your team. You can switch later.

**Option A: a team repo on GitHub.** Best if anyone on the team will write code. One person does
this:

1. On this repo's GitHub page, choose **Use this template**, then **Create a new repository**.
2. Name it for your team, set it to **Public**, and create it. Judges need to see it.
3. Add your teammates under Settings, then Collaborators.
4. Everyone gets a copy: `git clone https://github.com/YOUR-NAME/YOUR-REPO.git`, or
   **Code**, then **Open with GitHub Desktop**.

Keep the license file. When you start writing about your project, replace the top-level
`README.md` with [`templates/TEAM-README.md`](../templates/TEAM-README.md).

**Option B: download a ZIP.** Fastest if nobody on the team uses GitHub. On this repo's page,
choose **Code**, then **Download ZIP**, and unzip it. You still need one public GitHub repo by
2:30 PM to submit; an organizer can help you make it in five minutes.

## 2. Pick how you work with Claude

All three work for every lane.

| | How | Good for |
|---|---|---|
| **In the browser** | Open [claude.ai](https://claude.ai), start a project, and add the files for your lane | Teams that do not code |
| **Claude Code in the desktop app** | Install the [Claude app](https://claude.ai/download), open Claude Code and choose your folder | Building without a terminal |
| **Claude Code in a terminal** | Install from [claude.com/claude-code](https://claude.com/claude-code), then run `claude` in your folder | Developers |

Claude Code reads [`CLAUDE.md`](../CLAUDE.md) when it starts, so it already knows the event rules
and where the data is. In the browser, add `CLAUDE.md` to your project too.

## 3. Claim your credits

$100 in Claude API credits per person (API only, not Claude.ai). The claim link is on the hub at
9:15 AM: <https://claudesocal.com/uci-impact-lab> (`#credits`).

- Claim using your **Org ID** from [console.anthropic.com](https://console.anthropic.com), not
  your Claude.ai ID.
- One claim per person.
- Credits are tied to the email you registered with. People who registered on the day may not
  get them. If that is you, tell an organizer.

## 4. Register your team

By 10:00 AM, on the hub: <https://claudesocal.com/uci-impact-lab> (`#teams`). One person
registers everyone: each teammate's name, email and role. The four roles are builder/engineer,
creative/designer, communicator/presenter and organizer/facilitator; the best teams cover all
four. Still short a role? Mark what you are looking for and the team shows on the board for
people in the room to find. Picking a lane is optional at this point; decide together and update
the team later. Pick a room for the team on the hub (rooms fill up, so register early), then go
there together.

## If you do not write code

You are needed. Teams with someone who knows the work build better things. You can:

- Be the real user. What would a nonprofit lead, a permit tech or a first-time buyer try first?
- Read every output and say what is wrong with it.
- Check each source and each number. Is it real? Is it current?
- Write the words on the screen in plain language.
- Make the 30-second video and run the demo.

You can also build. Describe what you want to Claude in plain words and it will write the code.

## Keep your work safe

- Commit and push often.
- Keep API keys in environment variables. `.env` is already in `.gitignore`.
- No personal information about real people. See the [ground rules](ground-rules.md).

## Submit by 2:30 PM

See [submission.md](submission.md).

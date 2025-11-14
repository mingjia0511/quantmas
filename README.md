```text
________                       __                         
\_____  \  __ _______    _____/  |_  _____ _____    ______
 /  / \  \|  |  \__  \  /    \   __\/     \\__  \  /  ___/
/   \_/.  \  |  // __ \|   |  \  | |  Y Y  \/ __ \_\___ \ 
\_____\ \_/____/(____  /___|  /__| |__|_|  (____  /____  >
       \__>          \/     \/           \/     \/     \/ 
```

# 🎅✨ **Happy Quantmas, Brave Elves!**

Welcome, dear friends, to the annual **GEIC — Glacial ELF Investment Corporation**
**🎄 Quantmas Challenges! 🎄**

This is the season when the North Pole’s finest quants, coders, and agent-tamers gather together to test their logic, creativity, and winter-fuelled brilliance.

Grab your peppermint tea, dust off your GPUs, and let's get magical. ❄️🧝‍♂️💻

---

# 🦌 **How Quantmas Works**

Quantmas only comes **once a year**, and during this jolly time the mighty **GEIC** calls upon *you* to solve a series of increasingly challenging financial-AI quests.

Each challenge aims to help you:

### 🎁 1. **Level Up Your AI Skills**

You are *strongly* encouraged to use AI coding agents. We’ll provide starter AGENT files and an environment to build from.

### 🧠 2. **Flex Your Winter Wits**

These are not ordinary coding problems—there is **no single correct answer**.
You will be competing against your fellow elves for glory, creativity, and style points.

### 🧹 3. **Keep Things North-Pole Clean**

Even though agents are involved, you must ensure your code stays clean, safe, and well-tested.
Rogue agents get coal. 🧊

---

# 🎄 **Challenge Structure**

A new problem drops every **4–5 days**. Each one builds on the last, leading you deeper into the Quantmas spirit.

Problems follow a consistent structure:

```
/problems
 └── year_1/
      ├── data/
      │    └── ref_data.csv
      ├── problem.md
      └── sample_output.json
```

---

# 📦 **Submissions**

## 🎅 Code Expectations

Your solution should result in one or more **JSON output files**, but we also care deeply about **how** you got there.

Every submission must include:

### 🧩 Source Code

* Supported languages: **Java**, **Python**, **TypeScript**, **.NET**
* Must live in:

  ```
  implementation/src/
  ```

### 🧪 Tests (≥ 80% coverage)

* All tests go in:

  ```
  implementation/test/
  ```

### 📚 Documentation

* Your agent + human-readable docs live in:

  ```
  implementation/docs/
  ```
* Make them helpful. Agents read too. Probably.

### 📖 README

* Include steps to run and reproduce outputs:

  ```
  implementation/README.md
  ```

> 💡 *Tests, documentation, and CodeQL quality are part of your score.
> Your `AGENTS.md` must guide your agent like a wise Christmas mentor.*

---

# 🎁 **Result Files**

We cannot execute code internally, so you must run your solution locally and commit the generated `.json` outputs.

All problem outputs must be placed here:

```
/problems/[YEAR]/output/
```

Once ready, run the festive submit script:

```bash
bash ./test-and-submit.sh
```

> 🎄 **Pro Tip:** Submit as many times as you like while the challenge window is open.
> Santa believes in second chances (and third, and fourth…).


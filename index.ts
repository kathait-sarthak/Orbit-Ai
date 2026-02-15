import { execSync } from "child_process"
import * as readline from "readline"
import { GoogleGenerativeAI } from "@google/generative-ai"
import chalk from "chalk"
import * as dotenv from "dotenv"
import os from "os"
import path from "path"
import fs from "fs"

dotenv.config({ path: path.resolve(process.cwd(), ".env") })

const API_KEY = process.env.GEMINI_API_KEY

if (!API_KEY) {
  console.error(
    chalk.red.bold("\n[!] FATAL ERROR: GEMINI_API_KEY not found in .env file."),
  )
  process.exit(1)
}

const genAI = new GoogleGenerativeAI(API_KEY)
// PRIMARY MODEL: Gemini 3 Flash
const model = genAI.getGenerativeModel({
  model: "models/gemini-3-flash-preview",
})

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
})
const askQuestion = (query: string): Promise<string> =>
  new Promise((res) => rl.question(query, res))

let currentWorkingDirectory = process.cwd()

/**
 * PHASE 1: THE BRAIN (With Automatic Retry/Backoff)
 */
async function generatePlan(userGoal: string, attempt = 1): Promise<any[]> {
  const prompt = `
    You are Orbit-AI Project Manager. System: Windows (PowerShell).
    Goal: "${userGoal}"
    
    STRICT RULES:
    1. COMMAND SEPARATOR: Use ";" (semicolon) to chain commands, NEVER "&&".
    2. VENV: Use "python -m venv venv".
    3. JSON SCHEMA: Return ONLY a raw JSON array of objects: 
       [{"type":"shell","command":"..."},{"type":"write","path":"...","content":"..."}]
    4. NO CHAT: Do not provide explanations or markdown.
  `

  try {
    const result = await model.generateContent(prompt)
    let rawText = result.response.text().trim()

    const start = rawText.indexOf("[")
    const end = rawText.lastIndexOf("]")
    if (start === -1) throw new Error("No JSON roadmap detected.")

    return JSON.parse(rawText.substring(start, end + 1))
  } catch (err: any) {
    // Check for 503 (Service Unavailable) or 429 (Rate Limit)
    if (
      (err.message.includes("503") || err.message.includes("429")) &&
      attempt <= 3
    ) {
      const waitTime = Math.pow(2, attempt) * 1000 // 2s, 4s, 8s
      console.log(
        chalk.yellow(
          `\n[!] Brain is overloaded (503/429). Retrying in ${waitTime / 1000}s... (Attempt ${attempt}/3)`,
        ),
      )
      await new Promise((res) => setTimeout(res, waitTime))
      return generatePlan(userGoal, attempt + 1)
    }

    console.error(chalk.red(`\n[!] Brain Sync Error: ${err.message}`))
    return []
  }
}

/**
 * PHASE 2: THE EXECUTOR
 */
async function executeProject(goal: string) {
  const plan = await generatePlan(goal)
  if (plan.length === 0) return

  console.log(chalk.cyan(`\nPlan Ready: ${plan.length} steps.`))
  const deploy = await askQuestion(chalk.whiteBright("Deploy Project? (y/n): "))
  if (deploy.toLowerCase() !== "y") return

  for (const step of plan) {
    try {
      if (step.type === "write") {
        const fullPath = path.resolve(currentWorkingDirectory, step.path)
        const dir = path.dirname(fullPath)
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true })
        fs.writeFileSync(fullPath, step.content)
        console.log(chalk.green(`  [FILE] Written: ${step.path}`))
      } else if (step.type === "shell") {
        let cmd = step.command
        if (os.platform() === "win32") {
          cmd = cmd.replace(/\//g, "\\")
          cmd = cmd.replace(/ && /g, " ; ") // Force PowerShell compatibility
        }

        console.log(chalk.yellow(`  [EXEC] > ${cmd}`))

        if (cmd.startsWith("cd ")) {
          const target = cmd.substring(3).trim().replace(/["']/g, "")
          currentWorkingDirectory = path.resolve(
            currentWorkingDirectory,
            target,
          )
          if (!fs.existsSync(currentWorkingDirectory))
            fs.mkdirSync(currentWorkingDirectory, { recursive: true })
          process.chdir(currentWorkingDirectory)
          continue
        }

        execSync(cmd, {
          cwd: currentWorkingDirectory,
          stdio: "inherit",
          shell: "powershell.exe",
        })
      }
    } catch (e: any) {
      console.log(chalk.red(`  [!] Step failed: ${e.message}`))
    }
  }
  console.log(chalk.magenta.bold("\n✔ Orbit-AI Deployed Successfully."))
}

async function startLoop() {
  while (true) {
    const input = await askQuestion(chalk.blue.bold("\nOrbit-AI > "))
    if (input.toLowerCase() === "exit") break
    if (input.trim()) await executeProject(input)
  }
  rl.close()
}

console.clear()
console.log(
  chalk.bold.magenta("=== ORBIT-AI STARTUP ENGINE (V3.0-RESILIENT) ==="),
)
startLoop()

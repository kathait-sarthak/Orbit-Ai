import chalk from "chalk"

/**
 * Logic to identify dangerous shell patterns
 */
export enum RiskLevel {
  SAFE = "SAFE",
  WARNING = "WARNING",
  DANGEROUS = "DANGEROUS",
}

const DANGER_PATTERNS = [
  /rm\s+-rf\s+\//, // Wipes root directory
  /:\(\)\{.*:\|:&\};:/, // Fork bomb (system crasher)
  /mkfs\..*/, // Formatting drives
  />\s*\/dev\/sd[a-z]/, // Overwriting hard drives
  /dd\s+if=\/dev\/zero/, // Wiping disks
  /chmod\s+-R\s+777\s+\//, // Breaking system permissions
  /mv\s+.*\s+\/dev\/null/, // Deleting data via null device
]

const WARNING_KEYWORDS = [
  "rm",
  "sudo",
  "shutdown",
  "reboot",
  "kill",
  "iptables",
  "del",
  "format",
]

export function analyzeCommand(command: string): {
  level: RiskLevel
  reason?: string
} {
  // 1. Check for Catastrophic Patterns
  for (const pattern of DANGER_PATTERNS) {
    if (pattern.test(command)) {
      return {
        level: RiskLevel.DANGEROUS,
        reason: "Catastrophic system command detected.",
      }
    }
  }

  // 2. Check for High-Privilege or Destructive Keywords
  const words = command.toLowerCase().split(/\s+/)
  for (const word of words) {
    if (WARNING_KEYWORDS.includes(word)) {
      return {
        level: RiskLevel.WARNING,
        reason: `Command uses sensitive keyword: [${word}]`,
      }
    }
  }

  return { level: RiskLevel.SAFE }
}

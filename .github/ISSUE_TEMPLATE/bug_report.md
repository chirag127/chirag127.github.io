---
name: Bug Report
about: Report a reproducible bug in the project.
title: "[BUG]"
labels: bug
assignees: "chirag127"

body:
  - type: markdown
    attributes:
      value: |+
        ### 🐛 Bug Report
        Thank you for helping us improve! Please provide as much information as possible to help us reproduce the bug.

        **Project Repository:** [PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit](https://github.com/chirag127/PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit)

        --- 
  - type: input
    id: system-info
    attributes:
      label: System Information
      description: Please provide details about your operating system, shell, and relevant software versions.
      placeholder: e.g., Ubuntu 22.04, Zsh 5.9, Python 3.11.5, Google Gemini API key configured
    validations:
      required: true
  - type: input
    id: prfusion-version
    attributes:
      label: PRFusion Version
      description: What version of PRFusion are you using? (e.g., `pip show prfusion`)
      placeholder: e.g., 0.1.0
    validations:
      required: false
  - type: input
    id: command-line
    attributes:
      label: Command Line
      description: What command did you run that triggered the bug?
      placeholder: e.g., `prfusion batch-pr --repo owner/repo --title "My PR Title"`
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Detailed Description
      description: Please provide a clear and concise description of the bug.
      placeholder: What is the expected behavior? What is the actual behavior?
    validations:
      required: true
  - type: textarea
    id: steps-to-reproduce
    attributes:
      label: Steps to Reproduce
      description: Provide a step-by-step guide on how to reproduce the bug. Be specific!
      placeholder: |
        1. Go to '...' 
        2. Click on '....'
        3. Scroll down to '....'
        4. See error
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Log Output (Optional)
      description: If applicable, paste any relevant log output here. Use markdown code blocks for formatting.
      placeholder: |
        
        [Log output here]
        
    validations:
      required: false
  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots/Recordings (Optional)
      description: If possible, add screenshots or a screen recording to help explain your problem.
    validations:
      required: false
  - type: markdown
    attributes:
      value: |+
        --- 
        **AI Agent Directives Verification:**
        All interactions with the PRFusion CLI should align with the established AI Agent Directives found in the repository's [AGENTS.md](https://github.com/chirag127/PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit/blob/main/AGENTS.md). Please ensure your bug report accurately reflects the expected behavior as defined by these directives.

# Universal Tool Generation Prompt

**Objective**: Create a single HTML file for a new client-side tool that integrates into the Chirag Hub ecosystem.

**Instructions**:
1.  **Single File**: The output must be a single `index.html` file.
2.  **Universal Engine**: You MUST include the following scripts in the `<head>`:
    ```html
    <script src="https://chirag127.github.io/universal/config.js"></script>
    <script src="https://chirag127.github.io/universal/core.js"></script>
    ```
    *Do NOT include any analytics, headers, footers, or global styles manually.* The Engine handles all of that.
3.  **Container**: Wrap your tool's content in a `<main class="tool-container">`.
4.  **Styling**: Use `<style>` tags for tool-specific styles. Use the following CSS variables for consistency:
    -   `--primary`, `--secondary`, `--accent` (Gradients/Colors)
    -   `--bg-card`, `--bg-glass` (Backgrounds)
    -   `--glass-border`, `--radius-lg` (Borders/Radius)
5.  **Functionality**:
    -   All logic must be client-side (JS).
    -   Use `drop-zone` class for file inputs.
    -   Use `btn-action` class for primary buttons.

**Example Structure**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Tool Name - Chirag Hub</title>
  <!-- UNIVERSAL ENGINE -->
  <script src="https://chirag127.github.io/universal/config.js"></script>
  <script src="https://chirag127.github.io/public/universal/core.js"></script>
  <style>
    .tool-container { max-width: 800px; margin: 4rem auto; text-align: center; }
  </style>
</head>
<body>
  <!-- HEADER INJECTED BY CORE.JS -->
  <main class="tool-container">
    <h1>Tool Name</h1>
    <!-- Tool Interface Here -->
  </main>
  <!-- FOOTER INJECTED BY CORE.JS -->
  <script>
    // Tool Logic
  </script>
</body>
</html>
```

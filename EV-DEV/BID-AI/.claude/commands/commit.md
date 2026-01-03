# Smart Git Commit

Generate a conventional commit message based on the staged changes.

1. Run `git status` and `git diff --staged` to see what's changed
2. Analyze the changes and determine:
   - Type: feat, fix, docs, style, refactor, test, chore
   - Scope: backend, frontend, database, docs, config
   - Breaking changes (if any)
3. Generate a commit message following this format:
   ```
   type(scope): short description
   
   - Detailed change 1
   - Detailed change 2
   - Detailed change 3
   
   [BREAKING CHANGE: description if applicable]
   ```

Then ask if I want to commit with this message or edit it.

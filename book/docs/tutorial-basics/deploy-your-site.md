# Deploying Your Work to the World 🚀

## Introduction

You have written the code. You have built the simulation. You have trained the AI.
But if it stays on your `localhost`, it doesn't exist.

As a Physical AI Engineer, you must master **Deployment**. Whether it's deploying code to a robot or a website to the internet, the principle is the same: **Ship It.**

In this guide, we will deploy this textbook to **GitHub Pages** so you can share your portfolio with the world.

---

## 1. Prerequisites 📋

Before deploying, ensure you have:
1.  **A GitHub Repository:** Your code must be pushed to GitHub.
2.  **Node.js:** Installed on your machine.
3.  **The Publisher Skill:** If you are using our "Matrix" template, you have a secret weapon.

---

## 2. Configuration Check (Don't Skip This!) ⚙️

Docusaurus needs to know *where* it will live. Open your `docusaurus.config.ts` file and check these lines:

```typescript
const config: Config = {
  title: 'Physical AI Textbook',
  url: '[https://your-username.github.io](https://your-username.github.io)', // Your GitHub URL
  baseUrl: '/your-repo-name/',             // Your Repository Name
  organizationName: 'your-username',       // Your GitHub Username
  projectName: 'your-repo-name',           // Your Repository Name
  deploymentBranch: 'gh-pages',            // The branch for deployment
  // ...
};
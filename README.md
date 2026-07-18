# 📱 Interactive iOS Device Simulator Portfolio

Welcome to my personal portfolio! This is a modern, high-fidelity **iOS Simulator & Split-Screen Dashboard** designed to showcase my experience, skills, and publications as a **Senior Mobile & Full-Stack Engineer**.

Instead of a traditional plain resume, this site features a live virtual iOS device next to an immersive timeline panel, creating a responsive and interactive showcase of my career journey.

👉 **[Live Website Link](https://kyawtmayhlaing173.github.io/)**

---

## ✨ Features

*   **📱 Sticky iOS Mockup Bezel**: A realistic iPhone frame complete with responsive curves, side buttons, status bar clock, and a Dynamic Island.
*   **🔄 Bidirectional Scroll Sync**:
    *   **Simulator to Desktop**: Scroll through the experience list or projects grid on the phone, and the desktop view automatically scrolls to center and highlight the matching detailed card.
    *   **Desktop to Simulator**: Scroll the detailed timeline on the right, and the phone simulator automatically switches active tabs and navigation highlights.
*   **🛠️ Interactive App Screens**:
    *   `Home`: Profile card, overview counters, and contact rows.
    *   `Work`: Interactive timeline cards showing roles at **Amptalk**, **Opn**, and **Agoda**.
    *   `Skills`: Circular progress meters and responsive stack badges.
    *   `Projects`: Visual grid containing custom-generated mockup covers.
    *   `Contact`: Simulated native settings panel and functional form.
*   **🖨️ PDF Print Engine**: Supports high-fidelity print overrides (`@media print`). Tapping **Print/Save to PDF** automatically strips away the phone bezels and interactive cards, rendering a clean, high-contrast, multi-page paper resume.

---

## 🛠️ Tech Stack & Architecture

*   **Core**: HTML5, Vanilla CSS3 (Custom Properties & HSL Palettes), ES6 Javascript.
*   **Compiler**: Vite (Optimized production asset bundling).
*   **Deployment**: GitHub Pages (via `gh-pages` automated branch distribution).

---

## 🚀 Running Locally

Follow these steps to run the interactive dashboard in your local development environment:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kyawtmayhlaing173/kyawtmayhlaing173.github.io.git
   cd kyawtmayhlaing173.github.io
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the local development server**:
   ```bash
   npm run dev
   ```
   Open **[http://localhost:3000](http://localhost:3000)** in your browser.

4. **Build for production**:
   ```bash
   npm run build
   ```

---

## 📦 Deployment Workflow

We use the `gh-pages` build automation tool. To publish changes directly to your live site, run:

```bash
npm run deploy
```
*This command will automatically run the production compiler (`vite build`) and force-push the updated `/dist` assets to your repository's `gh-pages` branch.*

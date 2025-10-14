# AiVRIC Website

Official website for the AiVRIC Platform - A proprietary, enterprise-grade security operations platform that unifies offensive and defensive security capabilities with AI-powered analysis.

## Live Website

**[http://aivric.com](http://aivric.com)**

The website is automatically deployed via GitHub Pages from the `gh-pages` branch.

## Repository Structure

This repository uses a specific branch strategy:

### Branches

- **`gh-pages`** (deployment branch)
  - Contains all website HTML, CSS, JavaScript, and assets
  - Automatically deployed to http://aivric.com via GitHub Pages
  - **All website development and content updates should be made here**
  - This is where you should submit pull requests for website changes

- **`main`** (documentation branch)
  - Contains only repository documentation
  - README.md, CLAUDE.md, and contribution guidelines
  - Does NOT contain website files

## Contributing

### Making Website Changes

All website updates should target the `gh-pages` branch:

1. **Clone the repository**
   ```bash
   git clone https://github.com/AiVRIC/AiVRIC-Website.git
   cd AiVRIC-Website
   ```

2. **Checkout the gh-pages branch**
   ```bash
   git checkout gh-pages
   ```

3. **Create a feature branch from gh-pages**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes**
   - Edit HTML, CSS, JavaScript files
   - Add or update images in the `assets/` directory
   - Test locally (see Testing Locally section below)

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

6. **Push to your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to https://github.com/AiVRIC/AiVRIC-Website/pulls
   - Click "New Pull Request"
   - **Important: Set base branch to `gh-pages` (not main)**
   - Set compare branch to your feature branch
   - Provide a clear description of your changes
   - Submit the PR for review

### Contribution Guidelines

- **Target the correct branch**: All website PRs must target `gh-pages`
- **Test locally before submitting**: Ensure your changes work properly
- **Keep commits focused**: Make atomic commits with clear messages
- **Follow existing code style**: Maintain consistency with the existing codebase
- **Update documentation**: If you add new pages or features, document them

## Testing Locally

You can test the website locally before submitting changes:

### Option 1: Python Simple HTTP Server

```bash
# From the repository root (on gh-pages branch)
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

### Option 2: Docker

```bash
# Using the provided docker-compose.yml
docker-compose up
```

Then open http://localhost:8080 in your browser.

### Option 3: Live Server (VS Code)

If using VS Code:
1. Install the "Live Server" extension
2. Right-click on `index.html`
3. Select "Open with Live Server"

## Website Structure

```
AiVRIC-Website/
├── index.html                  # Homepage
├── about.html                  # About page
├── services.html               # Services overview
├── service-details-*.html      # Service detail pages
│   ├── service-details.html    # Defense
│   ├── service-details-2.html  # Offense
│   ├── service-details-3.html  # Vision
│   └── service-details-4.html  # Risk Assessment
├── contact.html                # Contact page
├── assets/                     # Static assets
│   ├── css/                    # Stylesheets
│   ├── js/                     # JavaScript files
│   ├── images/                 # Images and graphics
│   └── fonts/                  # Web fonts
└── ... (additional pages)
```

## Key Features

- **Responsive Design**: Mobile-friendly across all devices
- **Stripe Integration**: Subscription management and payments
- **Service Showcases**: Detailed pages for Defense, Offense, and Vision components
- **Blog System**: News and updates section
- **Contact Forms**: Integration with backend email service
- **Modern UI/UX**: Clean, professional design with smooth animations

## Deployment

Deployment is automated via GitHub Pages:

1. When a PR is merged to `gh-pages`, GitHub Pages automatically rebuilds the site
2. Changes typically appear live within 1-2 minutes
3. You can check deployment status at: Settings → Pages

## Technology Stack

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox/Grid
- **JavaScript**: Vanilla JS and jQuery
- **Bootstrap**: Responsive framework (if applicable)
- **Stripe.js**: Payment processing integration

## Related Repositories

This website is part of the larger AiVRIC Platform ecosystem:

- **[AiVRIC Platform](https://github.com/AiVRIC/AiVRIC-Platform)** - Meta-repository
- **[AiVRIC Defense](https://github.com/AiVRIC/AiVRIC-Defense)** - Cloud security scanner
- **[AiVRIC Offense](https://github.com/AiVRIC/AiVRIC-Offense)** - Penetration testing framework
- **[AiVRIC Vision](https://github.com/AiVRIC/AiVRIC-Vision)** - AI/ML security analytics
- **[AiVRIC Control Plane](https://github.com/AiVRIC/AiVRIC-Control-Plane)** - Infrastructure management

## Support

For questions, issues, or feature requests:

1. Check existing [Issues](https://github.com/AiVRIC/AiVRIC-Website/issues)
2. Create a new issue with detailed information
3. For security concerns, see our [Security Policy](SECURITY.md)

## License

This project is proprietary software. All rights reserved.

## Additional Resources

- **CLAUDE.md**: AI assistant context and guidelines for working with this repository
- **Live Site**: http://aivric.com
- **Deployment Status**: Check GitHub Pages settings for build status

---

**Remember**: Always submit pull requests to the `gh-pages` branch for website changes!

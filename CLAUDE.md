# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AIVric is a static HTML/CSS/JavaScript website for an AI-focused business. The site uses a traditional multi-page architecture with 56+ HTML pages, Bootstrap framework, and various JavaScript libraries for UI components.

## Project Structure

- **Root directory**: Contains 56 HTML pages (index.html, about.html, services.html, etc.)
- **assets/**: All static assets
  - `css/`: Stylesheets including Bootstrap, custom styles, and element-specific CSS files
  - `js/`: JavaScript libraries (jQuery, Bootstrap, Owl Carousel, Fancybox, etc.) and custom scripts
  - `images/`: Images organized by category (background, banner, clients, news, project, icons)
- **Deployment files**:
  - `vercel.json`: Vercel configuration with security headers
  - `Dockerfile.vercel`: Docker image for Vercel CLI
  - `docker-compose.yml`: Docker Compose configuration for local Vercel commands
  - `.github/workflows/preview-deploy.yml`: GitHub Actions workflow for preview deployments

## Key Commands

### Deployment

**Deploy to Vercel (Windows)**:
```bash
vercel-docker.bat deploy --prod
```

**Link Vercel project (first-time setup)**:
```bash
vercel-docker.bat link
```

**Build Docker image for Vercel CLI**:
```bash
docker build -f Dockerfile.vercel -t aivric-vercel:latest .
```

### Development

This is a static site - no build process required. Simply open HTML files in a browser or use a local web server:

```bash
# Python 3
python -m http.server 8000

# Node.js (if http-server is installed)
npx http-server
```

### Git Workflow

- **Main branch**: `main` - production branch
- **Preview branch**: `preview` - triggers automatic Vercel deployments via GitHub Actions
  - Push to `preview` branch to deploy preview site with password protection

## Deployment Architecture

### Vercel Preview Deployments

- Automated via GitHub Actions (`.github/workflows/preview-deploy.yml`)
- Triggered on push/PR to `preview` branch
- Password-protected (set `VERCEL_AUTHENTICATION_PASSWORD` in Vercel dashboard)
- Security headers configured in `vercel.json` (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection)

### Required Secrets (GitHub)

- `VERCEL_TOKEN`: Vercel API token
- `VERCEL_ORG_ID`: Found in `.vercel/project.json` after linking
- `VERCEL_PROJECT_ID`: Found in `.vercel/project.json` after linking

### Docker Wrapper Scripts

Windows users can run Vercel CLI via Docker using:
- `vercel-docker.bat` (Command Prompt)
- `vercel-docker.ps1` (PowerShell)
- `vercel-docker.sh` (Git Bash/WSL)

These scripts mount the project directory and `~/.vercel` config into a containerized Vercel CLI.

## Site Architecture

### Page Types

1. **Homepage variants**: index.html, index-2.html, index-3.html, index-onepage.html, index-rtl.html
2. **About pages**: about.html, about-element-1/2/3.html
3. **Service pages**: services.html, services-2.html, service-details-*.html, service-element-*.html
4. **Portfolio/Projects**: portfolio.html, portfolio-2.html, portfolio-details.html, project-element-*.html
5. **Blog/News**: blog.html, blog-2.html, blog-details.html, news-element-*.html
6. **E-commerce**: shop.html, shop-details.html, cart.html, checkout.html
7. **Other**: team.html, team-details.html, contact.html, pricing.html, faq.html, career.html, testimonial.html, clients-element.html, error.html

### CSS Organization

- Core styles: `bootstrap.css`, `style.css`, `responsive.css`
- Theme: `color.css`, `custom.css`
- Components: Individual CSS files in `assets/css/elements-css/` for banner, feature, about, service, projects, testimonial, working-process, funfact, expertise, news
- Third-party: Font Awesome, Flaticon, Owl Carousel, Fancybox, Nice Select, Animate.css

### JavaScript Libraries

- jQuery 3.x
- Bootstrap 4.x
- Owl Carousel (sliders)
- Isotope (filtering/sorting)
- Fancybox (lightbox)
- Google Maps integration
- WOW.js (scroll animations)
- Custom scripts in `script.js`

## Contact Form

`sendemail.php` handles form submissions - requires PHP server configuration. Update `RECIPIENT_EMAIL` constant for production use.

## Notes for Development

- Pages share common header/footer structure - changes to navigation/footer require updating multiple files
- Rebranding completed (see commit ef8785e) - branding is now "AIVric"
- Site uses Inter and Jost fonts from Google Fonts
- All pages follow a consistent template structure with preloader, search popup, and responsive menu
### Spry

Spry is an open-source, AI-native platform built on Frappe that combines workflow automation, AI content generation, CMS management, and ecommerce tools in one unified ecosystem.

## Modules

Spry is organized into multiple modules, each providing specific functionality:

### 1. **Spry Automation**
Visual workflow automation with AI-powered nodes. Create, manage, and execute automated workflows with a drag-and-drop interface.

**Key Features:**
- Visual workflow editor
- Node-based architecture (HTTP, Function, Data Transform)
- Credential management
- Execution history and monitoring
- Scheduled workflows

### 2. **Writer**
AI-powered content generation and writing assistance.

**Key Features:**
- AI content generation
- Content templates and workflows
- Multi-format content support
- Content versioning and collaboration
- SEO optimization tools

### 3. **CMS**
Comprehensive content management system for websites and digital content.

**Key Features:**
- Website and page management
- Dynamic content blocks
- Media library and asset management
- Theme and template system
- SEO and metadata management
- Multi-site support
- Content publishing workflows

## Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app spry
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/spry
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade
### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

agpl-3.0

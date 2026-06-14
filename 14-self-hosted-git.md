# Self-Hosted Git

[← Previous: Git Hooks](./13-git-hooks.md)

So far in this guide you've worked with GitHub, the world's largest Git hosting platform. But GitHub is not the only option, and for many organisations it is not the *right* option. This section introduces **self-hosted Git servers** — software you install and operate on your own infrastructure. You'll learn why teams choose this path, get hands-on with two popular platforms (GitLab and Gitea), and complete a practical exercise that installs Gitea using Docker.

---

## Why Self-Host Git?

Before diving into tools, let's understand the motivations. Self-hosting Git is a deliberate architectural choice with concrete benefits:

### Data Sovereignty and Compliance

Many industries — healthcare, finance, defence, and government — are subject to data-residency laws that require code and user data to remain within specific geographic boundaries. When you host Git on your own servers, you control exactly where every byte lives. With GitHub's cloud offering you cannot make that guarantee.

### Air-Gapped Environments

Secure networks that are physically isolated from the internet (air-gapped) cannot reach GitHub at all. Engineers in such environments have no choice but to run Git infrastructure internally. Defence contractors, nuclear facilities, and some research institutions operate this way.

### No Vendor Lock-In

When you run your own Git server, you own the data and the upgrade path. If a hosted provider changes pricing, terms, or sunsets a product, you migrate to a new host or even a different self-hosted solution without losing your history. Your code is not held hostage to a service's business decisions.

### CI/CD on Private Runners

GitHub Actions runners are shared, public cloud machines. Some teams need build agents that sit inside their private network, accessing internal APIs, proprietary toolchains, or hardware that cannot be exposed externally. Self-hosted runners on GitLab CI or custom Git hooks let you keep your pipeline infrastructure behind the firewall.

### Cost Control at Scale

GitHub's per-user pricing becomes expensive for large engineering organisations with hundreds or thousands of developers. Self-hosted solutions have no per-user licence cost — you pay only for the infrastructure to run them.

### Full Platform Ownership

Running GitLab, Gitea, or Gitea gives you a full DevOps platform — not just Git hosting, but also CI/CD pipelines, container registries, package registries, issue tracking, and more — without depending on a third party's roadmap or availability.

---

## GitLab

### What Is GitLab?

**GitLab** is a full-featured, open-source DevOps platform. It started as a Git hosting solution and evolved into an almost complete replacement for the entire software delivery toolchain:

- Git repositories (bare and mirrored)
- Built-in CI/CD (GitLab Pipelines)
- Container registry (per-project Docker images)
- GitLab Pages (static site hosting, like GitHub Pages)
- Issue tracking, epics, roadmaps, and time tracking
- Security scanning and compliance dashboards
- Kubernetes integration

GitLab is distributed as both a free open-source Community Edition (CE) and an Enterprise Edition (EE) with additional paid features. Most of what this section covers works in CE.

**When to choose GitLab:** You want an all-in-one platform with CI/CD, container registry, and project management built in. You have a team that will benefit from GitHub-like features without relying on a separate SaaS product.

### Installing GitLab

GitLab can be installed in several ways. Two are most common for beginners:

#### Option A: Omnibus Package (Recommended for Production)

The Omnibus package bundles all GitLab services (NGINX, PostgreSQL, Redis, Sidekiq, GitLab Rails) into a single installable package. It is the officially recommended way to deploy GitLab for teams.

**Ubuntu/Debian install:**

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y curl ca-certificates openssh-server perl

# Add the GitLab package repository and install
curl -sS https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
sudo apt-get install gitlab-ce
```

Once installed, edit the configuration file to set your external URL:

```bash
sudo nano /etc/gitlab/gitlab.rb
```

```ruby
# /etc/gitlab/gitlab.rb
external_url 'http://gitlab.example.com'
```

Then apply the configuration and start GitLab:

```bash
sudo gitlab-ctl reconfigure
```

This command runs Chef recipes that configure every GitLab component. It takes 2–5 minutes on a fresh machine. After it completes, GitLab is available at the URL you configured.

**Essential Omnibus commands:**

```bash
sudo gitlab-ctl status          # Check all services are running
sudo gitlab-ctl start           # Start all GitLab services
sudo gitlab-ctl stop            # Stop all GitLab services
sudo gitlab-ctl restart         # Restart all services
sudo gitlab-ctl reconfigure     # Re-apply configuration changes
sudo gitlab-ctl tail            # Stream all log files (troubleshooting)
sudo gitlab-rails console       # Rails console for advanced administration
```

#### Option B: Docker Install (Simpler for Exploration)

Docker is often the fastest way to get GitLab running for learning or evaluation:

```bash
docker run --detach \
  --hostname gitlab.example.com \
  --publish 443:443 --publish 80:80 --publish 22:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab \
  --volume /srv/gitlab/logs:/var/log/gitlab \
  --volume /srv/gitlab/data:/var/opt/gitlab \
  gitlab/gitlab-ce:latest
```

Breaking this down:

| Flag | Purpose |
|------|---------|
| `--detach` | Run container in the background |
| `--hostname` | Internal hostname GitLab uses for SSL certs |
| `-p 443:443 -p 80:80 -p 22:22` | Expose HTTPS, HTTP, and SSH |
| `--name gitlab` | Friendly container name |
| `-v /srv/gitlab/...` | Persist data and config outside the container |

GitLab in Docker takes 3–5 minutes to fully start while it runs the initial database migrations. You can monitor progress with:

```bash
docker logs -f gitlab
```

### Post-Install Setup

Once GitLab is running, complete the first-run setup:

**1. Set the root password**

Navigate to `http://your-gitlab-host/users/sign_in` and click "Forgot your password?" to reset the root account password. (In Omnibus, you can also set it before first login using `sudo gitlab-rails console`):

```bash
sudo gitlab-rails console
# Inside the console:
user = User.where(id: 1).first
user.password = 'YourSecurePassword123!'
user.password_confirmation = 'YourSecurePassword123!'
user.save!
exit
```

**2. Create users and groups**

Log in as root, then navigate to **Admin Area → Users → New User**. Fill in name, username, and email. Users receive an invitation email to set their password.

Create a group to organise related projects: **Admin Area → Groups → New Group**. Groups let you manage permissions across multiple projects at once.

**3. Create your first project**

Click **Create a project** on the welcome screen. You can:

- Start blank (push an existing local repo)
- Import from GitHub, Bitbucket, or other sources
- Use a GitLab template

GitLab displays the exact commands to push an existing repo:

```bash
git remote add gitlab http://gitlab.example.com/username/project.git
git push -u gitlab main
```

### Key Configuration Concepts

This is not a full configuration reference, but here are the concepts you'll encounter most often:

**External URL** — The URL GitLab uses to generate links in emails, SSH clone URLs, and the UI:

```ruby
external_url 'https://gitlab.internal.company.com'
```

**SMTP / Email Notifications** — Without configuring SMTP, GitLab cannot send password-reset emails, issue notifications, or pipeline status emails:

```ruby
# /etc/gitlab/gitlab.rb
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = 'smtp.company.com'
gitlab_rails['smtp_port'] = 587
gitlab_rails['smtp_user_name'] = 'gitlab@company.com'
gitlab_rails['smtp_password'] = 'your-smtp-password'
gitlab_rails['smtp_domain'] = 'company.com'
gitlab_rails['smtp_authentication'] = 'login'
gitlab_rails['smtp_tls'] = false
```

**GitLab Runners (CI/CD)** — GitLab CI/CD jobs run on **runners** — individual machines registered with your GitLab instance. A runner can be:

- **Shared** — available to all projects (set up by admins)
- **Group-specific** — available to projects within a group
- **Project-specific** — registered for one project only

Register a runner after installing the `gitlab-runner` binary:

```bash
sudo gitlab-runner register \
  --url http://gitlab.example.com/ \
  --registration-token "YOUR-REGISTRATION-TOKEN" \
  --description "docker-runner" \
  --tag-list "docker" \
  --executor docker \
  --docker-image docker:24.0.5 \
  --locked="false"
```

The registration token is found in **Settings → CI/CD → Runners** in the GitLab UI. Runners are discussed in depth in the GitLab documentation; the key concept is that the runner machine executes your CI/CD jobs — it is your private build agent.

---

## Gitea

### What Is Gitea?

**Gitea** is a lightweight, self-hosted Git service written in Go. It was forked from Gogs in late 2016 when the Gogs community and the original author disagreed on the project's direction. Gitea aims to be:

- **Lightweight** — runs on minimal hardware (512 MB RAM is enough for small teams)
- **Simple** — a single binary with no external dependencies
- **GitHub-compatible UI** — the interface looks and feels familiar to GitHub users
- **Easy to upgrade** — replace the binary, restart, done

Gitea deliberately omits some features that GitLab includes (container registry, built-in CI/CD pipeline editor, Kubernetes integration). For CI/CD, Gitea integrates with external systems — you write Actions YAML that runs in lightweight containers. The trade-off is deliberate: Gitea is a focused Git hosting tool, not a full DevOps suite.

**When to choose Gitea:** You want GitHub-like hosting with minimal resource usage, no need for container registry or built-in CI, and prefer a simple upgrade story. Gitea is popular among small teams, personal projects on low-cost VPS instances, and homelab enthusiasts.

### Installing Gitea

#### Option A: Docker Install (Recommended)

The fastest path to a running Gitea instance:

```bash
docker run -d \
  --name=gitea \
  --hostname=gitea.example.com \
  -p 3000:3000 \
  -p 2222:22 \
  -v /var/lib/gitea:/data \
  -v /etc/timezone:/etc/timezone:ro \
  -v /etc/localtime:/etc/localtime:ro \
  -e USER_UID=1000 \
  -e USER_GID=1000 \
  --restart unless-stopped \
  gitea/gitea:latest
```

Key points:
- Port `3000` serves the web UI
- Port `2222` maps to Gitea's internal SSH port (avoiding conflict with the host's SSH on port 22)
- `/var/lib/gitea` persists all data — repositories, users, database
- `USER_UID` and `USER_GID` ensure the Gitea process can write to mounted volumes

After the container starts, Gitea is available at `http://your-host:3000`. The first-run wizard runs automatically on a fresh install.

#### Option B: Binary Install (No Docker)

Download the latest release from `https://github.com/go-gitea/gitea/releases`:

```bash
# Replace VERSION with the latest stable release, e.g. 1.21.x
VERSION=1.21.11
wget https://github.com/go-gitea/gitea/releases/download/v${VERSION}/gitea-${VERSION}-linux-amd64
chmod +x gitea-${VERSION}-linux-amd64
sudo mv gitea-${VERSION}-linux-amd64 /usr/local/bin/gitea
```

Create a dedicated user (good practice — never run Git services as root):

```bash
sudo adduser --system --shell /bin/bash --group --disabled-password \
  --home /home/git git
sudo mkdir -p /var/lib/gitea
sudo chown git:git /var/lib/gitea
```

Create a basic `app.ini` configuration before starting:

```ini
# /etc/gitea/app.ini
RUN_MODE = prod

[server]
PROTOCOL         = http
DOMAIN           = gitea.example.com
ROOT_URL         = http://gitea.example.com/
HTTP_PORT        = 3000
SSH_DOMAIN       = gitea.example.com
SSH_PORT         = 22
DISABLE_SSH      = false
MINIMUM_KEY_SIZE = 3072

[database]
DB_TYPE  = sqlite3
PATH     = /var/lib/gitea/gitea.db

[security]
INSTALL_LOCK = true
SECRET_KEY   = change-this-to-a-random-secret
```

Run Gitea:

```bash
sudo -u git /usr/local/bin/gitea web --config /etc/gitea/app.ini
```

On first run, Gitea detects an uninitialised database and redirects you to the web setup wizard automatically.

### First-Time Setup Wizard (Web UI)

Navigate to `http://your-gitea-host:3000/install`. You'll configure:

**Database Settings**
- SQLite is the default and sufficient for small teams (no separate database server needed)
- For production with multiple workers, PostgreSQL is recommended

**General Settings**
- **Site Title:** Your organisation name
- **Repository Root Path:** Where Git repos are stored (default `/var/lib/gitea/gitea-repositories`)
- **Git LFS Path:** Path for Git LFS storage
- **Run as User:** `git`
- **Domain:** Used in SSH clone URLs

**Optional Settings**
- Disable user registration (`DISABLE_REGISTRATION`) if you want admin-only account creation
- Require sign-in to view repos (`REQUIRE_SIGNIN_VIEW`)

**Administrator Account** — Create your first admin user here. This is the only time the form appears; after setup, you create additional admins from within the UI.

Click **Install Gitea**. After installation completes, you'll be redirected to the sign-in page.

### Key Configuration Concepts (app.ini)

`app.ini` is Gitea's sole configuration file. Some important sections:

```ini
[server]
# Set RUN_MODE = prod for production (enables more aggressive caching)
RUN_MODE = prod

[security]
# INSTALL_LOCK must be true after first setup — it prevents the install page
INSTALL_LOCK = true
# Generate a proper secret: openssl rand -base64 32
SECRET_KEY = your-random-secret-here

[database]
DB_TYPE  = postgres
HOST     = 127.0.0.1:5432
NAME     = gitea
USER     = gitea
PASSWD   = your-db-password

[service]
# Require email confirmation before users can act
REGISTER_EMAIL_CONFIRM            = true
DISABLE_REGISTRATION              = false
ALLOW_ONLY_EXTERNAL_REGISTRATION  = false
REQUIRE_SIGNIN_VIEW               = false

[ssh]
# Minimum RSA key size (default 2048, recommend 3072+)
MINIMUM_KEY_SIZE = 3072
```

Changes to `app.ini` take effect after restarting Gitea:

```bash
# Binary install
sudo -u git pkill gitea
sudo -u git /usr/local/bin/gitea web --config /etc/gitea/app.ini

# Docker install
docker restart gitea
```

---

## GitLab vs Gitea: Comparison

| Feature | GitLab CE/EE | Gitea |
|---------|-------------|-------|
| **License** | MIT (CE), proprietary (EE) | MIT |
| **Minimum RAM** | 4 GB recommended | 512 MB |
| **Dependencies** | Bundled (PostgreSQL, Redis, NGINX) | Single binary (optional external DB) |
| **Built-in CI/CD** | Yes (GitLab Pipelines) | No (use external: Drone, Jenkins, GitHub Actions remote) |
| **Container Registry** | Yes, per-project | No |
| **Issue Tracking** | Full (Issues, Epics, Roadmaps, Time tracking) | Basic issues and pull requests |
| **Markdown Wiki** | Per-project wiki | Per-project wiki |
| **Import/Export** | GitHub, Bitbucket, GitLab → GitLab | GitHub, Bitbucket, Gitea, and more |
| **Upgrade Complexity** | `apt upgrade` or `docker pull` | Replace binary + migrate (usually trivial) |
| **API** | REST + GraphQL (comprehensive) | REST (functional, less comprehensive) |
| **GitHub Compatibility** | Partial (import only) | High (import + compatible UI) |
| **Best For** | Teams needing full DevOps platform | Small teams, personal projects, homelabs |
| **Complexity** | Higher (more powerful, more to manage) | Lower (simpler, leaner) |

Both are excellent choices. The decision typically comes down to: do you need built-in CI/CD and container registry? Choose GitLab. Do you need something lean that runs on a $10/month VPS? Choose Gitea.

---

## Self-Hosted vs GitHub

### Choose Self-Hosted When:

- **Compliance or data residency** is a hard requirement (cannot store code on third-party servers)
- You need **CI/CD runners inside a private network** with access to on-prem resources
- Your organisation has **>50 developers** and the per-seat GitHub cost is a budget concern
- You operate in an **air-gapped environment** with no internet access
- You want **full control over upgrades** and no risk of a SaaS deprecation

### Choose GitHub When:

- You want the **latest features** without managing infrastructure
- Your team is **distributed globally** and you want GitHub's CDN-backed global edge network
- You rely on **GitHub Actions** as your primary CI/CD system
- You want seamless integration with **GitHub Marketplace** apps and third-party tooling
- You are an **open-source project** that benefits from GitHub's social graph and discoverability

### The Middle Ground

Some teams use both: a self-hosted GitLab for private, compliance-sensitive work, and GitHub for open-source contributions. Multi-remote repositories make this feasible — you add both as remotes and push to each as needed:

```bash
git remote add github git@github.com:org/private-repo.git
git remote add gitlab git@gitlab.internal.com:dev/private-repo.git

# Push to both remotes
git push github main
git push gitlab main
```

---

## Exercise

### Scenario

You are a DevOps engineer setting up internal Git hosting for a small development team of 5 people. Your team needs Git hosting quickly without spending money on infrastructure. You have a Linux server (or can use Docker) available.

Your task:
1. Install Gitea using Docker
2. Complete the first-run setup wizard in the web UI
3. Create an admin account
4. Create a new repository named `hello-devops`
5. Clone the repository to your local machine
6. Add a file, commit it, and push to your self-hosted Gitea instance
7. Verify the commit appears in the Gitea web UI

### Prerequisites

- Docker installed (`docker --version`)
- Port `3000` available on localhost
- A web browser to access the Gitea UI

### Steps

**1. Start the Gitea container:**

```bash
docker run -d \
  --name=gitea \
  --hostname=localhost \
  -p 3000:3000 \
  -p 2222:22 \
  -v /tmp/gitea:/data \
  --restart unless-stopped \
  gitea/gitea:latest
```

**2. Wait for Gitea to start (30–60 seconds):**

```bash
docker logs gitea 2>&1 | tail -5
```

Expected output (truncated):

```text
2024/11/01 14:23:01 [I] Gitea version 1.21.11 built with GNU Make
2024/11/01 14:23:01 [I] Log mode: File (Info)
2024/11/01 14:23:02 [I] XORM Log Mode: File (Info)
2024/11/01 14:23:03 [I] Migration completed successfully
2024/11/01 14:23:03 [I] listen: http://0.0.0.0:3000
```

The line `listen: http://0.0.0.0:3000` confirms Gitea is ready.

**3. Open the setup wizard:**

Open `http://localhost:3000` in your browser. If this is the first time, you are redirected to `http://localhost:3000/install`.

**4. Fill in the setup form:**

- **Database Type:** SQLite3 (default, no setup needed)
- **Site Title:** `Gitea Local`
- **Repository Root Path:** `/data/git/repositories` (default)
- **Run As User:** `git`
- **Domain:** `localhost`
- **SSH Port:** `2222`
- **HTTP Port:** `3000`
- **Base URL:** `http://localhost:3000/`

Under **Administrator Account**:
- **Email:** `admin@gitea.local`
- **Password:** `SecureAdmin123!`
- **Confirm Password:** `SecureAdmin123!`
- **Username:** `gitea_admin`

Click **Install Gitea**.

**5. Sign in as admin:**

After installation, you are redirected to the sign-in page. Sign in with the admin credentials you just created.

**6. Create the repository:**

Click the **+** icon in the top navigation bar → **Create Repository**.

- Name: `hello-devops`
- Description: `My first Gitea repository`
- Visibility: **Private** (default)
- Initialize Repository: ☑️ **Add a README**

Click **Create Repository**.

**7. Clone the repository:**

On the repository page, Gitea shows clone instructions. Copy the SSH or HTTP URL. For local testing on `localhost` with no real SSH, use HTTP:

```bash
git clone http://localhost:3000/gitea_admin/hello-devops.git
```

```text
Cloning into 'hello-devops'...
warning: redirecting to http://localhost:3000/gitea_admin/hello-devops.git/
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), done.
```

**8. Add a file, commit, and push:**

```bash
cd hello-devops
echo "# Hello DevOps" > devops.txt
git add devops.txt
git commit -m "Add devops.txt marker file"
git push -u origin main
```

```text
[main (root-commit) abc1234] Add devops.txt marker file
 1 file changed, 1 insertion(+), 1 deletion(-)
 create mode 100644 devops.txt
Username for 'http://localhost:3000': gitea_admin
Password for 'http://localhost:3000': SecureAdmin123!
Enumerating objects: 2, done.
Counting objects: 100% (2/2), done.
Writing objects: 100% (2/2), 81 bytes, done.
Total 2 (delta 0), reused 0 (delta 0), pack-reused 0
To http://localhost:3000/gitea_admin/hello-devops.git
 * [new branch]      main -> main
branch 'main' set up to track 'main'.
```

**9. Verify in the web UI:**

Refresh the Gitea repository page. You should see:

- The `devops.txt` file listed in the file tree
- The commit `Add devops.txt marker file` in the commit history

**10. Clean up (optional):**

```bash
docker stop gitea && docker rm gitea
rm -rf /tmp/gitea
```

---

## Solution

The full step-by-step solution is embedded above. To verify your setup was successful:

```bash
# Verify the container is running
docker ps --filter name=gitea --format "{{.Names}} {{.Status}}"

# Verify the clone worked
ls hello-devops/devops.txt && echo "File exists"

# Verify the commit history
git -C hello-devops log --oneline
```

Expected output:

```text
gitea Up (healthy)
File exists
abc1234 Add devops.txt marker file
```

If you see the commit in the log and the file exists, your self-hosted Git server is working correctly.

---

## Recap

In this section you learned:

- **Why self-host** — data sovereignty, air-gapped networks, cost control, and private CI/CD runners
- **GitLab** — a full DevOps platform installed via Omnibus or Docker, with post-install user management, runner registration, and key config concepts
- **Gitea** — a lightweight, Go-based Git host installed via Docker or binary, configured through `app.ini` and a web setup wizard
- **Comparison** — GitLab is feature-rich and heavier; Gitea is lean and runs on minimal hardware
- **When to choose** self-hosted vs GitHub.com based on compliance, team size, and infrastructure needs

---

[← Previous: Git Hooks](./13-git-hooks.md) · [Next: Capstone Mini-Project →](./15-capstone.md) · [← Back to Index](./00-index.md)
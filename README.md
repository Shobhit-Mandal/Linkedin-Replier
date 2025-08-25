LinkedIn Replier — README

A small toolset that parses incoming LinkedIn service-request emails (HTML/JSON), extracts the important Q/A, builds a proposal message, and automates submitting that proposal to the LinkedIn Service Marketplace thread using Selenium + undetected_chromedriver.

This README explains project structure, setup (Windows-focused), recommended environment, how to run locally and from n8n Execute Command node, and troubleshooting tips for the common issues you encountered.

Table of contents

Project layout

Requirements

Recommended environment

Quick install (Windows)

Configure config.json

Running locally (examples)

Running from n8n (Execute Command)

Passing long messages / files

Logging, exit codes and n8n handling

Troubleshooting (common errors & fixes)

Notes & best practices

License

Project layout
linkedin-replier/
├─ linkedin_proposal.py        # main automation script (Selenium + uc)
├─ parse_request.py            # parses HTML/JSON to extract Q&A
├─ config.json                 # holds li_at cookie and other config
├─ file.json / file.html       # sample input files used by parser
├─ requirements.txt            # recommended Python packages
├─ README.md                   # this file
└─ venv/                       # optional virtualenv (not committed)

Requirements

Windows (instructions below are Windows-centric)

Python 3.11.x (recommended; some packages expect distutils available)

Chrome browser (desktop)

Chromedriver matching your Chrome major version

A li_at cookie value (stored in config.json) for LinkedIn auth

n8n (optional) — if you will trigger scripts from n8n

Recommended Python packages (see requirements.txt):

undetected-chromedriver
selenium
beautifulsoup4
lxml
pyperclip        # optional (if you try clipboard paste)


A requirements.txt example:

undetected-chromedriver==3.4.0
selenium==4.14.0
beautifulsoup4==4.12.2
lxml==4.9.3
pyperclip==1.8.2


Version pinning above is only an example. Use the versions that are compatible with your environment.

Recommended environment

Use a dedicated Python 3.11 venv to match your development environment.

Ensure Chromedriver version matches installed Chrome major version (e.g., Chrome 138 → Chromedriver for 138).

Run n8n as an interactive user session (not a Windows service) if you require headful Chrome UI automation. Headful Chrome needs an interactive desktop session.

Quick install (Windows)

Install Python 3.11 (if necessary)

If you downloaded python-3.11.5-amd64.exe to C:\Users\<you>\Downloads\Python311, first run the installer (GUI or silent). Example silent command (single-line for CMD prompt — run from the directory containing the installer):

C:\Users\agraw\Downloads\Python311\python-3.11.5-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir="C:\Python311"


If you install with /quiet you may need admin privileges.

Create a venv using Python 3.11

Example (adjust if your installed python is at a different path):

C:\Python311\python.exe -m venv "C:\Users\agraw\Downloads\linkedin replier\venv311"


Activate the venv

Using CMD:

C:\Users\agraw\Downloads\linkedin replier\venv311\Scripts\activate.bat


Using PowerShell (if execution policy allows):

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force
.\venv311\Scripts\Activate.ps1


Install dependencies

With venv active:

pip install --upgrade pip
pip install -r requirements.txt


If you don't have requirements.txt, you can install individually:

pip install undetected-chromedriver selenium beautifulsoup4 lxml pyperclip


Chromedriver

Download the Chromedriver binary that matches your Chrome major version and place it somewhere accessible (e.g. C:\drivers\chromedriver.exe). Update linkedin_proposal.py or CHROMEDRIVER path accordingly (or use undetected_chromedriver’s automatic management where possible).

Configure config.json

Create config.json with at least the li_at cookie value:

{
  "li_at": "<YOUR_LINKEDIN_li_at_COOKIE_VALUE>"
}


Important: keep config.json secret. li_at is sensitive — treat it like a credential.

Running locally (examples)
1) Run parser (parse_request.py)

If your JSON file format is:

[
  { "html": "<full html string...>" }
]


Run:

"C:\Users\agraw\Downloads\linkedin replier\venv311\Scripts\python.exe" "C:\Users\agraw\Downloads\linkedin replier\parse_request.py"


(Your script may accept file path; check parse_request.py for interface.)

2) Run LinkedIn proposal sender

Simple command-line run:

"C:\Users\agraw\Downloads\linkedin replier\venv311\Scripts\python.exe" "C:\Users\agraw\Downloads\linkedin replier\linkedin_proposal.py" "THREAD_URL" "MESSAGE_TEXT"


Example:

"C:\Users\agraw\Downloads\linkedin replier\venv311\Scripts\python.exe" "C:\Users\agraw\Downloads\linkedin replier\linkedin_proposal.py" "https://www.linkedin.com/service-marketplace/projects/15200..." "Hello! I can help with ... "


Tip: If MESSAGE_TEXT is long or contains newlines, prefer writing the message to a file (e.g. message.txt) and change the script to read the file content instead of taking a CLI argument. This avoids Windows command-length issues and newline escaping problems.

Running from n8n (Execute Command node)

Use the venv python executable absolute path so n8n runs the right interpreter:

n8n Execute Command node — Command field:

"C:\Users\agraw\Downloads\linkedin replier\venv311\Scripts\python.exe" "C:\Users\agraw\Downloads\linkedin replier\linkedin_proposal.py" "{{ $json.threadUrl }}" "{{ $json.message }}"


Notes:

Put quotes around every path and argument.

If message contains newlines or is very long, write it to a file in a previous node (File node) and pass the filename to the script, or have the script read from a pre-known file path.

If n8n runs as a Windows service, it may not have interactive desktop access. For headful Chrome automation, run n8n in an interactive user session.

Logging & Exit codes (how n8n detects success/failure)

The scripts print human-readable logs (timestamped), and special sentinel messages on failures such as:

login failed → printed then sys.exit(1)

submit_proposal_button_not_found → printed then sys.exit(1)

message_textarea_not_found → printed then sys.exit(1)

send_proposal_button_not_found → printed then sys.exit(1)

On success, script prints something like Proposal sent successfully and exits with code 0.

n8n Execute Command node returns exitCode and stdout/stderr; use exitCode !== 0 to detect errors.

Passing long messages / files

To avoid Windows command-length limits and newline/quoting issues:

Write message to a file (prior Node in n8n).

Pass filename to the Python script:

python linkedin_proposal.py THREAD_URL --message-file "C:\temp\message.txt"


In linkedin_proposal.py, handle --message-file argument and read file contents.

This is the most robust approach.

Troubleshooting (common errors and fixes)
UnicodeEncodeError: 'charmap' codec can't encode character

Occurs when printing Unicode characters on Windows with cp1252 default.

Fix: Set environment variable or in script:

import sys
sys.stdout.reconfigure(encoding='utf-8')


Or run Python with PYTHONIOENCODING=utf-8.

ModuleNotFoundError: No module named 'distutils'

Install setuptools/distutils or use Python 3.11 installed with standard libs.

On Windows: ensure installation included required components or install setuptools via pip.

SessionNotCreatedException: This version of ChromeDriver only supports Chrome version XXX

Chromedriver and Chrome must match major version.

Download correct Chromedriver or update Chrome.

OSError: [WinError 6] The handle is invalid in Chrome.del

Often harmless; ensure driver.quit() is called and that process runs in an interactive session.

Script types halfway and exits (message stops at \n\n)

Using character-by-character send_keys can hang or lose focus on newline sequences.

Recommended fix: set the textarea value via JavaScript and dispatch an input event (more reliable):

driver.execute_script("arguments[0].focus(); arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", textarea_element, MESSAGE_TEXT)


Then read back the value:

actual = driver.execute_script("return arguments[0].value;", textarea_element)
if actual != MESSAGE_TEXT:
    print("message_paste_failed", flush=True)
    sys.exit(1)


Alternatively, call element.send_keys(whole_text_string) in a single call instead of per-character loop.

Connection cannot be established when launching chromedriver from n8n

Likely caused by environment differences (missing PATH, service vs interactive session, firewall, antivirus, or user permissions).

Ensure n8n executes the Python under the same user context and that chromedriver is accessible.

PowerShell script activation errors

If Activate.ps1 cannot be loaded:

Run PowerShell as admin and Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force

Or use the activate.bat from CMD.

Notes & best practices

Security: li_at cookie is sensitive. Do not commit config.json to git. Use secrets management in production.

Stability: Interacting with LinkedIn's UI is brittle. Expect intermittent failures, element changes, and require robust selectors + fallbacks.

Headful vs headless Chrome: Headful (visible) often behaves better for complex pages. If automating on a server without display, consider a dedicated headless-friendly approach (but LinkedIn often blocks headless).

n8n deployment: For reliable automation from n8n, run n8n as the interactive user session (not as a locked Windows service) OR run a small agent script in the interactive session that receives commands from n8n (e.g. via a simple HTTP webhook or message queue).

Testing: Always test locally in the same environment you plan to run in (same Python, same Chrome, same chromedriver) before deploying to client machines.

Example: recommended linkedin_proposal.py invocation (local)
"C:\Users\agraw\Downloads\linkedin replier\venv311\Scripts\python.exe" "C:\Users\agraw\Downloads\linkedin replier\linkedin_proposal.py" "https://www.linkedin.com/service-marketplace/projects/15200..." "Hello! I'm Mayank. I can help with..."


Or (preferred for long messages):

"C:\Users\agraw\Downloads\linkedin replier\venv311\Scripts\python.exe" linkedin_proposal.py "THREAD_URL" --message-file "C:\temp\message.txt"

Final words

This project is a combination of web scraping, browser automation, and system-level integration with n8n. The most brittle areas are:

Chrome/Chromedriver compatibility

Running headful browsers from non-interactive services (n8n service)

LinkedIn UI changes

Handling long messages and character encoding

If you want, I can produce:

A ready-made requirements.txt and install_deps.py script,

A final copy-paste linkedin_proposal.py that:

reads message from file if present,

sets textarea value via JS and verifies it,

prints sentinel messages and proper exit codes,

enforces UTF-8 stdout.

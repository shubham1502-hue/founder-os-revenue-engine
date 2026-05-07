# How to fork and use Founder OS Revenue Engine

This guide is for a founder or operator who wants to adapt the repo without turning it into a generic portfolio project.

## First pass

1. Fork the repo.
2. Rename it for your company or operating workflow.
3. Read the README Quick Start section.
4. Replace sample inputs, templates, or context files with your own company context.
5. Run the workflow if executable, or copy the first template if it is a playbook.
6. Open the main output listed in the README before changing deeper logic.

## Company fork path

1. Click Fork.
2. Rename the repo if needed.
3. Replace `data/raw_data.csv` with your funnel or CRM export.
4. Update `context/startup_overview.md` with company stage, ACV, ICP, and current GTM motion.
5. Run the analysis scripts from the repo root.
6. Move the action list into Linear, Asana, ClickUp, HubSpot, Pipedrive, Attio, or your weekly GTM tracker.

## Non-technical path

- Replace one CSV: `data/raw_data.csv`.
- Edit one context file: `context/startup_overview.md`.
- Run the commands in order.
- Read one output first: `founder_note.md`.

## Data safety

The included sample data is synthetic, anonymized, or template-only unless a public source is explicitly documented. Do not commit private customer, prospect, employee, investor, borrower, merchant, payment, or company data to a public fork.

## Tools to connect later

Start with files first. After the workflow is useful, connect outputs to Google Sheets, Notion, Airtable, HubSpot, Pipedrive, Attio, Linear, Asana, ClickUp, Slack, or your internal ops tracker where relevant.

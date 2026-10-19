# [integrations] Integrations

Accounting sync: two-way sync with QuickBooks Online and Xero (Team and above). Sync runs every 15 minutes; a manual sync can be triggered from Settings > Integrations. Invoices sync to the accounting system, payments sync back. Conflicts (the same invoice edited on both sides) are resolved in favour of the accounting system, and a conflict notice is shown in Ledgerly.

Payments: Stripe (card, SEPA, ACH) and GoCardless (direct debit in the UK and eurozone). Only one Stripe account can be connected per company profile.

CRM: HubSpot and Salesforce (Business and above). Deals marked as won can create a draft invoice automatically.

Zapier and Make: available on all paid plans, with triggers for invoice created, invoice paid, invoice overdue, and customer created.

Slack: notifications for paid and overdue invoices, on all paid plans.

Common QuickBooks sync error "Duplicate document number": the invoice number already exists in QuickBooks. Fix it by changing the numbering prefix in Ledgerly (Settings > Invoicing > Numbering) or by renaming the conflicting document in QuickBooks, then trigger a manual sync.

Common Xero sync error "Account code not found": the revenue account mapped in Ledgerly was archived in Xero. Re-map it under Settings > Integrations > Xero > Account mapping.

Disconnecting an integration stops future syncs but does not delete data already synced to either side.

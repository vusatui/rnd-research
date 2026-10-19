# [invoicing] Creating and sending invoices

Invoice numbering: sequential per company profile, default format INV-{YYYY}-{0001}. The prefix and the next number can be changed under Settings > Invoicing > Numbering, but numbers can never go backwards and an already used number cannot be reused. This is required by tax rules in many countries.

Editing a sent invoice: a sent invoice cannot be edited. Create a credit note for it (Invoice > More > Create credit note) and issue a new invoice. Drafts can be edited freely.

Deleting invoices: drafts can be deleted. Sent invoices can only be voided, which keeps them in the numbering sequence with a VOID watermark.

Recurring invoices (Team and above): weekly, monthly, quarterly or yearly schedules. Each recurring invoice is created as a draft 3 days before the send date unless "auto-send" is switched on.

Payment reminders (Team and above): up to 3 automatic reminders, by default 3 days before due date, on the due date and 7 days after. Reminder texts are editable.

Late fees: a fixed amount or a percentage (max 10% per month) can be added automatically after the due date. Late fees must be enabled per customer.

Online payments: customers can pay invoices by card via Stripe or by bank transfer. Ledgerly charges no extra fee on top of Stripe's fees. Payouts follow the Stripe account schedule.

Custom templates (Business and above): HTML/CSS templates with merge fields such as {{customer.name}} and {{invoice.total}}. Templates are validated on save; external fonts are allowed, external scripts are not.

Multi-currency (Business and above): 42 currencies. Exchange rates are taken daily at 16:00 CET from the European Central Bank reference rates. The rate is locked when the invoice is sent.

E-invoicing: Peppol BIS Billing 3.0 is supported for Belgium, the Netherlands, Norway and Germany (XRechnung). Italy's SDI and France's Chorus Pro are on the roadmap with no committed date; support must not promise a date.

Attachments: up to 10 files per invoice, 10 MB each.

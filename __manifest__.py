# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "helpdesk timesheet bills",
    "summary": """
        Allow timesheet management and billing to helpdesk tickets """,
    "author": "Nahe Consulting Group",
    "maintainers": ["nahe-consulting-group"],
    "website": "https://nahe.com.ar/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "16.0.2.1.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["helpdesk_mgmt", "sale", "hr_timesheet"],
    "data": [
        "views/helpdesk_ticket_views.xml",
    ],
}

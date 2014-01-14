.. _Future Features:

Future Features
================

.. _Trip Entry Form:

Trip Entry Form
----------------

Create an Entry Form for Communards to easily record any Trips they have taken
out. The Entry Fields should include:

* Tripper Name
* Trip Number
* Trip Date
* Cash Advance
* Cash Returned

Transactions should be grouped by Merchant or Store, and totals should be
calculated not only for the entire entry, but also for each individual store.

Each Transaction line should have an "Item Price", "Sales Tax" and "Total
Price" field, with the Sales Tax defaulting to a "Sales Tax %" Setting. The
Total Price should be calculated whenever the Item Price or Sales Tax fields
are changed.

A valid form will require that ``Cash Advance = Total Prices + Cash Returned``.

A successful submission will redirect the User to a printable version of their
submitted entry, so they may print the form and attach receipts.

Brainstorm clean ways to deal with Store Accounts and Returns.

.. _Credit Card Entry Form:

Credit Card Entry Form
-----------------------

Create an Entry Form for Communards to record Personal Credit Cards. Entry
fields should include:

* Person's Name
* Credit Card Name
* Statement Date
* Statement Total

Transactions should have a ``Detail``, ``Amount`` and ``Account`` field.

A valid form will require that ``Statement Balance = Sum of Amounts``.

A successful submission will redirect the User to a printable version of their
submitted entry, so they may print the form and attach receipts.

.. _Bank Statement Form:

Bank Statement Form
--------------------

Use `OFX <http://en.wikipedia.org/wiki/Open_Financial_Exchange>`_ to pull
bank statements from banks.

Present the user with a form prefilled with all entered transactions that
match. If no transaction matches, fill the amount and date leaving account and
memo blank. User will enter these fields. For non-matched lines, the application
will create either a bank spending or receiving entry for the bank and
user-specified account.

.. _Budgeted Accounts:

Budgeted Accounts
-----------------

Add optional Budgets to Accounts

Do we do:

* Budgets per year, month, quarter?
* Rolling budgets or fixed date?

Application should display:

* Accounts balance as % of budget
* Accounts that are overbudget or close to their budget.
* Alert for accountants/administrators when Accounts hit their budget or get
  within $X.XX of their budget.

.. _Event Reports:

Event Reports
--------------

Events Reports should show a table of all events, ordered by date with the most
recent event first.

The table should display each Event's Date, Name, City, State and Net Change.

Clicking a row of the table should display the :ref:`Event Detail Page <Event
Detail Page Design>` for the selected Event.

.. _PL Reports:

Profit and Loss Reports
------------------------

P&L Reports should show the net balance change for each Account, from the
beginning of the fiscal year(or the beginning of time if there is no fiscal
year) to a user-specified date.

**Entry Conditions**

The Profit & Loss report should be accessible through a ``Profit & Loss`` link
in the :ref:`Reports Sub-menu <Reports Submenu Design>`.

**Initial Conditions**

The page should display the name of the report, a form for selecting the
start and end dates and a table.

The start date should default to the start of the current Fiscal Year. The
end date should default to the current date.

The table should contain every account that exists, sorted by account number.
It should have columns displaying the Account name and the Profit/Loss
amounts(aka net change) for each account.

Net Change is calculated by: ``netchange = sum of credits - sum of debits``

**Final Conditions**

Submitting the date range form will refresh the page, using the specified
start and end dates to calculate the profit and loss amounts.

Clicking a row in the table will redirect the User to the Account's
:ref:`Detail Page <Account Detail Page Design>`.

.. _Tax Prep Report Design:

Tax Preparation Report
-----------------------

A report to help the tax preparer collect information.

.. _Yearly Budget Report Design:

Yearly Budget Report
---------------------

This report should show the things we go over in our annual budget meeting.
YTD Expense spending and Income, compared with the YTD for previous years.

By default it should show from the beginning of the current fiscal year to the
current date. Maybe it could extrapolate for the rest of the year and show
breakdown by quarter?

.. _People Tracking:

People Tracking
----------------

Allow us to add members, interns, prov. members, visitors etc. Can be used to
automatically pay stipends and bonuses for interns and members. Can also help
the tax preparer learn the # of intern days in the year.

Can track the "Render unto Caesar" form details.

Store email address & email monthly balance reports to members and interns.

.. _Alternate Home Page:

Alternate Home Page
--------------------

The Home Page is currently the :ref:`Chart of Accounts Page <Chart of Accounts
Page Design>`.

An alternative is making the Home Page a "Recent Activity/Alerts" page. This
new page could show:

* Recently created or updated Journal Entries
* Balances of "watched" Accounts
* Over-budget or close-to-budget Accounts (see :ref:`Budgeted Accounts`)
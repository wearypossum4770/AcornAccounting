from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from entries.models import JournalEntry, Transaction
from receipts.models import Receipt

from .forms import CreditCardEntryForm, CreditCardTransactionFormSet
from .models import CreditCardEntry, CreditCardReceipt


@login_required
def list_creditcard_entries(request, template_name='creditcards/list.html'):
    """Retrieve every :class:`CreditCardEntry`."""
    entries = CreditCardEntry.objects.all()
    return render(request, template_name, {'entries': entries})


def show_creditcard_entry(request, entry_id,
                          template_name="creditcards/show_entry.html"):
    """View a :class:`~.models.CreditCardEntry`."""
    entry = get_object_or_404(CreditCardEntry, pk=entry_id)
    return render(request, template_name,
                  {'journal_entry': entry,
                   'transactions': entry.transaction_set.all()})


def add_creditcard_entry(request, entry_id=None,
                         template_name="creditcards/credit_card_form.html"):
    """Add, edit, approve or delete a :class:`~.models.CreditCardEntry`."""
    entry = _initialize_entry(request, entry_id)
    if request.method == 'POST':
        entry_form = CreditCardEntryForm(
            request.POST, request.FILES, prefix='entry', instance=entry)
        transaction_formset = CreditCardTransactionFormSet(
            request.POST, prefix='transaction', instance=entry)
        submision_type = (
            request.POST.get('subbtn', request.POST.get('delete', '')).lower())
        if any(t in submision_type for t in ['submit', 'approve']):
            transaction_formset.entry_form = entry_form
            if entry_form.is_valid() and transaction_formset.is_valid():
                entry_form.save()
                transaction_formset.save()
                _create_creditcard_receipts(entry_form, entry)
                if 'approve' in submision_type:
                    return _handle_approval_and_redirect(
                        request, entry, 'next' in submision_type)
                if entry_id is None:
                    message_text = ("Your Credit Card Entry has been "
                                    "successfully submitted for Approval.")
                    if not entry_form.instance.receipt_set.exists():
                        message_text += (
                            " Since you did not attach a receipt, <b>you"
                            " must print this page</b>, staple your receipts"
                            " to it and submit the paper copies to"
                            " Accounting.")
                    messages.success(request, message_text)
                return _handle_redirect(request, entry, submision_type)
        elif 'delete' in submision_type and entry.pk:
            entry.delete()
            messages.success(
                request, "The Credit Card Entry was deleted.")
            return HttpResponseRedirect(
                reverse('creditcards.views.list_creditcard_entries'))
        else:
            raise Http404

    else:
        entry_form = CreditCardEntryForm(prefix='entry', instance=entry)
        transaction_formset = CreditCardTransactionFormSet(
            prefix='transaction', instance=entry)
    request_data = {'entry_form': entry_form,
                    'verbose_entry_type': 'Credit Card Entry',
                    'transaction_formset': transaction_formset}
    return render(request, template_name, request_data)


def _initialize_entry(request, entry_id):
    """Fetch or create a new CreditCardEntry."""
    if entry_id is not None:
        if not request.user.is_authenticated():
            raise Http404
        entry = get_object_or_404(CreditCardEntry, id=entry_id)
    else:
        entry = CreditCardEntry()
    return entry


def _create_creditcard_receipts(valid_form, entry):
    """Create CreditCardReceipts from the receipts field of a valid form."""
    for receipt in valid_form.cleaned_data['receipts']:
        CreditCardReceipt.objects.create(
            creditcard_entry=entry, receipt_file=receipt)


def _handle_redirect(request, entry, submision_type):
    """Redirect to the proper page depending on the ``submision_type``."""
    if 'add more' in submision_type:
        if not entry.receipt_set.exists():
            messages.warning(
                request,
                "You did not attach a receipt, you <b>must</b> print this "
                "page & submit it to Accounting along with a hardcopy of the "
                "receipt."
            )
            return HttpResponseRedirect(
                reverse('creditcards.views.show_creditcard_entry',
                        args=[str(entry.id)])
            )

        return HttpResponseRedirect(reverse(
            'creditcards.views.add_creditcard_entry'))
    elif 'next' in submision_type:
        try:
            next_entry = CreditCardEntry.get_next_by_date(
                entry, card=entry.card)
            return HttpResponseRedirect(
                reverse('creditcards.views.add_creditcard_entry',
                        kwargs={'entry_id': next_entry.id}))
        except CreditCardEntry.DoesNotExist:
            return HttpResponseRedirect(
                reverse('creditcards.views.list_creditcard_entries'))
    return HttpResponseRedirect(
        reverse('creditcards.views.show_creditcard_entry',
                kwargs={'entry_id': entry.id}))


def _handle_approval_and_redirect(request, creditcard_entry, redirect_to_next):
    """Approve the CreditCardEntry & Redirect to the proper page."""
    journal_entry = JournalEntry.objects.create(
        date=creditcard_entry.date, memo=creditcard_entry.generate_memo(),
        comments=creditcard_entry.comments
    )
    creditcard_detail = 'Purchase by {}'.format(creditcard_entry.name)
    Transaction.objects.create(
        journal_entry=journal_entry, account=creditcard_entry.card.account,
        balance_delta=creditcard_entry.amount, detail=creditcard_detail,
    )
    for transaction in creditcard_entry.transaction_set.all():
        Transaction.objects.create(
            journal_entry=journal_entry, account=transaction.account,
            detail=transaction.detail, balance_delta=(-1 * transaction.amount)
        )
    for receipt in creditcard_entry.receipt_set.all():
        new_receipt = ContentFile(receipt.receipt_file.file.read())
        new_receipt.name = receipt.receipt_file.name
        Receipt.objects.create(
            journal_entry=journal_entry, receipt_file=new_receipt)

    messages.success(
        request,
        ("Approved the Credit Card Entry & Created <a href='{}' "
         "target='_blank'>{}</a>.".format(
             journal_entry.get_absolute_url(), journal_entry.get_number()))
    )

    redirect_url = None
    if redirect_to_next:
        next_entry = CreditCardEntry.objects.filter(
            card=creditcard_entry.card, date__gte=creditcard_entry.date
        ).exclude(pk=creditcard_entry.pk).order_by('date', 'id')
        if next_entry.exists():
            redirect_url = reverse('creditcards.views.add_creditcard_entry',
                                   args=[str(next_entry[0].id)])
    if redirect_url is None:
        redirect_url = reverse('creditcards.views.list_creditcard_entries')
    creditcard_entry.delete()
    return HttpResponseRedirect(redirect_url)
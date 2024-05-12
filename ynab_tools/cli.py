import csv
import logging

from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import click

from .api_session import BaseClient


LOGGER = logging.getLogger(__name__)
logging.basicConfig()

@click.group()
@click.version_option()
def cli():
    "Tools for use with YNAB (\"You Need A Budget\")"


@cli.command(name="get-excess-spending")
@click.option(
    "-b",
    "--budget-id",
    help="Budget ID to query. If absent, default to the first one.",
)
@click.option(
    "-m",
    "--month",
    help="Month for which to detect overspending (format YYYYMM)"
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Enable debug logging"
)
def get_excess_spending(
      budget_id: Optional[str],
      month: Optional[str],
      debug: bool):
    """
    YNAB already has a definition of overspending - "activity is greater than assigned" (i.e. spending money that has
    not already been earmarked for that purpose). This is not that.

    Rather, this means "activity in the month exceeded the target" - spending more than you _expected_ to. This allows
    the identification of poorly-set _targets_, which - to use YNAB's own terminology - helps you to "Embrace Your True
    Expenses" - if your targets do not cover your actual usual expenses, they are poorly-set targets. While it's good to
    "Roll With The Punches", accurate anticipation can reduce the number of incoming punches.
    """

    client = BaseClient()

    if not budget_id:
        budget_id = _get_budget_id(client)
    if not month:
        month = f"{datetime.now().year}-{str(datetime.now().month-1).rjust(2, '0')}-01"
    if debug:
        LOGGER.root.setLevel(logging.DEBUG)

    logging.debug(f"Budget Id is {budget_id}")
    logging.debug(f"Month is {month}")

    # TODO - parameterizable
    output_path = Path('output.csv')
    if output_path.exists():
        raise Exception(f'Output path {output_path} already exists')

    budget_data_for_month = client.get(f'/budgets/{budget_id}/months/{month}')['data']['month']['categories']
    LOGGER.debug(budget_data_for_month)


    # (`category_id`, `reason`)
    failed_processing: List[Tuple[str, str]] = []
    excess_spent_categories = []
    for category_info in budget_data_for_month:
        try:
            if _is_excess_spent_eligible_category(category_info):
                excess_spent_categories.append(category_info)
            else:
                continue
        except Exception as e:
            # TODO - probably make this less chatty. Some exceptions are expected - e.g. checking a month before the
            # category was created
            LOGGER.error(e)
            failed_processing.append((category_info['id'], str(e)))

    with output_path.open('w') as f:
        field_names = ['id', 'category_group_id', 'name', 'category_group_name', 'activity', 'goal_target']
        writer = csv.DictWriter(f, field_names)
        writer.writeheader()

        for category in excess_spent_categories:
            writer.writerow({field: category[field] for field in field_names})

    click.echo(f'Wrote output to {output_path}')


def _get_budget_id(client: BaseClient) -> str:
    return client.get('/budgets')['data']['budgets'][0]['id']

def _is_excess_spent_eligible_category(category_info) -> bool:
    """
    Initially, only look for categories with a monthly target, as that makes overspending easier to detect ("was
    spending in this month greater than the target?"). Other types of targets (e.g. quarterly) would require
    looking-back over multiple months.
    """
    return _is_monthly_target(category_info) and _is_excess_spent(category_info)

def _is_monthly_target(category_info) -> bool:
    LOGGER.debug(f'Checking is_monthly_target for {category_info}')
    return category_info['goal_type'] == 'NEED' and category_info['goal_cadence'] == 1

def _is_excess_spent(category_info) -> bool:
    return -(category_info['activity']) > category_info['goal_target']

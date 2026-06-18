import math
from abc import ABC, abstractmethod


# ==========================================================
# Play Calculators (Strategy)
# ==========================================================

class PlayCalculator(ABC):
    def __init__(self, performance, play):
        self.performance = performance
        self.play = play

    @property
    @abstractmethod
    def amount(self):
        pass

    @property
    def volume_credits(self):
        return max(self.performance["audience"] - 30, 0)


class TragedyCalculator(PlayCalculator):
    @property
    def amount(self):
        result = 40000
        if self.performance["audience"] > 30:
            result += 1000 * (self.performance["audience"] - 30)
        return result


class ComedyCalculator(PlayCalculator):
    @property
    def amount(self):
        result = 30000

        if self.performance["audience"] > 20:
            result += 10000 + 500 * (self.performance["audience"] - 20)

        result += 300 * self.performance["audience"]
        return result

    @property
    def volume_credits(self):
        return (
            super().volume_credits
            + math.floor(self.performance["audience"] / 5)
        )


def create_calculator(performance, play):
    if play["type"] == "tragedy":
        return TragedyCalculator(performance, play)

    if play["type"] == "comedy":
        return ComedyCalculator(performance, play)

    # Los tipos futuros aún no están implementados
    if play["type"] in ("history", "pastoral"):
        raise ValueError(f'unknown type: {play["type"]}')

    raise ValueError(f'unknown type: {play["type"]}')


# ==========================================================
# Statement Printers (Strategy)
# ==========================================================

class StatementPrinter(ABC):

    @abstractmethod
    def render(self, data):
        pass

    @staticmethod
    def format_as_dollars(amount):
        return f"${amount:0,.2f}"


class TextStatementPrinter(StatementPrinter):

    def render(self, data):
        result = f'Statement for {data["customer"]}\n'

        for perf in data["performances"]:
            result += (
                f' {perf["play"]["name"]}: '
                f'{self.format_as_dollars(perf["amount"] / 100)} '
                f'({perf["audience"]} seats)\n'
            )

        result += (
            f'Amount owed is '
            f'{self.format_as_dollars(data["total_amount"] / 100)}\n'
        )
        result += (
            f'You earned {data["volume_credits"]} credits\n'
        )

        return result


class HtmlStatementPrinter(StatementPrinter):

    def render(self, data):
        result = f"<h1>Statement for {data['customer']}</h1>\n"
        result += "<table>\n"
        result += (
            "<tr>"
            "<th>Play</th>"
            "<th>Seats</th>"
            "<th>Cost</th>"
            "</tr>\n"
        )

        for perf in data["performances"]:
            result += (
                "<tr>"
                f"<td>{perf['play']['name']}</td>"
                f"<td>{perf['audience']}</td>"
                f"<td>{self.format_as_dollars(perf['amount'] / 100)}</td>"
                "</tr>\n"
            )

        result += "</table>\n"
        result += (
            f"<p>Amount owed is "
            f"<em>{self.format_as_dollars(data['total_amount'] / 100)}</em></p>\n"
        )
        result += (
            f"<p>You earned "
            f"<em>{data['volume_credits']}</em> credits</p>\n"
        )

        return result


# ==========================================================
# Data preparation
# ==========================================================

def create_statement_data(invoice, plays):

    def play_for(performance):
        return plays[performance["playID"]]

    performances = []
    total_amount = 0
    volume_credits = 0

    for perf in invoice["performances"]:
        play = play_for(perf)

        calculator = create_calculator(perf, play)

        enriched_perf = {
            **perf,
            "play": play,
            "amount": calculator.amount,
            "volume_credits": calculator.volume_credits,
        }

        performances.append(enriched_perf)

        total_amount += calculator.amount
        volume_credits += calculator.volume_credits

    return {
        "customer": invoice["customer"],
        "performances": performances,
        "total_amount": total_amount,
        "volume_credits": volume_credits,
    }


# ==========================================================
# Public API
# ==========================================================

def statement(invoice, plays):
    """
    Mantiene la firma original para no romper las pruebas existentes.
    """
    data = create_statement_data(invoice, plays)
    return TextStatementPrinter().render(data)


def html_statement(invoice, plays):
    """
    Nueva salida HTML.
    """
    data = create_statement_data(invoice, plays)
    return HtmlStatementPrinter().render(data)

import math


def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = f'Statement for {invoice["customer"]}\n'

    def format_as_dollars(amount):
        return f"${amount:0,.2f}"

    def play_for(perf):
        return plays[perf['playID']]

    def calculate_credits(perf):
        play = play_for(perf)
        credits = 0
        # add volume credits
        credits += max(perf['audience'] - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == play["type"]:
            credits += math.floor(perf['audience'] / 5)
        return credits

    def amount_for(perf):
        play = play_for(perf)
        if play['type'] == "tragedy":
            this_amount = 40000
            if perf['audience'] > 30:
                this_amount += 1000 * (perf['audience'] - 30)
        elif play['type'] == "comedy":
            this_amount = 30000
            if perf['audience'] > 20:
                this_amount += 10000 + 500 * (perf['audience'] - 20)

            this_amount += 300 * perf['audience']

        else:
            raise ValueError(f'unknown type: {play["type"]}')
        return this_amount

    for perf in invoice['performances']:
        play = play_for(perf)

        volume_credits += calculate_credits(perf)

        # print line for this order
        result += f' {play["name"]}: {format_as_dollars(amount_for(perf)/100)} ({perf["audience"]} seats)\n'
        total_amount += amount_for(perf)

    result += f'Amount owed is {format_as_dollars(total_amount/100)}\n'
    result += f'You earned {volume_credits} credits\n'
    return result

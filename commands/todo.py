from hashlib import sha1
from datetime import datetime

name = 'todo'
aliases = ('делать')
help = 'pass a list of choices separated by \'|\' and let bot decide what is more important to you'


def compose_response(choices, distr):
    max_choice_len = max(map(len, choices))
    tmp = {d: c for d, c in zip(distr, choices)}
    s_distr = sorted(distr, reverse=True)
    s_choices = [tmp[d] for d in s_distr]
    choice_dist = '\n'.join(['<code>{} {} {:.2f}%</code>'.format(c,
                                                                 '─' *
                                                                 (max_choice_len - len(c) +
                                                                  (0 if (d // 10) else 1) + 1),
                                                                 d)
                             for c, d in zip(s_choices, s_distr)])
    return f'you should do:\n{choice_dist}'


async def handler(args, request):
    if not args:
        return await request.reply(help)
    raw_choices = ' '.join(args)
    choices = list(
        set([c for c in map(lambda c: c.strip(), raw_choices.split('|')) if c]))
    if len(choices) == 1:
        await request.reply('you always have other options, think better')
    else:
        weights = list(
            map(lambda c: int(sha1(c.encode('utf8')).hexdigest(), base=16),
                map(lambda c: f'{datetime.now().timetuple().tm_yday}{request.event.sender}{c}', choices)))
        total_weight = sum(weights)
        distribution = list(
            map(lambda w: w * 100 / total_weight, weights))
        response = compose_response(choices, distribution)
        await request.reply(response, formatted=True)

import argparse
from nani.fetcher import Fetcher
import textwrap


# nani entry point
def run():
    parser = argparse.ArgumentParser(
        prog='nani',
        description='A Software Development Question & Answer Aggregator.')

    parser.add_argument(
        'search',
        type=str,
        nargs='+',
        help='The question your want to search')

    parser.add_argument(
        '-r',
        '--results',
        type=int,
        default=3,
        help='The number of results to return')

    parser.add_argument(
        '-u',
        '--unsupported',
        type=bool,
        default=False,
        help='Display the unsupported results')

    args = parser.parse_args()

    exit = False
    fetch = Fetcher(args.unsupported)  # create the fetcher object.
    fetch.fetch_search(args.search, args.results)
    focus = None

    exits = ['q', 'Q', 'Quit', 'quit', 'exit', 'Exit', 'done', 'Done']
    opens = ['o', 'O', 'Open', 'open']
    backs = ['b', 'B', 'Back', 'back']
    helps = ['h', 'H', 'Help', 'help']

    help = '''
Help:\n
===Search List===\n
\t<number> - Select a search result\n
\tquit - Quit the Nani search\n
\t\tAliases: q, quit, exit, done\n
\thelp - This help output\n
\t\tAliases: h, help\n
===Answer List===\n
\topen - Open this page in your default browser\n
\t\tAliases: o, open\n
\tback - Go back to the Search List\n
\t\tAliases: b, back\n'''

    if fetch.max_results < 1:  # if there is no useable results exit out.
        exit = True
        print('No Results Found For: '+' '.join(args.search))

    while not exit:  # handle the commands that the user inputs.
        print(fetch.format_output(focus))
        in_string = input(">")
        if focus is not None:
            if in_string in opens:
                fetch.open_page(focus)
            elif in_string in backs:
                focus = None
            elif in_string in exits:
                exit = True
            else:
                print('Unrecognised Command. back OR open')
        else:
            if in_string in helps:
                print(help)
            elif in_string in exits:
                exit = True
            else:
                try:
                    focus = int(in_string)
                    if focus > fetch.max_results or focus < 1:
                        print('No Matching Result!')
                        focus = None
                    else:
                        focus = focus-1
                except:
                    print('Unrecognised command, Use help')
                    focus = None


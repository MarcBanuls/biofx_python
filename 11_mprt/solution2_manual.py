#!/usr/bin/env python3
""" Find locations of N-glycosylation motif """

import argparse
import os
import requests
import sys
from typing import NamedTuple, List, TextIO
from Bio import SeqIO


class Args(NamedTuple):
    file: TextIO
    download_dir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Find locations of N-glycosylation motif',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='Input text file of UniProt IDs',
                        metavar='FILE',
                        type=argparse.FileType('rt'))

    parser.add_argument('-d',
                        '--download_dir',
                        help='Directory for downloads',
                        metavar='DIR',
                        type=str,
                        default='fasta')

    args = parser.parse_args()

    return Args(args.file, args.download_dir)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    files = fetch_fasta(args.file, args.download_dir)

    for file in files:
        prot_id, _ = os.path.splitext(os.path.basename(file))
        if recs := list(SeqIO.parse(file, 'fasta')):
            if matches := find_motif(str(recs[0].seq)):
                pos = map(lambda p: p + 1, matches)
                print('\n'.join([prot_id, ' '.join(map(str, pos))]))


# --------------------------------------------------
def fetch_fasta(fh: TextIO, fasta_dir: str) -> List[str]:
    """ Fetch the FASTA files into the download directory """

    if not os.path.isdir(fasta_dir):
        os.makedirs(fasta_dir)

    files = []
    for prot_id in map(str.rstrip, fh):
        fasta = os.path.join(fasta_dir, prot_id + '.fasta')
        if not os.path.isfile(fasta):
            url = f'http://www.uniprot.org/uniprot/{prot_id}.fasta'
            response = requests.get(url)
            if response.status_code == 200:
                fh = open(fasta, 'wt')
                fh.write(response.text)
                fh.close()
            else:
                print(f'Error fetching "{url}": "{response.status_code}"',
                      file=sys.stderr)
                continue

        files.append(fasta)

    return files


# --------------------------------------------------
def find_motif(text: str) -> List[int]:
    """ Find a pattern in some text """
    def is_match(s: str) -> bool:
        return s[0] == 'N' and s[1] != 'P' and s[2] in 'ST' and s[3] != 'P'

    kmers = list(enumerate(find_kmers(text, 4)))
    return [i for i, kmer in kmers if is_match(kmer)]


# --------------------------------------------------
def test_find_motif() -> None:
    """ Test find_pattern """

    assert find_motif('') == []
    assert find_motif('NPTX') == []
    assert find_motif('NXTP') == []
    assert find_motif('NXSX') == [0]
    assert find_motif('ANXTX') == [1]
    assert find_motif('NNTSYS') == [0, 1]
    assert find_motif('XNNTSYS') == [1, 2]


# --------------------------------------------------
def find_kmers(seq: str, k: int) -> List[str]:
    """ Find k-mers in string """

    n = len(seq) - k + 1
    return [] if n < 1 else [seq[i:i + k] for i in range(n)]


# --------------------------------------------------
def test_find_kmers() -> None:
    """ Test find_kmers """

    assert find_kmers('', 1) == []
    assert find_kmers('ACTG', 1) == ['A', 'C', 'T', 'G']
    assert find_kmers('ACTG', 2) == ['AC', 'CT', 'TG']
    assert find_kmers('ACTG', 3) == ['ACT', 'CTG']
    assert find_kmers('ACTG', 4) == ['ACTG']
    assert find_kmers('ACTG', 5) == []


# --------------------------------------------------
if __name__ == '__main__':
    main()

#!/usr/bin/env python3
""" Translate RNA to proteins """

import argparse
from typing import NamedTuple, List


class Args(NamedTuple):
    """ Command-line arguments """
    rna: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Translate RNA to proteins',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('rna', type=str, metavar='RNA', help='RNA sequence')

    args = parser.parse_args()

    return Args(args.rna)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    rna = args.rna.upper()
    codon_to_aa = {
        'AAA': 'K', 'AAC': 'N', 'AAG': 'K', 'AAU': 'N', 'ACA': 'T',
        'ACC': 'T', 'ACG': 'T', 'ACU': 'T', 'AGA': 'R', 'AGC': 'S',
        'AGG': 'R', 'AGU': 'S', 'AUA': 'I', 'AUC': 'I', 'AUG': 'M',
        'AUU': 'I', 'CAA': 'Q', 'CAC': 'H', 'CAG': 'Q', 'CAU': 'H',
        'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCU': 'P', 'CGA': 'R',
        'CGC': 'R', 'CGG': 'R', 'CGU': 'R', 'CUA': 'L', 'CUC': 'L',
        'CUG': 'L', 'CUU': 'L', 'GAA': 'E', 'GAC': 'D', 'GAG': 'E',
        'GAU': 'D', 'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCU': 'A',
        'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGU': 'G', 'GUA': 'V',
        'GUC': 'V', 'GUG': 'V', 'GUU': 'V', 'UAC': 'Y', 'UAU': 'Y',
        'UCA': 'S', 'UCC': 'S', 'UCG': 'S', 'UCU': 'S', 'UGC': 'C',
        'UGG': 'W', 'UGU': 'C', 'UUA': 'L', 'UUC': 'F', 'UUG': 'L',
        'UUU': 'F', 'UAA': '*', 'UAG': '*', 'UGA': '*',
    }

    # Method 1: for loop
    protein = ''
    for codon in codons(rna, 3):
        aa = codon_to_aa.get(codon, '-')
        if aa == '*':
            break
        protein += aa

    print(protein)


# --------------------------------------------------
def codons(seq: str, k: int) -> List[str]:
    """ Extract k-sized codons from a sequence """

    # assert k > 0

    # if k < 1:
    #     return []

    # ret = []
    # for codon in [seq[i:i + k] for i in range(0, len(seq), k)]:
    #     ret.append(codon)

    # return ret

    return [] if k < 1 else [seq[i:i + k] for i in range(0, len(seq), k)]


# --------------------------------------------------
def test_codons() -> None:
    """ Test codons """

    assert codons('', 0) == []
    assert codons('', 1) == []
    assert codons('A', 1) == ['A']
    assert codons('A', 2) == ['A']
    assert codons('ABC', 3) == ['ABC']
    assert codons('ABCDE', 3) == ['ABC', 'DE']
    assert codons('ABCDEF', 3) == ['ABC', 'DEF']


# --------------------------------------------------
if __name__ == '__main__':
    main()

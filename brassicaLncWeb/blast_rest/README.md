# Bundled BLAST REST runtime

Copied from the local `blast_rest` checkout (upstream metadata: https://github.com/fbluewhale/blast_rest, author fbluewhale, MIT License). The repository's legacy gitlink has no `.gitmodules` entry, so production uses this normal tracked package instead. It contains the REST view, record helpers, and nucleotide reference database. Database paths are relative to this package. Keep these files in version control; no separate BLAST service or pip package is required.

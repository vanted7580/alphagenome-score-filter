# Github @vanted7580


import openpyxl

from alphagenome.data import genome
from alphagenome.models import dna_client
from alphagenome.models import variant_scorers

API_KEY = ''
REQUESTED_OUTPUTS = [
    dna_client.OutputType.RNA_SEQ
]
REQUIRED_BIOSAMPLE_KEYWORDS = [
    'cardio'
]

model = dna_client.create(API_KEY)

data_workbook = openpyxl.load_workbook(filename='data.xlsx')
data_sheet = data_workbook.worksheets[0]
data_sheet.delete_rows(idx=1, amount=1)

chromosomes = [c.value for c in data_sheet['A']]  # chr_hg38
start = [c.value for c in data_sheet['B']]  # start
end = [c.value for c in data_sheet['C']]  # end
positions = [c.value for c in data_sheet['M']]  # Var_Pos
reference_bases = [c.value for c in data_sheet['N']]  # REF
alternate_bases = [c.value for c in data_sheet['O']]  # ALT
ontology_terms = ['UBERON:0001157']
variant_scorers_ = [
    variant_scorers.RECOMMENDED_VARIANT_SCORERS['RNA_SEQ'],
]

for i in range(len(chromosomes)):

    print("------------------------------")

    missing_key = []

    if chromosomes[i] is None: missing_key.append('chromosome')
    if start[i] is None: missing_key.append('start')
    if end[i] is None: missing_key.append('end')
    if positions[i] is None: missing_key.append('position')
    if reference_bases[i] is None: missing_key.append('reference_base')
    if alternate_bases[i] is None: missing_key.append('alternate_base')

    if missing_key:
        print(f"Skipping row {i + 2}: missing key {', '.join(missing_key)}")
        continue

    interval = genome.Interval(
        chromosome=chromosomes[i],
        start=start[i],
        end=end[i]
    )

    variant = genome.Variant(
        chromosome=chromosomes[i],
        position=positions[i],
        reference_bases=reference_bases[i],
        alternate_bases=alternate_bases[i]
    )

    # output = model.predict_variant(
    #     interval=interval,
    #     variant=variant,
    #     ontology_terms=ontology_terms,
    #     requested_outputs=REQUESTED_OUTPUTS
    # )

    variant_scores = model.score_variant(
        interval=interval,
        variant=variant,
        variant_scorers=variant_scorers_)

    for variant_score in variant_scores:

        raw = variant_score.X
        quant = variant_score.layers['quantiles']

        genes = variant_score.obs['gene_name']
        biosamples = variant_score.var['biosample_name']

        # Filters
        filtered_genes = genes[(raw > 0.2).any(axis=1)]
        top_genes = genes[(quant > 0.9).any(axis=1)]

        requested_output = variant_score.uns['variant_scorer'].requested_output.name

        # Biosample name
        matched_keyword = []

        for keyword in REQUIRED_BIOSAMPLE_KEYWORDS:
            if biosamples.str.contains(keyword, case=False, na=False).any():
                matched_keyword.append(keyword)

        # if not matched_keyword: continue

        print(f"Matched keywords: {', '.join(matched_keyword)}")

        print(
            f"Variant #{i + 1} ({variant.chromosome}:{variant.position} {variant.reference_bases} -> {variant.alternate_bases})")

        print(f"Requested output: {requested_output}")
        print(f"Filtered genes (raw_score): {len(filtered_genes)}")

        if not filtered_genes.empty: print("    ", ", ".join(filtered_genes))
        print(f"Filtered genes (quantile_score): {len(top_genes)}")

        if not top_genes.empty: print("    ", ", ".join(top_genes))

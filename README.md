#### Filter results by:

###### Keywords
```
REQUIRED_BIOSAMPLE_KEYWORDS = [
    'cardio'，
    <str>
]
```
###### Raw score
```
filtered_mask = ((raw > 0.1) & (raw < 1)).any(axis=1)
```
###### Quantile score
```
top_mask = ((quant > -1) & (quant < 0.5)).any(axis=1)
```

#### Example Output
```
------------------------------
Matched keywords: 
Variant #1 (chr22:36201698 A -> C)
Requested output: RNA_SEQ
Filtered genes (raw_score): 7
     MTCO3P20, MTND1P10, MTCO2P20, MTCO1P20, MTCYBP34, MTATP6P20, ENSG00000288778
Filtered genes (quantile_score): 37
     RBFOX2, APOL4, APOL1, MYH9, TXN2, FOXRED2, EIF3D, APOL3, APOL5, APOL2, CACNG2, ENSG00000188078, MYH9-DT, MTCO3P20, MRPS16P3, ENSG00000228587, ENSG00000228719, MTND1P10, ENSG00000229971, MTCO2P20, MTCO1P20, CACNG2-DT, MTCYBP34, NDUFA9P1, RPS15AP38, MTATP6P20, Y_RNA, ENSG00000261675, MIR6819, ENSG00000279217, ENSG00000279652, ENSG00000279714, ENSG00000279805, ENSG00000279927, ENSG00000287269, ENSG00000288778, ENSG00000293594
------------------------------
```

#### Requirements
```
pip install openpyxl
```
[https://github.com/google-deepmind/alphagenome](https://github.com/google-deepmind/alphagenome)

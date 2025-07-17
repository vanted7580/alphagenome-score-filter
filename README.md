### Filter result by:

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

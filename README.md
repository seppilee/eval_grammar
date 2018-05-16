## edit distance tagging

## eval_grammar
not yet working properly.

```
The spellchecker accuracy is measured in terms of standard precision/recall are measured.
Precision/recall measures are calculated at two levels: (i) detection and (ii) correction.
For both levels, precision/recall and other related measures are calculated as follows:
|Precision      - TP / (TP + FP)
|Recall         - TP / (TP + FN)
|F1-measure     - 2 * (precision * recall) / (precision + recall)
|F0.5-measure   - 1.25 * (precision * recall) /(0.25 * precision) +recall
|F2 -           -  5  * (precision * recall) /(4 * precision) +recall
|Accuracy       - (TP + TN) / (TP + FP + TN + FN)
```
### Error detection
```
|**TP** - Number of words with spelling errors that the spell checker detected correctly
|**FP** - Number of words identified as spelling errors that are not actually spelling errors
|**TN** - Number of correct words that the spell checker did not flag as having spelling errors
|**FN** - Number of words with spelling errors that the spell checker did not flag as having spelling errors
```
### Error correction
```
|**TP** - Number of words with spelling errors for which the spell checker gave the correct suggestion
|**FP** - Number of words (with/without spelling errors) for which the spell checker made suggestions, and for those,
|         either the suggestion is not needed (in the case of non-existing errors) or the suggestion is incorrect if
|         indeed there was an error in the original word.
|**TN** - Number of correct words that the spell checker did not flag as having spelling errors and no
|         suggestions were made.
|**FN** - Number of words with spelling errors that the spell checker did not flag as having spelling errors or did not
|         provide any suggestions
```


###  PART -1 DATA FOUNDATION AND VALIDATION
### STEP-4 Data quality Report

1)Remove exact duplicates	
Dimension : Uniqueness	
Explanation & Fix :Removing duplicate records ensures that the same order record is not counted more than once.It was fixed using 'drop_duplicates()'

2)Normalize region names
Dimension : Consistency
Explanation & Fix : Region names may contain leading/trailing spaces or different capitalization.Leading and trailing spaces were removed and region names were converted to title case.

3)Impute missing Category values
Dimension : Completeness
Explanation & Fix : Missing category values make the dataset incomplete. Filling them using the product-to-category relationship using lookup function makes the records more complete.

4)Impute missing Profit values
Dimension : Completeness,Accuracy
Explanation & Fix : The missing profit values are filled using the category-level profit-margin pattern in the available data instead of simply dropping the records.The result was rounded off upto 2 decimal for accurate values.

5)Schema Validation
Dimension : Validity
Explanation :  The schema must contain the required fields for the dataset to be processed correctly.A validate_schema() function checks whether every required column is present before the data continues through the pipeline.

# Aggregated-Policies-Biparty-Decision-Theory


## Structure
- `src` that contains the source Python code;
- `data` that contains the benchmark data, see the relative `README` for downloading the data.
- `results` contains the results for the performance of the policies;
- `settings.py` contains the main settings for the experiments as described in the paper below;



## Requirements
The following Python packages are required:

-   [numpy](http://www.numpy.org/) tested with version 1.25.0;
-   [pandas](https://pandas.pydata.org/) tested with version 2.0.2.
-   [matplotlib](https://matplotlib.org/) tested with version 3.7.1;
-   [https://seaborn.pydata.org/](https://seaborn.pydata.org/) tested with version 0.12.2.
-   [pygraphviz](https://pypi.org/project/pygraphviz/) tested with version 1.7.0.




### Running the code

To run the policy experiments for a given dataset (don2022 or don2022NoOPT), type:
```
python3 run_policy_experiments.py --ds=don2022
```
or
```
python3 run_policy_experiments.py --ds=don2022NoOPT
```

To run the metrics evaluation, type:
```
python3 run_policy_experiments.py --ds=don2022
```
for the don2022 dataset or
```
python3 run_policy_experiments.py --ds=don2022NoOPT
```
for the don2022NoOPT dataset. 

### Results
After running the experiments, the results are .. in the `results` folder. 


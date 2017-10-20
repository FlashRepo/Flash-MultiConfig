Data/ -> Folder to store the configurations evaluated by ePAL

The scripts has to be executed in the following order:
1. extract_actual_pareto_frontier.py -> To extract the actual pareto frontier from the raw data (../Data/)
2. extract_predicted_pareto_frontier.py -> To extract the frontier from the solutions evaluated by ePAL
3. get_performance_measure.py -> To extract the performance measures (IGD and GD)
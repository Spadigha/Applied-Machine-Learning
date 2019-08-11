## Dependencies

To run these notebooks you'll need to install Python 3.6+, Numpy, Jupyter Notebooks and many other packages. The easiest way for all of this efficientlty is to create a conda environment:

```
conda create -n myEnv python=3.6
conda activate myEnv
conda install numpy jupyter notebook pandas
pip install abc=x.y.z
```

To deactivate an active environment, use
```
conda deactivate
```

make exact clone of env
```
conda create --name myclone --clone myenv
```

To see if a specific package is installed in an environment, in your terminal window or an Anaconda Prompt, run:
```
conda list -n myenv scipy
```
or enter into the environment and simply type
```
conda list
```

To remove an environment, in your terminal window or an Anaconda Prompt, run:
```
conda remove --name myenv --all
```

To verify that the environment was removed, in your terminal window or an Anaconda Prompt, run:
```
conda info --envs
```

for more info: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
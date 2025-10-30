# [NeurIPS'25 Spotlight]LLM Meeting Decision Trees on Tabular Data

<div style="text-align: center; margin: 20px 0;">
  <img src="picture/framework1-1.png" alt="The DeLTa framework" style="max-width: 100%; height: auto;">
</div>

## Official implementation of the experiments in the [DeLTa paper]().

## Usage Options

### Option1: Quick verify the experiments reported in the paper


#### 1. Obtain the rules of the RandomForest.
 
```bash
cd DeLTa-main
python run_randforest.py
```
#### 2. Fit the negative gradient.
    
```bash
cd DeLTa-main
python run.py
```
#### 3. run  error correction
    
```bash
cd DeLTa-main
python run_ensemble.py
```

### Option2: Including the steps to query the LLM yourself

#### 1. Obtain the rules of the RandomForest.
 
```bash
cd DeLTa-main
python run_randforest.py
```

#### 2. Build prompts

```bash
cd DeLTa-main/llm/get_prompts
python run_get_prompt.py
```


#### 3. query the LLM and get answer 
Our method has been validated with these three LLMs (GPT-4o, Qwen3-32B, and Qwen3-8B), though you are also welcome to use other models.
```bash
cd DeLTa-main/llm/query
python run_get_answer.py
```

#### 4. Place the generated rules in a Python file within the directory DeLTa-main/model/llm_rule

```bash
cd DeLTa-main/llm
python get_trees.py
```

#### 5. Fit the negative gradient.
    
```bash
cd DeLTa-main
python run.py
```
#### 6. run  error correction
    
```bash
cd DeLTa-main
python run_ensemble.py
```

Datasets are accessible via [Google Drive](https://drive.google.com/open?id=1JIsivUoM4qeM3MY9jNpXjJJH4VplndCy&usp=drive_fs).



## Citation

If you use DeLTa in your research, please cite:

```bibtex

```

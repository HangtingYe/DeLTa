# LLM Meeting Decision Trees on Tabular Data




<div style="text-align: center; margin: 20px 0;">
  <img src="picture/framework1-1.png" alt="The DeLTa framework" style="max-width: 100%; height: auto;">
  <p style="margin-top: 8px; font-weight: 500;">The DeLTa framework</p>
</div>


## Quick Start


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

## Including the steps to query the LLM yourself

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

Get tree rules
```bash
cd DeLTa-main/llm
python get_trees.py
```

#### 3. query the LLM and get answer
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
